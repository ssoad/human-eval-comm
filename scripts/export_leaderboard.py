#!/usr/bin/env python3
"""
Export a multi-dimensional leaderboard CSV by combining:
- Communication metrics parsed from log files
- Code and reliability metrics from evaluation_results.jsonl

Outputs: results/leaderboard.csv
"""

import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class CommMetrics:
    total_entries: int = 0
    question_entries: int = 0
    good_question_entries: int = 0
    questions_per_problem_sum: int = 0
    problems_count: int = 0

    def comm_rate(self) -> float:
        if self.total_entries == 0:
            return 0.0
        return (self.question_entries / self.total_entries) * 100.0

    def good_q_rate(self) -> float:
        if self.question_entries == 0:
            return 0.0
        return (self.good_question_entries / self.question_entries) * 100.0

    def clarification_efficiency(self) -> float:
        if self.problems_count == 0:
            return 0.0
        return self.questions_per_problem_sum / self.problems_count


def parse_model_from_filename(filename: str) -> str:
    # Example: ./log/dataset_HumanEvalComm_model_Okanagan_topn_1_temperature_1.log_3
    m = re.search(r"_model_([^_]+)_topn_", filename)
    return m.group(1) if m else "unknown"


def parse_comm_metrics(log_dir: str = "log") -> Dict[str, CommMetrics]:
    metrics_by_model: Dict[str, CommMetrics] = defaultdict(CommMetrics)

    if not os.path.isdir(log_dir):
        return metrics_by_model

    # Aggregate per model
    for name in os.listdir(log_dir):
        if (
            not name.endswith(".log_1")
            and not name.endswith(".log_2")
            and not name.endswith(".log_3")
            and not name.endswith(".log_0")
        ):
            continue
        file_path = os.path.join(log_dir, name)
        model = parse_model_from_filename(name)

        # Track per-problem question counts to compute efficiency
        per_problem_questions: Dict[str, int] = defaultdict(int)

        try:
            with open(file_path, "r") as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue

                    # Expect keys: name (problem), question_quality, response, code
                    problem_key = (
                        rec.get("name", "unknown") + "::" + rec.get("prompt_type", "")
                    )
                    qq = str(rec.get("question_quality", "0"))
                    metrics_by_model[model].total_entries += 1

                    # A question round if quality != '0'
                    is_question = qq not in ("0", "", None)
                    if is_question:
                        metrics_by_model[model].question_entries += 1
                        per_problem_questions[problem_key] += 1

                        # Good question: 2 or 3
                        try:
                            q_int = int(qq)
                        except Exception:
                            q_int = 0
                        if q_int >= 2:
                            metrics_by_model[model].good_question_entries += 1

        except Exception:
            continue

        # Aggregate per-problem question counts
        if per_problem_questions:
            metrics_by_model[model].questions_per_problem_sum += sum(
                per_problem_questions.values()
            )
            metrics_by_model[model].problems_count += len(per_problem_questions)

    return metrics_by_model


def load_eval_results(path: str = "evaluation_results.jsonl") -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        return rows
    with open(path, "r") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def aggregate_by_model(eval_rows: List[Dict[str, Any]], comm_by_model: Dict[str, CommMetrics]) -> Dict[str, Dict[str, float]]:
    agg: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    counts: Dict[str, int] = defaultdict(int)

    for r in eval_rows:
        model = r.get("model_name", "unknown")
        counts[model] += 1

        # Communication metrics (from eval results, but will be overridden by comm_by_model)
        agg[model]["communication_rate"] += r.get("communication_rate", 0.0)
        agg[model]["good_question_rate"] += r.get("good_question_rate", 0.0)

        # Code Correctness
        agg[model]["pass_at_1"] += r.get("pass_at_1", 0.0) * 100.0
        agg[model]["test_pass_rate"] += r.get("test_pass_rate", 0.0) * 100.0
        agg[model]["fuzz_test_robustness"] += r.get("fuzz_test_robustness", 0.0)

        # Code Trustworthiness
        agg[model]["readability_score"] += r.get("readability_100", 0.0)
        agg[model]["maintainability_index"] += r.get("maintainability_index_100", 0.0)
        agg[model]["security_score"] += r.get("security_100", 0.0)

        # Efficiency
        agg[model]["efficiency_normalized"] += r.get("efficiency_normalized", 0.0)
        agg[model]["runtime_sec"] += r.get("runtime_sec", 0.0)
        agg[model]["peak_memory_mb"] += r.get("peak_memory_mb", 0.0)

        # Reliability Indicators
        agg[model]["judge_consensus_confidence"] += r.get("judge_consensus_confidence", 0.0) * 100.0
        agg[model]["calibration_gap_percent"] += r.get("calibration_gap_percent", 0.0)

        # Composite Score
        agg[model]["v2_score"] += r.get("v2_composite_score", 0.0) * 100.0

    # Finalize
    finalized: Dict[str, Dict[str, float]] = {}
    for model, sums in agg.items():
        n = max(1, counts[model])
        comm_metrics = comm_by_model.get(model, CommMetrics())
        finalized[model] = {
            "Communication Rate": round(comm_metrics.comm_rate(), 1),
            "Good Question Rate": round(comm_metrics.good_q_rate(), 1),
            "Clarification Efficiency": round(comm_metrics.clarification_efficiency(), 2),
            "Pass@1": round(sums["pass_at_1"] / n, 1),
            "Test Pass Rate": round(sums["test_pass_rate"] / n, 1),
            "Fuzz Test Robustness": round(sums["fuzz_test_robustness"] / n, 1),
            "Readability Score": round(sums["readability_score"] / n, 1),
            "Maintainability Index": round(sums["maintainability_index"] / n, 1),
            "Security Score": round(sums["security_score"] / n, 1),
            "Efficiency": round(sums["efficiency_normalized"] / n, 3),
            "Runtime": round(sums["runtime_sec"] / n, 2),
            "Peak Memory": round(sums["peak_memory_mb"] / n, 2),
            "Judge Consensus Confidence": round(sums["judge_consensus_confidence"] / n, 1),
            "Calibration Gap": round(sums["calibration_gap_percent"] / n, 1),
            "V2 Score": round(sums["v2_score"] / n, 1),
        }
    return finalized


def write_leaderboard_csv(
    output_path: str,
    comm_by_model: Dict[str, CommMetrics],
    eval_by_model: Dict[str, Dict[str, float]],
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    headers = [
        "Model",
        "Comm Rate",
        "Good Q Rate",
        "Clarification Efficiency",
        "Pass@1",
        "Test Pass Rate",
        "Fuzz Test Robustness",
        "Readability Score",
        "Maintainability Index",
        "Security Score",
        "Efficiency",
        "Runtime",
        "Peak Memory",
        "Judge Consensus Confidence",
        "Calibration Gap",
        "V2 Score",
    ]
    with open(output_path, "w") as f:
        f.write(",".join(headers) + "\n")
        models = sorted(set(list(comm_by_model.keys()) + list(eval_by_model.keys())))
        for model in models:
            c = comm_by_model.get(model, CommMetrics())
            e = eval_by_model.get(model, {})
            row = [
                model,
                f"{c.comm_rate():.1f}%",
                f"{c.good_q_rate():.1f}%",
                f"{c.clarification_efficiency():.2f}",
                f"{e.get('Pass@1', 0.0):.1f}%",
                f"{e.get('Test Pass Rate', 0.0):.1f}%",
                f"{e.get('Fuzz Test Robustness', 0.0):.1f}%",
                f"{e.get('Readability Score', 0.0):.1f}",
                f"{e.get('Maintainability Index', 0.0):.1f}",
                f"{e.get('Security Score', 0.0):.1f}",
                f"{e.get('Efficiency', 0.0):.3f}",
                f"{e.get('Runtime', 0.0):.2f}",
                f"{e.get('Peak Memory', 0.0):.2f}",
                f"{e.get('Judge Consensus Confidence', 0.0):.1f}%",
                f"{e.get('Calibration Gap', 0.0):.1f}%",
                f"{e.get('V2 Score', 0.0):.1f}",
            ]
            f.write(",".join(map(str, row)) + "\n")


def main():
    comm_by_model = parse_comm_metrics("log")
    eval_rows = load_eval_results("evaluation_results.jsonl")
    eval_by_model = aggregate_by_model(eval_rows, comm_by_model)

    write_leaderboard_csv("results/leaderboard.csv", comm_by_model, eval_by_model)
    print("Leaderboard written to results/leaderboard.csv")


if __name__ == "__main__":
    main()
