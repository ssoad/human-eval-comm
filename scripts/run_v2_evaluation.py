#!/usr/bin/env python3
"""
V2 Evaluation Framework Runner

Comprehensive evaluation pipeline with advanced features:
- Multi-LLM judging with human calibration
- Property-based fuzzing with Hypothesis
- Enhanced aggregation with configurable formulas
- Dashboard and reporting
- Safety measures and reproducibility
"""

import logging
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add evaluators to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from evaluators.aggregator import Aggregator
from evaluators.automated_static_dynamic import AutomatedStaticDynamic
from evaluators.multi_llm_judge import MultiLLMJudge
from evaluators.sandbox_runner import SandboxRunner
from evaluators.hypothesis_fuzzer import HypothesisFuzzer
from evaluators.human_calibration import HumanCalibrationSystem
from evaluators.enhanced_aggregator import EnhancedAggregator
from evaluators.dashboard import EvaluationDashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('v2_evaluation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class V2EvaluationPipeline:
    """Complete V2 evaluation pipeline."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the V2 evaluation pipeline."""
        logger.info("Initializing V2 Evaluation Pipeline...")

        # Core components
        self.analyzer = AutomatedStaticDynamic()
        self.sandbox = SandboxRunner(use_docker=False)  # Use subprocess for compatibility
        self.llm_judge = MultiLLMJudge(config_path)
        self.aggregator = Aggregator()

        # V2 Advanced components
        self.hypothesis_fuzzer = HypothesisFuzzer()
        self.calibration_system = HumanCalibrationSystem()
        self.enhanced_aggregator = EnhancedAggregator()
        self.dashboard = EvaluationDashboard()

        # Results storage
        self.results = []
        self.v2_results = []

        logger.info("V2 Evaluation Pipeline initialized successfully")

    def evaluate_single_problem(self, code: str, test_code: str,
                              problem_description: str,
                              problem_id: str = "unknown") -> Dict[str, Any]:
        """Evaluate a single problem using the complete V2 pipeline."""

        logger.info(f"Evaluating problem: {problem_id}")
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
                # Run async LLM evaluation
                import asyncio
                llm_scores = asyncio.run(self.llm_judge.evaluate_code(code, problem_description))
            except Exception as e:
                logger.warning(f"LLM evaluation failed: {e}")
                llm_scores = None

            # 4. Hypothesis Fuzzing (V2 Feature)
            logger.info("Running hypothesis fuzzing...")
            hypothesis_results = self.hypothesis_fuzzer.run_hypothesis_tests(
                code, test_code, self._extract_function_name(code)
            )

            # 5. Standard Aggregation
            logger.info("Running standard aggregation...")
            standard_result = self.aggregator.evaluate_problem(
                problem_id=problem_id,
                test_results=dynamic_results,
                static_results=static_results,
                sandbox_results=sandbox_results,
                llm_scores=llm_scores
            )

            # 6. Enhanced Aggregation (V2 Feature)
            logger.info("Running enhanced aggregation...")
            evaluation_data = {
                'problem_id': problem_id,
                'static_results': static_results.__dict__ if hasattr(static_results, '__dict__') else static_results,
                'dynamic_results': dynamic_results.__dict__ if hasattr(dynamic_results, '__dict__') else dynamic_results,
                'sandbox_results': sandbox_results.__dict__ if hasattr(sandbox_results, '__dict__') else sandbox_results,
                'llm_scores': llm_scores.__dict__ if llm_scores and hasattr(llm_scores, '__dict__') else self._convert_llm_scores(llm_scores),
                'hypothesis_results': hypothesis_results.__dict__ if hasattr(hypothesis_results, '__dict__') else hypothesis_results
            }

            enhanced_result = self.enhanced_aggregator.aggregate_results(evaluation_data)

            # 7. Store Results
            result_record = {
                'timestamp': datetime.now().isoformat(),
                'problem_id': problem_id,
                'model_name': 'V2_Evaluation_Framework',  # Add model name for dashboard
                'code_length': len(code),
                'test_code_length': len(test_code),

                # Standard results
                'standard_composite_score': standard_result.composite_score,
                'standard_weighted_score': standard_result.weighted_composite_score,

                # Enhanced results (V2)
                'v2_composite_score': enhanced_result.composite_score,
                'v2_weighted_score': enhanced_result.weighted_composite_score,
                'v2_formula_used': enhanced_result.formula_used,
                'v2_penalties_applied': enhanced_result.penalties_applied,
                'v2_bonuses_applied': enhanced_result.bonuses_applied,

                # Component scores
                'static_analysis_score': static_results.pylint_score if hasattr(static_results, 'pylint_score') else 0,
                'security_score': static_results.security_score if hasattr(static_results, 'security_score') else 0,
                'test_pass_rate': dynamic_results.test_passes if hasattr(dynamic_results, 'test_passes') else 0,
                'llm_consensus_score': llm_scores.consensus_score if llm_scores else 0,

                # V2 Features
                'hypothesis_tests_run': hypothesis_results.tests_run,
                'hypothesis_coverage_improvement': hypothesis_results.coverage_improvement,

                # Execution details
                'execution_success': sandbox_results.success,
                'execution_time': sandbox_results.execution_time,
                'memory_used': sandbox_results.memory_used,

                # Metadata
                'environment': {
                    'python_version': sys.version,
                    'platform': sys.platform,
                    'evaluation_version': 'V2'
                }
            }

            self.results.append(result_record)
            self.v2_results.append(enhanced_result)

            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Evaluation completed in {execution_time:.2f}s")
            return result_record

        except Exception as e:
            logger.error(f"Evaluation failed for {problem_id}: {e}")
            return {
                'problem_id': problem_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _extract_function_name(self, code: str) -> str:
        """Extract main function name from code."""
        import re
        match = re.search(r'def\s+(\w+)\s*\(', code)
        return match.group(1) if match else "unknown_function"

    def _convert_llm_scores(self, llm_scores) -> Dict[str, Any]:
        """Convert LLM scores to JSON-serializable format."""
        if not llm_scores:
            return {}

        result = {}
        if hasattr(llm_scores, '__dict__'):
            for key, value in llm_scores.__dict__.items():
                if hasattr(value, '__dict__'):
                    # Handle nested objects like JudgeResponse
                    result[key] = {}
                    for sub_key, sub_value in value.__dict__.items():
                        result[key][sub_key] = sub_value
                elif isinstance(value, list):
                    # Handle lists of objects
                    result[key] = []
                    for item in value:
                        if hasattr(item, '__dict__'):
                            result[key].append(item.__dict__)
                        else:
                            result[key].append(item)
                else:
                    result[key] = value
        else:
            result = llm_scores if isinstance(llm_scores, dict) else {}

        return result

    def evaluate_multiple_problems(self, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluate multiple problems."""
        results = []

        for problem in problems:
            result = self.evaluate_single_problem(
                code=problem['code'],
                test_code=problem.get('test_code', ''),
                problem_description=problem.get('description', ''),
                problem_id=problem.get('problem_id', f"problem_{len(results)}")
            )
            results.append(result)

        return results

    def generate_reports(self):
        """Generate comprehensive reports."""
        logger.info("Generating evaluation reports...")

        # Save raw results
        self._save_results()

        # Generate dashboard
        self._generate_dashboard()

        # Generate performance report
        self._generate_performance_report()

        # Generate calibration data if available
        self._generate_calibration_data()

        logger.info("Reports generated successfully")

    def _save_results(self):
        """Save evaluation results to files."""
        # Save standard results
        with open('evaluation_results.jsonl', 'w') as f:
            for result in self.results:
                f.write(json.dumps(result, default=str) + '\n')

        # Save V2 enhanced results
        with open('v2_evaluation_results.jsonl', 'w') as f:
            for result in self.v2_results:
                # Convert to dict and handle nested objects
                result_dict = result.__dict__ if hasattr(result, '__dict__') else result
                if isinstance(result_dict, dict):
                    # Handle nested JudgeResponse objects
                    if 'judge_responses' in result_dict and result_dict['judge_responses']:
                        judge_responses = []
                        for jr in result_dict['judge_responses']:
                            if hasattr(jr, '__dict__'):
                                judge_responses.append(jr.__dict__)
                            else:
                                judge_responses.append(jr)
                        result_dict['judge_responses'] = judge_responses
                f.write(json.dumps(result_dict, default=str) + '\n')

        logger.info(f"Saved {len(self.results)} evaluation results")

    def _generate_dashboard(self):
        """Generate HTML dashboard."""
        # Dashboard expects results in results/ directory, so copy or use correct path
        import shutil
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        # Copy the results file to the expected location
        source_file = 'evaluation_results.jsonl'
        dest_file = os.path.join(results_dir, 'evaluation_results.jsonl')

        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            logger.info(f"Copied results to {dest_file}")

        self.dashboard.load_results('evaluation_results.jsonl')
        dashboard_path = self.dashboard.export_dashboard_html()
        if dashboard_path:
            logger.info(f"Dashboard generated: {dashboard_path}")

    def _generate_performance_report(self):
        """Generate performance report."""
        report = self.dashboard.generate_performance_report()

        with open('v2_performance_report.txt', 'w') as f:
            f.write(report)

        logger.info("Performance report generated")

    def _generate_calibration_data(self):
        """Generate calibration data for human annotation."""
        if not self.results:
            return

        # Generate annotation candidates based on disagreements
        candidates = self.calibration_system.generate_annotation_candidates(
            self.results, strategy="disagreement"
        )

        if candidates:
            csv_path = self.calibration_system.export_annotation_csv(candidates)
            logger.info(f"Calibration data exported: {csv_path}")

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of the evaluation."""
        if not self.results:
            return {"status": "no_results"}

        successful_evaluations = [r for r in self.results if 'error' not in r]

        return {
            "total_problems": len(self.results),
            "successful_evaluations": len(successful_evaluations),
            "average_v2_score": round(sum(r.get('v2_composite_score', 0) for r in successful_evaluations) / len(successful_evaluations), 3) if successful_evaluations else 0,
            "average_execution_time": round(sum(r.get('execution_time', 0) for r in successful_evaluations) / len(successful_evaluations), 2) if successful_evaluations else 0,
            "llm_evaluation_success_rate": round(sum(1 for r in successful_evaluations if r.get('llm_consensus_score', 0) > 0) / len(successful_evaluations), 3) if successful_evaluations else 0,
            "hypothesis_tests_average": round(sum(r.get('hypothesis_tests_run', 0) for r in successful_evaluations) / len(successful_evaluations), 1) if successful_evaluations else 0
        }


def main():
    """Main entry point for V2 evaluation."""
    import argparse

    parser = argparse.ArgumentParser(description="V2 Evaluation Framework")
    parser.add_argument("--config", default="config.yaml", help="Configuration file")
    parser.add_argument("--code", help="Code to evaluate")
    parser.add_argument("--test-code", help="Test code")
    parser.add_argument("--description", help="Problem description")
    parser.add_argument("--problem-id", default="test_problem", help="Problem ID")
    parser.add_argument("--batch-file", help="JSON file with multiple problems to evaluate")
    parser.add_argument("--output-dir", default=".", help="Output directory")

    args = parser.parse_args()

    # Change to output directory
    os.chdir(args.output_dir)

    # Initialize pipeline
    pipeline = V2EvaluationPipeline(args.config)

    try:
        if args.batch_file:
            # Batch evaluation
            logger.info(f"Loading batch file: {args.batch_file}")
            with open(args.batch_file, 'r') as f:
                problems = json.load(f)

            results = pipeline.evaluate_multiple_problems(problems)
            logger.info(f"Evaluated {len(results)} problems")

        elif args.code:
            # Single problem evaluation
            result = pipeline.evaluate_single_problem(
                code=args.code,
                test_code=args.test_code or "",
                problem_description=args.description or "",
                problem_id=args.problem_id
            )
            logger.info(f"Evaluation completed for {args.problem_id}")

        else:
            # Default: evaluate the Fibonacci example
            logger.info("Running default Fibonacci example...")

            code = """
def fibonacci(n):
    '''Calculate the nth Fibonacci number.'''
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

            test_code = """
import sys
sys.path.insert(0, '/tmp')

def test_fibonacci():
    '''Test basic fibonacci functionality.'''
    from solution import fibonacci

    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55

def test_fibonacci_edge_cases():
    '''Test edge cases for fibonacci.'''
    from solution import fibonacci

    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    # Test negative input (should raise ValueError)
    try:
        fibonacci(-1)
        assert False, "Should have raised ValueError for negative input"
    except ValueError:
        pass  # Expected behavior

if __name__ == "__main__":
    test_fibonacci()
    test_fibonacci_edge_cases()
    print("All tests passed!")
"""

            result = pipeline.evaluate_single_problem(
                code=code,
                test_code=test_code,
                problem_description="Implement a function to calculate Fibonacci numbers with proper error handling",
                problem_id="fibonacci_example"
            )

        # Generate reports
        pipeline.generate_reports()

        # Print summary
        stats = pipeline.get_summary_stats()
        print("\n" + "="*60)
        print("V2 EVALUATION SUMMARY")
        print("="*60)
        print(f"Total Problems: {stats['total_problems']}")
        print(f"Successful Evaluations: {stats['successful_evaluations']}")
        print(f"Average V2 Score: {stats['average_v2_score']:.3f}")
        print(f"Average Execution Time: {stats['average_execution_time']:.2f}s")
        print(f"LLM Success Rate: {stats['llm_evaluation_success_rate']:.1%}")
        print(f"Average Hypothesis Tests: {stats['hypothesis_tests_average']:.1f}")
        print("\nReports generated:")
        print("- evaluation_results.jsonl")
        print("- v2_evaluation_results.jsonl")
        print("- dashboard.html")
        print("- v2_performance_report.txt")

    except Exception as e:
        logger.error(f"V2 evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()