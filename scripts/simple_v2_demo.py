#!/usr/bin/env python3
"""
Simple V2 Evaluation Framework Demo

Demonstrates the core V2 evaluation features without complex serialization issues.
"""

import logging
import os
import sys
from datetime import datetime

# Add evaluators to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from evaluators.aggregator import Aggregator
from evaluators.automated_static_dynamic import AutomatedStaticDynamic
from evaluators.multi_llm_judge import MultiLLMJudge
from evaluators.sandbox_runner import SandboxRunner
from evaluators.hypothesis_fuzzer import HypothesisFuzzer
from evaluators.enhanced_aggregator import EnhancedAggregator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Run a simple V2 evaluation demo."""
    print("🚀 V2 Evaluation Framework Demo")
    print("=" * 50)

    # Initialize components
    print("\n📦 Initializing components...")
    analyzer = AutomatedStaticDynamic()
    sandbox = SandboxRunner(use_docker=False)
    aggregator = Aggregator()
    hypothesis_fuzzer = HypothesisFuzzer()
    enhanced_aggregator = EnhancedAggregator()

    # Try to initialize LLM judge (may fail without API keys)
    llm_judge = None
    try:
        llm_judge = MultiLLMJudge()
        print("✅ LLM Judge initialized")
    except Exception as e:
        print(f"⚠️  LLM Judge initialization failed: {e}")
        print("   (LLM evaluation will be skipped)")

    # Sample Fibonacci code
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
def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55

def test_fibonacci_edge_cases():
    try:
        fibonacci(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

if __name__ == "__main__":
    test_fibonacci()
    test_fibonacci_edge_cases()
    print("All tests passed!")
"""

    print("\n🔬 Running V2 Evaluation Pipeline...")
    print("-" * 40)

    start_time = datetime.now()

    try:
        # 1. Static Analysis
        print("1️⃣  Static Analysis...")
        static_results, dynamic_results = analyzer.analyze_code(
            code, test_code, "fibonacci_demo"
        )
        print("   ✅ Pylint Score: {:.2f}/10".format(static_results.pylint_score))
        print("   ✅ Security Score: {:.2f}/10".format(static_results.security_score))

        # 2. Dynamic Analysis (Sandbox)
        print("\n2️⃣  Sandbox Execution...")
        sandbox_results = sandbox.run_code(code, test_code)
        print("   ✅ Execution: {}".format("Success" if sandbox_results.success else "Failed"))
        print("   ✅ Execution Time: {:.2f}s".format(sandbox_results.execution_time))
        print("   ✅ Memory Used: {:.2f}MB".format(sandbox_results.memory_used))

        # 3. LLM Evaluation (if available)
        llm_scores = None
        if llm_judge:
            print("\n3️⃣  LLM Evaluation...")
            try:
                import asyncio
                llm_scores = asyncio.run(llm_judge.evaluate_code(
                    code, "Implement a function to calculate Fibonacci numbers with proper error handling"
                ))
                print("   ✅ LLM Consensus Score: {:.2f}/10".format(llm_scores.consensus_score))
            except Exception as e:
                print(f"   ⚠️  LLM evaluation failed: {e}")
        else:
            print("\n3️⃣  LLM Evaluation... Skipped (no API keys)")

        # 4. Hypothesis Fuzzing (V2 Feature)
        print("\n4️⃣  Hypothesis Fuzzing (V2)...")
        hypothesis_results = hypothesis_fuzzer.run_hypothesis_tests(
            code, test_code, "fibonacci"
        )
        print("   ✅ Tests Run: {}".format(hypothesis_results.tests_run))
        print("   ✅ Coverage Improvement: {:.1f}%".format(hypothesis_results.coverage_improvement))

        # 5. Standard Aggregation
        print("\n5️⃣  Standard Aggregation...")
        standard_result = aggregator.evaluate_problem(
            problem_id="fibonacci_demo",
            test_results=dynamic_results,
            static_results=static_results,
            sandbox_results=sandbox_results,
            llm_scores=llm_scores
        )
        print("   ✅ Composite Score: {:.2f}/10".format(standard_result.composite_score))

        # 6. Enhanced Aggregation (V2 Feature)
        print("\n6️⃣  Enhanced Aggregation (V2)...")
        evaluation_data = {
            'problem_id': 'fibonacci_demo',
            'static_results': static_results.__dict__ if hasattr(static_results, '__dict__') else {},
            'dynamic_results': dynamic_results.__dict__ if hasattr(dynamic_results, '__dict__') else {},
            'sandbox_results': sandbox_results.__dict__ if hasattr(sandbox_results, '__dict__') else {},
            'llm_scores': llm_scores.__dict__ if llm_scores and hasattr(llm_scores, '__dict__') else {},
            'hypothesis_results': hypothesis_results.__dict__ if hasattr(hypothesis_results, '__dict__') else {}
        }

        enhanced_result = enhanced_aggregator.aggregate_results(evaluation_data)
        print("   ✅ V2 Composite Score: {:.2f}/10".format(enhanced_result.composite_score))
        print("   ✅ V2 Weighted Score: {:.2f}/10".format(enhanced_result.weighted_composite_score))
        print("   ✅ Formula Used: {}".format(enhanced_result.formula_used))

        if enhanced_result.penalties_applied:
            print("   ℹ️  Penalties Applied: {}".format(list(enhanced_result.penalties_applied.keys())))

        if enhanced_result.bonuses_applied:
            print("   ℹ️  Bonuses Applied: {}".format(list(enhanced_result.bonuses_applied.keys())))

        # Summary
        execution_time = (datetime.now() - start_time).total_seconds()

        print("\n" + "=" * 50)
        print("🎉 V2 EVALUATION COMPLETE")
        print("=" * 50)
        print("📊 Results Summary:")
        print("   • Standard Score: {:.2f}/10".format(standard_result.composite_score))
        print("   • V2 Enhanced Score: {:.2f}/10".format(enhanced_result.composite_score))
        print("   • Execution Time: {:.2f}s".format(execution_time))
        print("   • Tests Passed: {}".format(dynamic_results.test_passes if hasattr(dynamic_results, 'test_passes') else 'N/A'))
        print("   • Hypothesis Tests: {}".format(hypothesis_results.tests_run))

        print("\n🚀 V2 Features Demonstrated:")
        print("   ✅ Enhanced aggregation with configurable formulas")
        print("   ✅ Property-based fuzzing with Hypothesis")
        print("   ✅ Human-calibration ready system")
        print("   ✅ Advanced scoring with penalties/bonuses")
        print("   ✅ Comprehensive evaluation pipeline")

        if llm_scores:
            print("   ✅ Multi-LLM judging with consensus")
        else:
            print("   ⚠️  Multi-LLM judging (requires API keys)")

        print("\n📈 Next Steps:")
        print("   • Add API keys for LLM evaluation")
        print("   • Try different scoring formulas")
        print("   • Run batch evaluations")
        print("   • Generate calibration data")

    except Exception as e:
        logger.error(f"V2 evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()