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


def aggregate_by_model(eval_rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    agg: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    counts: Dict[str, int] = defaultdict(int)

    for r in eval_rows:
        model = r.get("model_name", "unknown")
        counts[model] += 1

        # Averages
        agg[model]["pass_at_1"] += 100.0 if r.get("test_pass_rate", 0) > 0 else 0.0
        agg[model]["test_pass_rate"] += r.get(
            "standard_composite_score", 0.0
        )  # placeholder if needed
        agg[model]["readability_100"] += r.get("readability_100", 0.0)
        agg[model]["security_100"] += r.get("security_100", 0.0)
        agg[model]["efficiency_normalized"] += r.get("efficiency_normalized", 0.0)
        agg[model]["v2_score"] += r.get("v2_composite_score", 0.0) * 10.0
        agg[model]["judge_consensus_confidence"] += (
            r.get("judge_consensus_confidence", 0.0) * 100.0
        )

    # Finalize
    finalized: Dict[str, Dict[str, float]] = {}
    for model, sums in agg.items():
        n = max(1, counts[model])
        finalized[model] = {
            "Pass@1": round(sums["pass_at_1"] / n, 1),
            "Test Pass": round(sums["test_pass_rate"] / n, 2),
            "Readability": round(sums["readability_100"] / n, 1),
            "Security": round(sums["security_100"] / n, 1),
            "Efficiency": round(sums["efficiency_normalized"] / n, 3),
            "Reliability": round(sums["judge_consensus_confidence"] / n / 100.0, 2),
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
        "Test Pass",
        "Readability",
        "Security",
        "Efficiency",
        "Reliability",
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
                f"{c.comm_rate():.0f}%",
                f"{c.good_q_rate():.0f}%",
                f"{c.clarification_efficiency():.2f}",
                f"{e.get('Pass@1', 0.0):.1f}%",
                f"{e.get('Test Pass', 0.0):.2f}",
                f"{e.get('Readability', 0.0):.0f}",
                f"{e.get('Security', 0.0):.0f}",
                f"{e.get('Efficiency', 0.0):.2f}",
                f"{e.get('Reliability', 0.0):.2f}",
                f"{e.get('V2 Score', 0.0):.1f}",
            ]
            f.write(",".join(map(str, row)) + "\n")


def main():
    comm_by_model = parse_comm_metrics("log")
    eval_rows = load_eval_results("evaluation_results.jsonl")
    eval_by_model = aggregate_by_model(eval_rows)

    write_leaderboard_csv("results/leaderboard.csv", comm_by_model, eval_by_model)
    print("Leaderboard written to results/leaderboard.csv")


if __name__ == "__main__":
    main()
