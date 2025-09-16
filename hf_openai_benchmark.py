#!/usr/bin/env python3
"""
HuggingFace Model Benchmarking using OpenAI Wrapper

This script demonstrates how to use HuggingFace's OpenAI-compatible API
to benchmark multiple models on the HumanEvalComm dataset.
"""

import os
import json
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Load local evaluators
from evaluators import (
    Aggregator, 
    AutomatedStaticDynamic, 
    SandboxRunner
)

# Load environment variables
load_dotenv()


@dataclass
class ModelConfig:
    """Configuration for a HuggingFace model using OpenAI wrapper."""
    name: str
    model_id: str  # Model ID for HuggingFace router
    max_tokens: int = 512
    temperature: float = 0.1
    description: str = ""
    provider: str = ""  # Optional provider specification


@dataclass
class EvaluationResult:
    """Results from evaluating a single problem with a model."""
    problem_id: str
    model_name: str
    prompt_type: str
    raw_response: str
    extracted_code: str
    is_question: bool
    
    # V2 Evaluator scores
    composite_score: float = 0.0
    test_pass_rate: float = 0.0
    static_analysis_score: float = 0.0
    security_score: float = 0.0
    
    # Communication metrics
    communication_rate: float = 0.0
    question_quality: float = 0.0
    
    # Execution metrics
    execution_success: bool = False
    execution_time: float = 0.0
    memory_usage: float = 0.0
    
    # Metadata
    timestamp: str = ""
    error_message: str = ""


class HuggingFaceBenchmark:
    """Main benchmarking class using HuggingFace OpenAI wrapper."""
    
    def __init__(self, hf_token: str):
        """Initialize the benchmark with HuggingFace token."""
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        
        # Initialize evaluators
        self.analyzer = AutomatedStaticDynamic()
        self.sandbox = SandboxRunner(use_docker=False)
        self.aggregator = Aggregator()
        
        print("✅ HuggingFace OpenAI client initialized")
        print("✅ V2 Evaluators initialized")
    
    def extract_code_from_response(self, response: str) -> str:
        """Extract code from model response."""
        import re
        
        # Look for code blocks
        code_pattern = re.compile(r'```(?:python)?\n?(.*?)\n?```', 
                                 re.DOTALL | re.IGNORECASE)
        matches = code_pattern.findall(response)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, check if response is mostly code
        lines = response.strip().split('\n')
        code_lines = [line for line in lines 
                     if line.strip().startswith(('def ', 'class ', 'import ', 
                                               'from ', '    '))]
        
        if len(code_lines) > len(lines) * 0.5:  # More than 50% code lines
            return response.strip()
        
        return ""
    
    def is_question(self, response: str) -> bool:
        """Check if response contains clarifying questions."""
        question_indicators = [
            '?', 'what', 'how', 'when', 'where', 'why', 'which', 'who',
            'could you', 'can you', 'please clarify', 'unclear', 'ambiguous',
            'need more', 'additional information', 'specify', 'clarification',
            'not clear', 'missing', 'incomplete'
        ]
        
        response_lower = response.lower()
        question_count = sum(1 for indicator in question_indicators 
                           if indicator in response_lower)
        
        # Consider it a question if multiple indicators or explicit question marks
        return question_count >= 2 or '?' in response
    
    async def generate_code(self, model_config: ModelConfig, prompt: str) -> Optional[str]:
        """Generate code using HuggingFace OpenAI wrapper."""
        try:
            # Construct model ID with provider if specified
            model_id = model_config.model_id
            if model_config.provider:
                model_id = f"{model_id}:{model_config.provider}"
            
            # Create the prompt message
            messages = [
                {
                    "role": "system",
                    "content": ("You are an expert software developer. "
                              "Generate Python code or ask clarifying questions "
                              "if the requirements are unclear.")
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Use asyncio to run the synchronous OpenAI call
            loop = asyncio.get_event_loop()
            completion = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    max_tokens=model_config.max_tokens,
                    temperature=model_config.temperature,
                    timeout=30
                )
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"   Error generating code: {e}")
            return None
    
    def generate_test_code(self, problem: Dict, code: str) -> str:
        """Generate test code from problem test cases."""
        if 'test_case' not in problem:
            return ""
        
        entry_point = problem.get('entry_point', 'candidate')
        test_cases = problem['test_case']
        
        test_code = f"""
# Test code for {problem['name']}
{code}

def test_solution():
    \"\"\"Test the generated solution.\"\"\"
    try:
"""
        
        for i, test_case in enumerate(test_cases[:3]):  # Limit to 3 test cases
            input_val = test_case['input']
            expected = test_case['output']
            relation = test_case.get('relation', '==')
            
            if relation == '==':
                test_code += f"""
        # Test case {i+1}
        result_{i} = {entry_point}({input_val})
        assert result_{i} == {expected}, f"Test {i+1} failed: expected {expected}, got {{result_{i}}}"
"""
        
        test_code += """
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    test_solution()
"""
        
        return test_code
    
    async def evaluate_problem(self, problem: Dict, model_config: ModelConfig, 
                             prompt_type: str = 'prompt') -> EvaluationResult:
        """Evaluate a single problem with a specific model."""
        result = EvaluationResult(
            problem_id=problem['name'],
            model_name=model_config.name,
            prompt_type=prompt_type,
            raw_response="",
            extracted_code="",
            is_question=False,
            timestamp=datetime.now().isoformat()
        )
        
        try:
            # Get the prompt
            if prompt_type not in problem:
                result.error_message = f"Prompt type '{prompt_type}' not found"
                return result
            
            prompt = problem[prompt_type]
            
            # Generate response
            response = await self.generate_code(model_config, prompt)
            
            if response is None:
                result.error_message = "Failed to generate response"
                return result
            
            result.raw_response = response
            result.is_question = self.is_question(response)
            result.communication_rate = 1.0 if result.is_question else 0.0
            
            # Extract and evaluate code
            if not result.is_question:
                result.extracted_code = self.extract_code_from_response(response)
                
                if result.extracted_code:
                    await self.evaluate_code(result, problem)
            else:
                # Simple question quality scoring
                result.question_quality = self.evaluate_questions(response)
        
        except Exception as e:
            result.error_message = str(e)
            print(f"❌ Error evaluating {problem['name']} with {model_config.name}: {e}")
        
        return result
    
    async def evaluate_code(self, result: EvaluationResult, problem: Dict):
        """Evaluate generated code using V2 evaluators."""
        try:
            # Create test code
            test_code = self.generate_test_code(problem, result.extracted_code)
            
            # Run static and dynamic analysis
            static_results, dynamic_results = self.analyzer.analyze_code(
                result.extracted_code, test_code, result.problem_id
            )
            
            # Run in sandbox
            execution_result = self.sandbox.run_code(result.extracted_code, test_code)
            
            result.execution_success = execution_result.success
            result.execution_time = execution_result.execution_time
            result.memory_usage = execution_result.memory_used
            
            # Aggregate results
            evaluation = self.aggregator.evaluate_problem(
                problem_id=result.problem_id,
                test_results=dynamic_results,
                static_results=static_results,
                sandbox_results=execution_result
            )
            
            # Update result with scores
            result.composite_score = evaluation.composite_score
            result.test_pass_rate = evaluation.test_pass_rate_score
            result.static_analysis_score = evaluation.static_analysis_score
            result.security_score = evaluation.security_score
            
        except Exception as e:
            result.error_message = f"Code evaluation failed: {e}"
    
    def evaluate_questions(self, questions: str) -> float:
        """Simple heuristic evaluation of question quality."""
        question_count = questions.lower().count('?')
        relevant_keywords = ['clarify', 'unclear', 'ambiguous', 'specify', 'missing']
        keyword_count = sum(1 for keyword in relevant_keywords 
                          if keyword in questions.lower())
        
        # Simple scoring: more questions and relevant keywords = higher quality
        return min(1.0, (question_count * 0.3 + keyword_count * 0.2))
    
    async def benchmark_models(self, problems: List[Dict], 
                             models: Dict[str, ModelConfig],
                             prompt_types: List[str]) -> List[EvaluationResult]:
        """Benchmark multiple models on multiple problems."""
        results = []
        total_evaluations = len(problems) * len(models) * len(prompt_types)
        
        print(f"🚀 Starting benchmark: {total_evaluations} total evaluations")
        print(f"   Models: {list(models.keys())}")
        print(f"   Prompt types: {prompt_types}")
        print(f"   Problems: {len(problems)}")
        
        with tqdm(total=total_evaluations, desc="Evaluating") as pbar:
            for problem in problems:
                for model_key, model_config in models.items():
                    for prompt_type in prompt_types:
                        # Skip if prompt type doesn't exist for this problem
                        if prompt_type not in problem:
                            pbar.update(1)
                            continue
                        
                        pbar.set_description(
                            f"Evaluating {model_config.name} on "
                            f"{problem['name']} ({prompt_type})"
                        )
                        
                        result = await self.evaluate_problem(
                            problem, model_config, prompt_type
                        )
                        results.append(result)
                        
                        pbar.update(1)
                        
                        # Small delay to avoid rate limiting
                        await asyncio.sleep(0.1)
        
        print(f"✅ Benchmark completed! {len(results)} results generated.")
        return results


def load_problems(dataset_path: str = "Benchmark/HumanEvalComm.jsonl", 
                 max_problems: int = -1) -> List[Dict]:
    """Load HumanEvalComm dataset."""
    problems = []
    
    try:
        with open(dataset_path, 'r') as f:
            for i, line in enumerate(f):
                if max_problems > 0 and i >= max_problems:
                    break
                problems.append(json.loads(line.strip()))
                
        print(f"📚 Loaded {len(problems)} problems from {dataset_path}")
        return problems
        
    except FileNotFoundError:
        print(f"❌ Dataset file not found: {dataset_path}")
        return []
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return []


def create_results_dataframe(results: List[EvaluationResult]) -> pd.DataFrame:
    """Convert evaluation results to pandas DataFrame."""
    data = []
    for result in results:
        data.append({
            'problem_id': result.problem_id,
            'model_name': result.model_name,
            'prompt_type': result.prompt_type,
            'is_question': result.is_question,
            'communication_rate': result.communication_rate,
            'question_quality': result.question_quality,
            'composite_score': result.composite_score,
            'test_pass_rate': result.test_pass_rate,
            'static_analysis_score': result.static_analysis_score,
            'security_score': result.security_score,
            'execution_success': result.execution_success,
            'execution_time': result.execution_time,
            'memory_usage': result.memory_usage,
            'has_error': bool(result.error_message),
            'code_length': len(result.extracted_code),
            'response_length': len(result.raw_response)
        })
    
    return pd.DataFrame(data)


def export_results(df: pd.DataFrame, results: List[EvaluationResult], 
                  output_dir: str = 'benchmark_results'):
    """Export benchmark results in multiple formats."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Export DataFrame to CSV
    csv_path = f"{output_dir}/hf_benchmark_results_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    print(f"📊 Results exported to CSV: {csv_path}")
    
    # Export detailed results to JSON
    json_path = f"{output_dir}/hf_detailed_results_{timestamp}.json"
    detailed_results = [asdict(result) for result in results]
    with open(json_path, 'w') as f:
        json.dump(detailed_results, f, indent=2, default=str)
    print(f"📋 Detailed results exported to JSON: {json_path}")
    
    # Generate summary report
    report_path = f"{output_dir}/hf_benchmark_report_{timestamp}.md"
    generate_summary_report(df, report_path)
    print(f"📄 Summary report generated: {report_path}")
    
    return {
        'csv': csv_path,
        'json': json_path,
        'report': report_path
    }


def generate_summary_report(df: pd.DataFrame, output_path: str):
    """Generate a comprehensive markdown report."""
    with open(output_path, 'w') as f:
        f.write("# HuggingFace Model Benchmark Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Evaluations:** {len(df)}\n")
        f.write(f"- **Models Tested:** {df['model_name'].nunique()}\n")
        f.write(f"- **Problems Evaluated:** {df['problem_id'].nunique()}\n")
        f.write(f"- **Prompt Types:** {df['prompt_type'].nunique()}\n\n")
        
        # Model Rankings
        f.write("## Model Rankings\n\n")
        model_scores = df.groupby('model_name')['composite_score'].mean().sort_values(ascending=False)
        
        f.write("### Overall Performance (Composite Score)\n\n")
        for i, (model, score) in enumerate(model_scores.items(), 1):
            f.write(f"{i}. **{model}**: {score:.3f}\n")
        
        # Communication Analysis
        f.write("\n### Communication Capabilities\n\n")
        comm_rates = df.groupby('model_name')['communication_rate'].mean().sort_values(ascending=False)
        
        for model, rate in comm_rates.items():
            f.write(f"- **{model}**: {rate:.3f} communication rate\n")
        
        # Performance by prompt type
        f.write("\n### Performance by Prompt Type\n\n")
        prompt_analysis = df.groupby(['prompt_type', 'model_name'])['composite_score'].mean().unstack()
        f.write(prompt_analysis.to_markdown())


async def main():
    """Main function to run the benchmark."""
    print("🚀 HuggingFace Model Benchmark with OpenAI Wrapper")
    print("=" * 60)
    
    # Check for HuggingFace token
    hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_API_TOKEN')
    if not hf_token:
        print("❌ No HuggingFace API token found!")
        print("   Please set HF_TOKEN in your .env file")
        return
    
    # Define models to test
    models = {
        'codellama-7b': ModelConfig(
            name="CodeLlama-7B-Instruct",
            model_id="meta-llama/CodeLlama-7b-Instruct-hf",
            description="Meta's CodeLlama 7B parameter instruction-tuned model"
        ),
        'llama3-8b': ModelConfig(
            name="Llama-3.1-8B-Instruct",
            model_id="meta-llama/Llama-3.1-8B-Instruct",
            description="Meta's Llama 3.1 8B instruction model",
            provider="cerebras"  # Fast inference provider
        ),
        'deepseek-coder': ModelConfig(
            name="DeepSeek-Coder-6.7B-Instruct",
            model_id="deepseek-ai/deepseek-coder-6.7b-instruct",
            description="DeepSeek's code generation model"
        )
    }
    
    # Load problems
    problems = load_problems(max_problems=5)  # Start with 5 problems
    if not problems:
        print("❌ No problems loaded!")
        return
    
    # Initialize benchmark
    benchmark = HuggingFaceBenchmark(hf_token)
    
    # Define prompt types to test
    prompt_types = ['prompt', 'prompt1a', 'prompt1c', 'prompt1p']
    
    # Run benchmark
    print(f"\n🎯 Running benchmark...")
    start_time = time.time()
    
    results = await benchmark.benchmark_models(problems, models, prompt_types)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Benchmark completed in {duration:.2f} seconds")
    print(f"📊 Generated {len(results)} evaluation results")
    
    # Create DataFrame and analyze results
    df = create_results_dataframe(results)
    
    # Display summary statistics
    print(f"\n📈 Summary Statistics:")
    print(f"   Successful evaluations: {len([r for r in results if not r.error_message])}")
    print(f"   Failed evaluations: {len([r for r in results if r.error_message])}")
    
    # Model performance summary
    print(f"\n🏆 Model Performance Summary:")
    model_summary = df.groupby('model_name').agg({
        'composite_score': 'mean',
        'communication_rate': 'mean',
        'execution_success': 'mean'
    }).round(3)
    print(model_summary)
    
    # Export results
    export_paths = export_results(df, results)
    print(f"\n📁 Results exported to: benchmark_results/")
    
    print(f"\n🎉 Benchmark completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())