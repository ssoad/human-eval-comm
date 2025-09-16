#!/usr/bin/env python3
"""
HumanEvalComm V2 Model Benchmarking Script

Runs V2 evaluations for multiple models and generates a comprehensive leaderboard
with all required metrics as specified in the V2 framework.

Usage:
    python scripts/benchmark_models.py --models model1 model2 --data data.jsonl
"""

import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add evaluators to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluators.aggregator import Aggregator
from evaluators.automated_static_dynamic import AutomatedStaticDynamic
from evaluators.dashboard import EvaluationDashboard
from evaluators.enhanced_aggregator import EnhancedAggregator
from evaluators.human_calibration import HumanCalibrationSystem
from evaluators.hypothesis_fuzzer import HypothesisFuzzer
from evaluators.multi_llm_judge import MultiLLMJudge
from evaluators.sandbox_runner import SandboxRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("benchmark.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class ModelBenchmarker:
    """Benchmark multiple models using V2 evaluation framework."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the benchmarker."""
        logger.info("Initializing Model Benchmarker...")

        # Core components
        self.analyzer = AutomatedStaticDynamic()
        self.sandbox = SandboxRunner(use_docker=False)
        self.llm_judge = MultiLLMJudge(config_path)
        self.aggregator = Aggregator()
        self.hypothesis_fuzzer = HypothesisFuzzer()
        self.enhanced_aggregator = EnhancedAggregator()
        self.dashboard = EvaluationDashboard()

        # Results storage
        self.results = []

        logger.info("Model Benchmarker initialized successfully")

    def _readability_0_100(self, static_results) -> float:
        try:
            pylint_score = getattr(static_results, "pylint_score", 0.0) or 0.0
            cc = 0.0
            if hasattr(static_results, "complexity_metrics") and isinstance(
                static_results.complexity_metrics, dict
            ):
                cc = float(
                    static_results.complexity_metrics.get("cyclomatic_complexity", 0.0)
                    or 0.0
                )
            penalty = min(2.0, cc / 5.0)
            score_10 = max(0.0, pylint_score - penalty)
            return round(score_10 * 10.0, 1)
        except Exception:
            return 0.0

    def _maintainability_0_100(self, static_results) -> float:
        try:
            if hasattr(static_results, "complexity_metrics") and isinstance(
                static_results.complexity_metrics, dict
            ):
                mi = (
                    static_results.complexity_metrics.get("maintainability_index", 0.0)
                    or 0.0
                )
                mi = float(mi)
                mi = max(0.0, min(100.0, mi))
                pylint_issues = getattr(static_results, "pylint_issues", []) or []
                doc_penalty = 0.0
                convention_count = sum(
                    1
                    for i in pylint_issues
                    if (isinstance(i, dict) and i.get("type") == "convention")
                )
                if convention_count > 10:
                    doc_penalty = min(5.0, (convention_count - 10) * 0.3)
                return round(max(0.0, mi - doc_penalty), 1)
            return 0.0
        except Exception:
            return 0.0

    def _security_0_100(self, static_results) -> float:
        try:
            sec_10 = getattr(static_results, "security_score", 0.0) or 0.0
            return round(sec_10 * 10.0, 1)
        except Exception:
            return 0.0

    def _efficiency_normalized(self, sandbox_results) -> float:
        try:
            t = float(getattr(sandbox_results, "execution_time", 0.0) or 0.0)
            m = float(getattr(sandbox_results, "memory_used", 0.0) or 0.0)
            t_norm = max(0.0, min(1.0, 1.0 - (t / 5.0)))
            m_norm = max(0.0, min(1.0, 1.0 - (m / 100.0)))
            return round((t_norm + m_norm) / 2.0, 3)
        except Exception:
            return 0.0

    def _calibration_gap_percent(self, llm_scores) -> float:
        try:
            if not llm_scores or not hasattr(llm_scores, "judge_responses"):
                return 0.0
            score_std = getattr(llm_scores, "score_std", 0.0) or 0.0
            mean_conf = getattr(llm_scores, "mean_confidence", 0.0) or 0.0
            gap = ((score_std / 10.0) + max(0.0, 1.0 - mean_conf)) * 50.0
            return round(max(0.0, min(100.0, gap)), 1)
        except Exception:
            return 0.0

    def evaluate_model_solution(
        self,
        model_name: str,
        code: str,
        test_code: str,
        problem_description: str,
        problem_id: str,
    ) -> Dict[str, Any]:
        """Evaluate a single solution from a model."""

        logger.info(f"Evaluating {model_name} on {problem_id}")
        start_time = datetime.now()

        try:
            # 1. Static and Dynamic Analysis
            logger.info("Running static and dynamic analysis...")
            static_results, dynamic_results = self.analyzer.analyze_code(
                code, test_code, problem_id
            )

            # 2. Sandbox Execution
            logger.info("Running sandbox execution...")
            sandbox_results = self.sandbox.run_code(code, test_code)

            # 3. LLM Evaluation
            logger.info("Running LLM evaluation...")
            llm_scores = None
            try:
                import asyncio
                llm_scores = asyncio.run(
                    self.llm_judge.evaluate_code(code, problem_description)
                )
            except Exception as e:
                logger.warning(f"LLM evaluation failed: {e}")
                llm_scores = None

            # 4. Hypothesis Fuzzing
            logger.info("Running hypothesis fuzzing...")
            hypothesis_results = self.hypothesis_fuzzer.run_hypothesis_tests(
                code, test_code, self._extract_function_name(code)
            )

            # 5. Enhanced Aggregation (V2)
            logger.info("Running enhanced aggregation...")
            evaluation_data = {
                "problem_id": problem_id,
                "static_results": (
                    static_results.__dict__
                    if hasattr(static_results, "__dict__")
                    else static_results
                ),
                "dynamic_results": (
                    dynamic_results.__dict__
                    if hasattr(dynamic_results, "__dict__")
                    else dynamic_results
                ),
                "sandbox_results": (
                    sandbox_results.__dict__
                    if hasattr(sandbox_results, "__dict__")
                    else sandbox_results
                ),
                "llm_scores": (
                    llm_scores.__dict__
                    if llm_scores and hasattr(llm_scores, "__dict__")
                    else self._convert_llm_scores(llm_scores)
                ),
                "hypothesis_results": (
                    hypothesis_results.__dict__
                    if hasattr(hypothesis_results, "__dict__")
                    else hypothesis_results
                ),
            }

            enhanced_result = self.enhanced_aggregator.aggregate_results(
                evaluation_data
            )

            # 6. Store Results
            result_record = {
                "timestamp": datetime.now().isoformat(),
                "problem_id": problem_id,
                "model_name": model_name,
                "code_length": len(code),
                "test_code_length": len(test_code),
                # Communication metrics (set to 0 for now, would be parsed from logs)
                "communication_rate": 0,
                "good_question_rate": 0,
                # Code Correctness
                "pass_at_1": 1 if sandbox_results.success else 0,
                "test_pass_rate": (
                    dynamic_results.test_passes
                    if hasattr(dynamic_results, "test_passes")
                    else 0
                ),
                "fuzz_test_robustness": hypothesis_results.coverage_improvement if hypothesis_results else 0,
                # V2 results
                "v2_composite_score": enhanced_result.composite_score,
                "v2_weighted_score": enhanced_result.weighted_composite_score,
                "v2_formula_used": enhanced_result.formula_used,
                "v2_penalties_applied": enhanced_result.penalties_applied,
                "v2_bonuses_applied": enhanced_result.bonuses_applied,
                # Component scores
                "static_analysis_score": (
                    static_results.pylint_score
                    if hasattr(static_results, "pylint_score")
                    else 0
                ),
                "security_score": (
                    static_results.security_score
                    if hasattr(static_results, "security_score")
                    else 0
                ),
                "llm_consensus_score": llm_scores.consensus_score if llm_scores else 0,
                # V2 Features
                "hypothesis_tests_run": hypothesis_results.tests_run,
                "hypothesis_coverage_improvement": hypothesis_results.coverage_improvement,
                # Execution details
                "execution_success": sandbox_results.success,
                "execution_time": sandbox_results.execution_time,
                "memory_used": sandbox_results.memory_used,
                # Trustworthiness and efficiency
                "readability_100": self._readability_0_100(static_results),
                "maintainability_index_100": self._maintainability_0_100(static_results),
                "security_100": self._security_0_100(static_results),
                "efficiency_normalized": self._efficiency_normalized(sandbox_results),
                "runtime_sec": sandbox_results.execution_time,
                "peak_memory_mb": sandbox_results.memory_used,
                # Reliability indicators
                "judge_consensus_confidence": (
                    llm_scores.mean_confidence if llm_scores else 0.0
                ),
                "calibration_gap_percent": self._calibration_gap_percent(llm_scores),
                # Metadata
                "environment": {
                    "python_version": sys.version,
                    "platform": sys.platform,
                    "evaluation_version": "V2",
                },
            }

            self.results.append(result_record)

            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Evaluation completed in {execution_time:.2f}s")
            return result_record

        except Exception as e:
            logger.error(f"Evaluation failed for {model_name} on {problem_id}: {e}")
            return {
                "problem_id": problem_id,
                "model_name": model_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _extract_function_name(self, code: str) -> str:
        """Extract main function name from code."""
        import re
        match = re.search(r"def\s+(\w+)\s*\(", code)
        return match.group(1) if match else "unknown_function"

    def _convert_llm_scores(self, llm_scores) -> Dict[str, Any]:
        """Convert LLM scores to JSON-serializable format."""
        if not llm_scores:
            return {}
        result = {}
        if hasattr(llm_scores, "__dict__"):
            for key, value in llm_scores.__dict__.items():
                if hasattr(value, "__dict__"):
                    result[key] = {}
                    for sub_key, sub_value in value.__dict__.items():
                        result[key][sub_key] = sub_value
                elif isinstance(value, list):
                    result[key] = []
                    for item in value:
                        if hasattr(item, "__dict__"):
                            result[key].append(item.__dict__)
                        else:
                            result[key].append(item)
                else:
                    result[key] = value
        else:
            result = llm_scores if isinstance(llm_scores, dict) else {}
        return result

    def benchmark_models(self, model_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Benchmark multiple models on multiple problems."""
        results = []

        for item in model_data:
            result = self.evaluate_model_solution(
                model_name=item["model_name"],
                code=item["code"],
                test_code=item.get("test_code", ""),
                problem_description=item.get("problem_description", ""),
                problem_id=item.get("problem_id", f"{item['model_name']}_{len(results)}"),
            )
            results.append(result)

        return results

    def generate_leaderboard(self):
        """Generate the final leaderboard."""
        logger.info("Generating leaderboard...")

        # Save results
        with open("evaluation_results.jsonl", "w") as f:
            for result in self.results:
                f.write(json.dumps(result, default=str) + "\n")

        # Generate leaderboard using the export script
        from scripts.export_leaderboard import main as export_main
        export_main()

        logger.info("Leaderboard generated successfully")


def main():
    """Main entry point for model benchmarking."""
    import argparse

    parser = argparse.ArgumentParser(description="HumanEvalComm V2 Model Benchmarking")
    parser.add_argument(
        "--data",
        required=True,
        help="JSONL file with model solutions (format: {'model_name': str, 'code': str, 'test_code': str, 'problem_description': str, 'problem_id': str})"
    )
    parser.add_argument("--config", default="config.yaml", help="Configuration file")
    parser.add_argument("--output-dir", default=".", help="Output directory")

    args = parser.parse_args()

    # Change to output directory
    os.chdir(args.output_dir)

    # Load model data
    model_data = []
    with open(args.data, "r") as f:
        for line in f:
            if line.strip():
                model_data.append(json.loads(line))

    # Initialize benchmarker
    benchmarker = ModelBenchmarker(args.config)

    # Run benchmarking
    results = benchmarker.benchmark_models(model_data)

    # Generate leaderboard
    benchmarker.generate_leaderboard()

    print(f"Benchmarking completed for {len(model_data)} model solutions")
    print("Results saved to evaluation_results.jsonl")
    print("Leaderboard saved to results/leaderboard.csv")


if __name__ == "__main__":
    main()