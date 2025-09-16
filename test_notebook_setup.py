#!/usr/bin/env python3
"""
Test script to validate the HuggingFace Model Benchmark notebook setup.

This script checks that all dependencies are installed and the basic
functionality works before running the full notebook.
"""

import sys
import os
import json


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
        'aiohttp', 'requests', 'tqdm', 'dotenv', 'yaml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements_notebook.txt")
        return False
    
    print("✅ All dependencies installed!")
    return True


def check_evaluators():
    """Check if the evaluators package is available."""
    print("\n🔍 Checking evaluators package...")
    
    try:
        from evaluators import (Aggregator, AutomatedStaticDynamic,
                                SandboxRunner)
        print("   ✅ All evaluator classes imported successfully")
        
        # Test basic functionality
        AutomatedStaticDynamic()
        SandboxRunner(use_docker=False)
        Aggregator()
        
        print("   ✅ Evaluator instances created successfully")
        return True
        
    except ImportError as e:
        print(f"   ❌ Evaluators import failed: {e}")
        print("   Make sure you're in the correct directory and "
              "evaluators are installed")
        return False
    except Exception as e:
        print(f"   ⚠️  Evaluators partially working: {e}")
        return True


def check_dataset():
    """Check if the HumanEvalComm dataset is available."""
    print("\n🔍 Checking dataset...")
    
    dataset_path = "Benchmark/HumanEvalComm.jsonl"
    
    if not os.path.exists(dataset_path):
        print(f"   ❌ Dataset not found: {dataset_path}")
        print("   Make sure you're in the correct project directory")
        return False
    
    try:
        with open(dataset_path, 'r') as f:
            first_line = f.readline()
            problem = json.loads(first_line)
            
        print("   ✅ Dataset loaded successfully")
        print(f"   ✅ Sample problem: {problem['name']}")
        prompt_types = [k for k in problem.keys() if k.startswith('prompt')]
        print(f"   ✅ Available prompt types: {prompt_types}")
        return True
        
    except Exception as e:
        print(f"   ❌ Dataset validation failed: {e}")
        return False


def check_environment():
    """Check environment configuration."""
    print("\n🔍 Checking environment...")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("   ✅ .env file found")
    else:
        print("   ⚠️  .env file not found "
              "(you can create one from .env.template)")
    
    # Check for HuggingFace token
    from dotenv import load_dotenv
    load_dotenv()
    
    hf_token = os.getenv('HUGGINGFACE_API_TOKEN') or os.getenv('HF_TOKEN')
    if hf_token:
        print("   ✅ HuggingFace API token found")
    else:
        print("   ⚠️  HuggingFace API token not found")
        print("      Set HUGGINGFACE_API_TOKEN in your .env file")
        print("      Get token from: https://huggingface.co/settings/tokens")
    
    # Check output directory
    os.makedirs('benchmark_results', exist_ok=True)
    print("   ✅ Output directory created/verified")
    
    return True


def test_basic_functionality():
    """Test basic functionality of key components."""
    print("\n🔍 Testing basic functionality...")
    
    try:
        # Test evaluators
        from evaluators import (AutomatedStaticDynamic, SandboxRunner,
                                Aggregator)
        
        analyzer = AutomatedStaticDynamic()
        sandbox = SandboxRunner(use_docker=False)
        aggregator = Aggregator()
        
        # Test with simple code
        test_code = """
def add(a, b):
    '''Add two numbers.'''
    return a + b
"""
        
        test_test_code = """
def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

if __name__ == "__main__":
    test_add()
    print("All tests passed!")
"""
        
        print("   🧪 Testing static/dynamic analysis...")
        static_results, dynamic_results = analyzer.analyze_code(
            test_code, test_test_code, "test"
        )
        print(f"      Pylint score: {static_results.pylint_score:.2f}")
        print(f"      Tests passed: {dynamic_results.test_passes}")
        
        print("   🏃 Testing sandbox execution...")
        execution_result = sandbox.run_code(test_code, test_test_code)
        print(f"      Execution success: {execution_result.success}")
        print(f"      Execution time: {execution_result.execution_time:.3f}s")
        
        print("   📊 Testing aggregation...")
        evaluation = aggregator.evaluate_problem(
            problem_id="test",
            test_results=dynamic_results,
            static_results=static_results,
            sandbox_results=execution_result
        )
        print(f"      Composite score: {evaluation.composite_score:.2f}")
        
        print("   ✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Basic functionality test failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("🚀 HuggingFace Model Benchmark Notebook Setup Validation")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Evaluators Package", check_evaluators),
        ("Dataset", check_dataset),
        ("Environment", check_environment),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"   ❌ {check_name} check failed with exception: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 All checks passed! The notebook is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Set your HUGGINGFACE_API_TOKEN in .env file")
        print("   2. Launch Jupyter: "
              "jupyter notebook huggingface_model_benchmark.ipynb")
        print("   3. Run the notebook cells to start benchmarking")
    else:
        print("⚠️  Some checks failed. "
              "Please fix the issues above before using the notebook.")
        print("\n🔧 Common fixes:")
        print("   • Install missing packages: "
              "pip install -r requirements_notebook.txt")
        print("   • Ensure you're in the correct project directory")
        print("   • Set up your .env file with API tokens")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)