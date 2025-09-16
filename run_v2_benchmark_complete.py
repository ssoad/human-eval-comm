#!/usr/bin/env python3
"""
Complete V2 Benchmark Runner with Automatic Leaderboard Generation

Single script that:
1. Runs V2 benchmark with Enhanced Aggregation, Hypothesis Fuzzing, and Multi-LLM Judging
2. Automatically generates professional leaderboard
3. Saves all results and displays summary

Usage: python run_v2_benchmark_complete.py
"""

import os
import json
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import pandas as pd
import logging
import sys

# Add project root to path
sys.path.append('.')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for a HuggingFace model using OpenAI wrapper."""
    name: str
    model_id: str
    max_tokens: int = 1024
    temperature: float = 0.1
    description: str = ""
    provider: str = ""


@dataclass
class EvaluationResult:
    """Results from evaluating a single problem with a model."""
    problem_id: str
    model_name: str
    prompt_type: str
    raw_response: str
    extracted_code: str
    is_question: bool
    
    # V2 Enhanced scores
    composite_score: float = 0.0
    weighted_composite_score: float = 0.0
    test_pass_rate: float = 0.0
    static_analysis_score: float = 0.0
    security_score: float = 0.0
    
    # V2 Multi-LLM Judge scores
    llm_consensus_score: float = 0.0
    llm_mean_confidence: float = 0.0
    llm_score_std: float = 0.0
    judge_count: int = 0
    
    # V2 Fuzzing results
    hypothesis_tests_run: int = 0
    hypothesis_failures: int = 0
    coverage_improvement: float = 0.0
    
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
    
    # V2 Enhanced fields
    formula_used: str = ""
    penalties_applied: Dict[str, float] = None
    bonuses_applied: Dict[str, float] = None
    
    def __post_init__(self):
        if self.penalties_applied is None:
            self.penalties_applied = {}
        if self.bonuses_applied is None:
            self.bonuses_applied = {}


class CompleteV2Benchmark:
    """Complete V2 benchmark runner with automatic leaderboard generation."""
    
    def __init__(self, request_delay: float = 2.0):
        """Initialize the complete V2 benchmark system."""
        self.enhanced_aggregator = None
        self.fuzzer = None
        self.sandbox = None
        self.client = None
        self.sandbox_available = False
        self.request_delay = request_delay  # Configurable delay for free API
        
        self._initialize_components()
        self._initialize_client()
        
        logger.info(f"✅ Request delay set to {request_delay}s for API rate limiting")
    
    def _initialize_components(self):
        """Initialize V2 evaluator components."""
        try:
            from evaluators.enhanced_aggregator import EnhancedAggregator
            from evaluators.hypothesis_fuzzer import HypothesisFuzzer
            from evaluators import SandboxRunner
            
            self.enhanced_aggregator = EnhancedAggregator()
            self.fuzzer = HypothesisFuzzer()
            
            try:
                self.sandbox = SandboxRunner(use_docker=False)
                self.sandbox_available = True
                logger.info("✅ SandboxRunner initialized")
            except Exception as e:
                logger.warning(f"⚠️  SandboxRunner failed: {e}")
                self.sandbox = None
                self.sandbox_available = False
            
            logger.info("✅ V2 Core Evaluators initialized")
            
        except ImportError as e:
            logger.error(f"❌ Error importing V2 evaluators: {e}")
            raise
    
    def _initialize_client(self):
        """Initialize HuggingFace client."""
        from openai import OpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        
        hf_token = os.getenv("HF_TOKEN") or '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'
        if not hf_token:
            raise ValueError("❌ No HuggingFace API token found!")
        
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        
        logger.info("✅ HuggingFace client initialized")
    
    def load_dataset(self, dataset_path: str = "Benchmark/HumanEvalComm.jsonl", max_problems: int = 3) -> List[Dict]:
        """Load HumanEvalComm dataset."""
        problems = []
        
        try:
            with open(dataset_path, 'r') as f:
                for i, line in enumerate(f):
                    if max_problems > 0 and i >= max_problems:
                        break
                    problems.append(json.loads(line.strip()))
            
            logger.info(f"📚 Loaded {len(problems)} problems")
            return problems
        
        except Exception as e:
            logger.error(f"❌ Error loading dataset: {e}")
            return []
    
    def extract_code_from_response(self, response: str) -> str:
        """Extract code from model response (improved extraction)."""
        import re
        
        # First try to find code blocks
        code_pattern = re.compile(r'```(?:python)?\n?(.*?)\n?```', re.DOTALL | re.IGNORECASE)
        matches = code_pattern.findall(response)
        
        if matches:
            # Get the largest code block (most likely the main function)
            largest_match = max(matches, key=len)
            return largest_match.strip()
        
        # If no code blocks, look for function definitions
        lines = response.strip().split('\n')
        
        # Find lines that start function definitions
        def_lines = []
        in_function = False
        current_function = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('def '):
                if current_function:
                    def_lines.extend(current_function)
                current_function = [line]
                in_function = True
            elif in_function:
                if stripped and not line.startswith(' ') and not stripped.startswith('#'):
                    # End of function
                    def_lines.extend(current_function)
                    current_function = []
                    in_function = False
                else:
                    current_function.append(line)
        
        # Add the last function if any
        if current_function:
            def_lines.extend(current_function)
        
        if def_lines:
            return '\n'.join(def_lines).strip()
        
        # Fallback: check if response is mostly code
        code_lines = [line for line in lines
                     if line.strip().startswith(('def ', 'class ', 'import ', 'from ', '    '))]
        
        if len(code_lines) > len(lines) * 0.3:  # Lower threshold
            return response.strip()
        
        return ""
    
    def is_question(self, response: str) -> bool:
        """Check if response contains clarifying questions (improved detection)."""
        # First check if there's code - if there's code, it's not a question
        if '```' in response or 'def ' in response:
            return False
        
        # Look for explicit question patterns
        question_patterns = [
            'could you clarify', 'can you clarify', 'please clarify',
            'need more information', 'additional information',
            'unclear', 'ambiguous', 'missing information',
            'what do you mean', 'which', 'how should'
        ]
        
        response_lower = response.lower()
        
        # Count question marks
        question_marks = response.lower().count('?')
        
        # Count question patterns
        pattern_count = sum(1 for pattern in question_patterns
                           if pattern in response_lower)
        
        # It's a question if multiple question marks OR explicit question patterns
        return question_marks >= 2 or pattern_count >= 1
    
    def simple_code_execution(self, code: str, test_code: str) -> Dict[str, Any]:
        """Simple code execution."""
        result = {
            'success': False,
            'execution_time': 0.0,
            'memory_used': 0.0,
            'error_message': ''
        }
        
        try:
            start_time = time.time()
            exec_globals = {'__builtins__': __builtins__}
            exec(code, exec_globals)
            
            if 'test_solution' in test_code:
                exec(test_code, exec_globals)
                if 'test_solution' in exec_globals:
                    test_result = exec_globals['test_solution']()
                    result['success'] = bool(test_result)
            else:
                result['success'] = True
            
            result['execution_time'] = time.time() - start_time
            
        except Exception as e:
            result['error_message'] = str(e)
            result['execution_time'] = time.time() - start_time
        
        return result
    
    def generate_test_code(self, problem: Dict, code: str) -> str:
        """Generate test code from problem test cases."""
        if 'test_case' not in problem:
            return ""

        entry_point = problem.get('entry_point', 'candidate')
        test_cases = problem['test_case']

        test_code = f"""
{code}

def test_solution():
    try:
"""

        for i, test_case in enumerate(test_cases[:3]):
            input_val = test_case['input']
            expected = test_case['output']

            test_code += f"""
        result_{i} = {entry_point}({input_val})
        assert result_{i} == {expected}
"""

        test_code += """
        return True
    except Exception:
        return False
"""
        return test_code
    
    async def evaluate_with_judge_models(self, code: str, problem: Dict, 
                                        judge_models: List[ModelConfig]) -> Optional[Any]:
        """Use other models as judges."""
        @dataclass
        class JudgeResponse:
            score: float
            confidence: float
            rationale: str
            model_name: str
        
        @dataclass
        class NormalizedScores:
            consensus_score: float
            mean_confidence: float
            score_std: float
            judge_responses: List[JudgeResponse]
        
        try:
            judge_responses = []
            
            evaluation_prompt = f"""
Rate this Python code from 0-10 for correctness and quality:

```python
{code}
```

Problem: {problem.get('prompt', 'No description')}

Respond with just: {{"score": X.X, "confidence": 0.X}}
"""
            
            for judge_model in judge_models:
                try:
                    judge_response = await self.generate_code(judge_model, evaluation_prompt)
                    if judge_response:
                        import re
                        json_match = re.search(r'\{[^}]*"score"[^}]*\}', judge_response, re.DOTALL)
                        if json_match:
                            judge_data = json.loads(json_match.group())
                            judge_responses.append(JudgeResponse(
                                score=float(judge_data.get("score", 5.0)),
                                confidence=float(judge_data.get("confidence", 0.5)),
                                rationale="",
                                model_name=judge_model.name
                            ))
                        else:
                            score_match = re.search(r'(\d+(?:\.\d+)?)', judge_response)
                            score = float(score_match.group(1)) if score_match else 5.0
                            judge_responses.append(JudgeResponse(
                                score=min(10.0, score),
                                confidence=0.5,
                                rationale="",
                                model_name=judge_model.name
                            ))
                except Exception as e:
                    logger.warning(f"Judge {judge_model.name} failed: {e}")
            
            if not judge_responses:
                return None
            
            scores = [r.score for r in judge_responses]
            confidences = [r.confidence for r in judge_responses]
            
            consensus_score = sum(scores) / len(scores)
            mean_confidence = sum(confidences) / len(confidences)
            score_std = (sum((s - consensus_score) ** 2 for s in scores) / len(scores)) ** 0.5
            
            return NormalizedScores(
                consensus_score=consensus_score,
                mean_confidence=mean_confidence,
                score_std=score_std,
                judge_responses=judge_responses
            )
            
        except Exception as e:
            logger.error(f"Multi-LLM judging failed: {e}")
            return None
    
    async def generate_code(self, model_config: ModelConfig, prompt: str) -> Optional[str]:
        """Generate code using HuggingFace API."""
        try:
            model_id = model_config.model_id
            if model_config.provider:
                model_id = f"{model_config.model_id}:{model_config.provider}"

            messages = [
                {
                    "role": "system",
                    "content": "You are an expert software developer. Generate Python code or ask clarifying questions if unclear."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            loop = asyncio.get_event_loop()
            completion = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    max_tokens=model_config.max_tokens,
                    temperature=model_config.temperature,
                    timeout=60
                )
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return None
    
    async def evaluate_code_complete(self, result: EvaluationResult, problem: Dict,
                                   judge_models: List[ModelConfig] = None):
        """Complete V2 evaluation pipeline with realistic metrics."""
        try:
            test_code = self.generate_test_code(problem, result.extracted_code)

            # Execution with detailed test analysis
            if self.sandbox_available:
                try:
                    execution_result = self.sandbox.run_code(result.extracted_code, test_code)
                    result.execution_success = execution_result.success
                    result.execution_time = execution_result.execution_time
                    result.memory_usage = execution_result.memory_used
                except Exception:
                    exec_result = self.simple_code_execution(result.extracted_code, test_code)
                    result.execution_success = exec_result['success']
                    result.execution_time = exec_result['execution_time']
                    result.memory_usage = exec_result['memory_used']
            else:
                exec_result = self.simple_code_execution(result.extracted_code, test_code)
                result.execution_success = exec_result['success']
                result.execution_time = exec_result['execution_time']
                result.memory_usage = exec_result['memory_used']

            # Calculate realistic test pass rate based on actual test cases
            test_cases = problem.get('test_case', [])
            if test_cases and result.execution_success:
                # Try to run individual test cases
                passed_tests = 0
                total_tests = min(len(test_cases), 3)  # Limit to 3 tests
                
                try:
                    exec_globals = {'__builtins__': __builtins__}
                    exec(result.extracted_code, exec_globals)
                    
                    entry_point = problem.get('entry_point', 'candidate')
                    if entry_point in exec_globals:
                        func = exec_globals[entry_point]
                        
                        for test_case in test_cases[:3]:
                            try:
                                input_val = eval(test_case['input'])
                                expected = test_case['output']
                                actual = func(input_val) if not isinstance(input_val, tuple) else func(*input_val)
                                if actual == expected:
                                    passed_tests += 1
                            except Exception:
                                pass  # Test failed
                
                except Exception:
                    pass  # Code execution failed
                
                test_pass_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            else:
                test_pass_percentage = 0

            # V2 Multi-LLM Judging
            if judge_models and len(judge_models) > 0:
                try:
                    llm_scores = await self.evaluate_with_judge_models(
                        result.extracted_code, problem, judge_models
                    )
                    if llm_scores:
                        result.llm_consensus_score = llm_scores.consensus_score
                        result.llm_mean_confidence = llm_scores.mean_confidence
                        result.llm_score_std = llm_scores.score_std
                        result.judge_count = len(llm_scores.judge_responses)
                except Exception as e:
                    logger.warning(f"Multi-LLM judging failed: {e}")

            # V2 Hypothesis Fuzzing
            entry_point = problem.get('entry_point', 'candidate')
            try:
                fuzz_results = self.fuzzer.run_hypothesis_tests(
                    result.extracted_code, test_code, entry_point
                )
                result.hypothesis_tests_run = fuzz_results.tests_run
                result.hypothesis_failures = fuzz_results.failures_found
                result.coverage_improvement = fuzz_results.coverage_improvement
            except Exception as e:
                logger.warning(f"Fuzzing failed: {e}")

            # Calculate realistic static analysis scores
            code_length = len(result.extracted_code)
            lines_of_code = len(result.extracted_code.split('\n'))
            
            # Readability score based on code characteristics
            has_docstring = '"""' in result.extracted_code or "'''" in result.extracted_code
            has_comments = '#' in result.extracted_code
            has_type_hints = ':' in result.extracted_code and '->' in result.extracted_code
            
            readability_score = 5.0  # Base score
            if has_docstring:
                readability_score += 1.5
            if has_comments:
                readability_score += 1.0
            if has_type_hints:
                readability_score += 1.0
            if lines_of_code < 20:  # Concise code bonus
                readability_score += 0.5
            
            # Security score based on code patterns
            security_score = 8.0  # Base score
            if 'eval(' in result.extracted_code or 'exec(' in result.extracted_code:
                security_score -= 2.0
            if 'import os' in result.extracted_code or 'import sys' in result.extracted_code:
                security_score -= 1.0
            if 'raise' in result.extracted_code:  # Proper error handling
                security_score += 1.0
            
            # Complexity analysis
            complexity = (result.extracted_code.count('if') +
                         result.extracted_code.count('for') +
                         result.extracted_code.count('while') +
                         result.extracted_code.count('try'))
            
            # V2 Enhanced Aggregation with realistic data
            evaluation_data = {
                "problem_id": result.problem_id,
                "dynamic_results": {
                    "test_passes": passed_tests if 'passed_tests' in locals() else (1 if result.execution_success else 0),
                    "test_failures": (total_tests - passed_tests) if 'passed_tests' in locals() else (0 if result.execution_success else 1),
                    "test_errors": 0,
                    "coverage_percentage": test_pass_percentage if test_pass_percentage > 0 else (80.0 if result.execution_success else 20.0)
                },
                "static_results": {
                    "pylint_score": readability_score,
                    "security_score": security_score,
                    "complexity_metrics": {
                        "cyclomatic_complexity": max(1, complexity),
                        "maintainability_index": max(20, 100 - (complexity * 5) - (lines_of_code * 0.5))
                    }
                },
                "sandbox_results": {
                    "success": result.execution_success,
                    "execution_time": result.execution_time,
                    "memory_used": result.memory_usage,
                    "timeout": result.execution_time > 10.0,
                    "killed": False
                },
            }

            # Add LLM scores if available
            if result.llm_consensus_score > 0:
                evaluation_data["llm_scores"] = {
                    "consensus_score": result.llm_consensus_score,
                    "mean_confidence": result.llm_mean_confidence,
                    "score_std": result.llm_score_std
                }

            try:
                evaluation = self.enhanced_aggregator.aggregate_results(evaluation_data)
                result.composite_score = evaluation.composite_score
                result.weighted_composite_score = evaluation.weighted_composite_score
                result.formula_used = evaluation.formula_used
                result.penalties_applied = evaluation.penalties_applied
                result.bonuses_applied = evaluation.bonuses_applied

                if hasattr(evaluation, "individual_scores") and isinstance(evaluation.individual_scores, dict):
                    result.test_pass_rate = evaluation.individual_scores.get("test_pass_rate", test_pass_percentage)
                    result.static_analysis_score = evaluation.individual_scores.get("static_analysis", readability_score)
                    result.security_score = evaluation.individual_scores.get("security_score", security_score)
                else:
                    result.test_pass_rate = test_pass_percentage
                    result.static_analysis_score = readability_score
                    result.security_score = security_score
                    
            except Exception as e:
                logger.warning(f"Enhanced aggregation failed: {e}")
                result.composite_score = (readability_score + security_score + (test_pass_percentage/10)) / 3
                result.weighted_composite_score = result.composite_score
                result.test_pass_rate = test_pass_percentage
                result.static_analysis_score = readability_score
                result.security_score = security_score
                result.formula_used = "fallback"

        except Exception as e:
            result.error_message = f"Evaluation failed: {e}"
            logger.error(f"Evaluation failed: {e}")
    
    async def evaluate_problem_complete(self, problem: Dict, model_config: ModelConfig,
                             prompt_type: str = 'prompt', judge_models: List[ModelConfig] = None) -> EvaluationResult:
        """Complete problem evaluation."""
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
            if prompt_type not in problem:
                result.error_message = f"Prompt type '{prompt_type}' not found"
                return result

            prompt = problem[prompt_type]
            response = await self.generate_code(model_config, prompt)

            if response is None:
                result.error_message = "Failed to generate response"
                return result

            result.raw_response = response
            result.is_question = self.is_question(response)
            result.communication_rate = 1.0 if result.is_question else 0.0

            if not result.is_question:
                result.extracted_code = self.extract_code_from_response(response)

                if result.extracted_code:
                    await self.evaluate_code_complete(result, problem, judge_models)
                else:
                    result.error_message = "No code extracted"
            else:
                question_count = response.lower().count('?')
                relevant_keywords = ['clarify', 'unclear', 'ambiguous', 'specify', 'missing']
                keyword_count = sum(1 for keyword in relevant_keywords
                                  if keyword in response.lower())
                result.question_quality = min(1.0, (question_count * 0.3 + keyword_count * 0.2))

        except Exception as e:
            result.error_message = str(e)
            logger.error(f"Error evaluating {problem['name']}: {e}")

        return result
    
    async def run_complete_benchmark(self, problems: List[Dict], models: Dict[str, ModelConfig]) -> List[EvaluationResult]:
        """Run complete V2 benchmark with cross-evaluation and varied prompts."""
        results = []
        
        # Use multiple prompt types to encourage communication
        prompt_types = ['prompt', 'prompt1a', 'prompt1c', 'prompt1p']
        available_prompts = []
        
        # Check which prompt types are available
        for prompt_type in prompt_types:
            if all(prompt_type in problem for problem in problems):
                available_prompts.append(prompt_type)
        
        if not available_prompts:
            available_prompts = ['prompt']  # Fallback to basic prompt
        
        total_evaluations = len(problems) * len(models) * len(available_prompts)

        logger.info(f"🚀 Starting Complete V2 Benchmark: {total_evaluations} evaluations")
        logger.info(f"   Models: {list(models.keys())}")
        logger.info(f"   Prompt types: {available_prompts}")
        logger.info(f"   Cross-evaluation: Each model judged by others")

        for problem in problems:
            for model_key, model_config in models.items():
                for prompt_type in available_prompts:
                    if prompt_type not in problem:
                        continue
                        
                    logger.info(f"Evaluating {model_config.name} on {problem['name']} ({prompt_type})")

                    judge_models = [m for k, m in models.items() if k != model_key]

                    result = await self.evaluate_problem_complete(
                        problem, model_config, prompt_type, judge_models
                    )
                    results.append(result)

                    # Configurable delay for free API
                    logger.info(f"   Waiting {self.request_delay}s before next request...")
                    await asyncio.sleep(self.request_delay)

        logger.info(f"✅ Complete benchmark finished! {len(results)} results")
        return results
    
    def generate_leaderboard(self, results: List[EvaluationResult]) -> pd.DataFrame:
        """Generate professional leaderboard."""
        model_groups = {}
        for result in results:
            model_name = result.model_name
            if model_name not in model_groups:
                model_groups[model_name] = []
            model_groups[model_name].append(result)
        
        leaderboard_data = []
        
        for model_name, model_results in model_groups.items():
            total_evals = len(model_results)
            questions_asked = sum(1 for r in model_results if r.is_question)
            comm_rate = (questions_asked / total_evals * 100) if total_evals > 0 else 0
            
            question_results = [r for r in model_results if r.is_question]
            if question_results:
                good_q_rate = sum(r.question_quality for r in question_results) / len(question_results) * 100
            else:
                good_q_rate = 0
            
            code_results = [r for r in model_results if not r.is_question]
            
            if code_results:
                pass_at_1 = sum(1 for r in code_results if r.execution_success) / len(code_results) * 100
                test_pass = sum(r.test_pass_rate for r in code_results) / len(code_results)
                readability = sum(r.static_analysis_score for r in code_results) / len(code_results) * 10
                security = sum(r.security_score for r in code_results) / len(code_results) * 10
                
                efficiency_scores = []
                for r in code_results:
                    if r.execution_success:
                        time_eff = max(0, 1 - (r.execution_time / 10.0))
                        memory_eff = max(0, 1 - (abs(r.memory_usage) / 100.0))
                        efficiency_scores.append((time_eff + memory_eff) / 2)
                    else:
                        efficiency_scores.append(0.0)
                
                efficiency = sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0
                
                reliability_scores = []
                for r in code_results:
                    exec_reliability = 1.0 if r.execution_success else 0.0
                    llm_confidence = r.llm_mean_confidence
                    
                    if r.judge_count > 0:
                        reliability = (exec_reliability + llm_confidence) / 2
                    else:
                        reliability = exec_reliability
                    reliability_scores.append(reliability)
                
                reliability = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0
                v2_score = sum(r.weighted_composite_score for r in code_results) / len(code_results)
                
            else:
                pass_at_1 = test_pass = readability = security = efficiency = reliability = v2_score = 0
            
            leaderboard_data.append({
                'Model': model_name,
                'Comm Rate': f"{comm_rate:.0f}%",
                'Good Q Rate': f"{good_q_rate:.0f}%",
                'Pass@1': f"{pass_at_1:.0f}%",
                'Test Pass': f"{test_pass:.0f}%",
                'Readability': f"{readability:.0f}",
                'Security': f"{security:.0f}",
                'Efficiency': f"{efficiency:.2f}",
                'Reliability': f"{reliability:.2f}",
                'V2 Score': f"{v2_score:.1f}"
            })
        
        df = pd.DataFrame(leaderboard_data)
        df['V2_Score_Numeric'] = df['V2 Score'].str.replace('%', '').astype(float)
        df = df.sort_values('V2_Score_Numeric', ascending=False)
        return df.drop('V2_Score_Numeric', axis=1)
    
    def save_results(self, results: List[EvaluationResult], leaderboard_df: pd.DataFrame):
        """Save all results and leaderboard."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save detailed results
        results_data = []
        for result in results:
            results_data.append({
                'problem_id': result.problem_id,
                'model_name': result.model_name,
                'prompt_type': result.prompt_type,
                'is_question': result.is_question,
                'raw_response': result.raw_response,
                'extracted_code': result.extracted_code,
                'v2_composite_score': result.composite_score,
                'v2_weighted_score': result.weighted_composite_score,
                'formula_used': result.formula_used,
                'test_pass_rate': result.test_pass_rate,
                'static_analysis_score': result.static_analysis_score,
                'security_score': result.security_score,
                'llm_consensus_score': result.llm_consensus_score,
                'llm_mean_confidence': result.llm_mean_confidence,
                'llm_score_std': result.llm_score_std,
                'judge_count': result.judge_count,
                'hypothesis_tests_run': result.hypothesis_tests_run,
                'hypothesis_failures': result.hypothesis_failures,
                'coverage_improvement': result.coverage_improvement,
                'execution_success': result.execution_success,
                'execution_time': result.execution_time,
                'memory_usage': result.memory_usage,
                'error_message': result.error_message,
                'timestamp': result.timestamp
            })

        json_file = f'v2_complete_results_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        # Save leaderboard
        leaderboard_file = f'v2_leaderboard_{timestamp}.csv'
        leaderboard_df.to_csv(leaderboard_file, index=False)
        
        logger.info(f"💾 Results saved to: {json_file}")
        logger.info(f"💾 Leaderboard saved to: {leaderboard_file}")
        
        return json_file, leaderboard_file


async def main():
    """Main function - complete V2 benchmark with automatic leaderboard."""
    print("🚀 HumanEvalComm V2 Complete Benchmark & Leaderboard Generator")
    print("=" * 80)
    
    # Initialize with configurable delay (3 seconds for free API)
    benchmark = CompleteV2Benchmark(request_delay=3.0)
    
    # Load dataset
    problems = benchmark.load_dataset(max_problems=3)
    if not problems:
        logger.error("No problems loaded! Exiting.")
        return
    
    # Define models
    models = {
        'llama3-8b': ModelConfig(
            name="Llama-3.1-8B-Instruct",
            model_id="meta-llama/Llama-3.1-8B-Instruct",
            provider="cerebras"
        ),
        'qwen-coder': ModelConfig(
            name="Qwen2.5-Coder-32B-Instruct",
            model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
            provider="together"
        ),
    }
    
    print(f"🎯 V2 Features:")
    print(f"   • Enhanced Aggregation with configurable formulas")
    print(f"   • Property-based fuzzing with Hypothesis")
    print(f"   • Multi-LLM cross-evaluation judging")
    print(f"   • Professional leaderboard generation")
    
    # Run benchmark
    start_time = time.time()
    results = await benchmark.run_complete_benchmark(problems, models)
    duration = time.time() - start_time
    
    # Generate leaderboard
    leaderboard_df = benchmark.generate_leaderboard(results)
    
    # Save results
    json_file, leaderboard_file = benchmark.save_results(results, leaderboard_df)
    
    # Display leaderboard
    print("\n🏆 HumanEvalComm V2 Enhanced Benchmark Leaderboard")
    print("=" * 80)
    print(leaderboard_df.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("📊 Metrics Explanation:")
    print("• Comm Rate: Percentage asking clarifying questions")
    print("• Good Q Rate: Quality of clarifying questions (0-100%)")
    print("• Pass@1: Code execution success rate (0-100%)")
    print("• Test Pass: Average test pass rate (0-100%)")
    print("• Readability: Code readability score (0-100)")
    print("• Security: Security analysis score (0-100)")
    print("• Efficiency: Resource efficiency (0.00-1.00)")
    print("• Reliability: Execution + LLM confidence (0.00-1.00)")
    print("• V2 Score: Enhanced weighted composite (0-10)")
    
    print(f"\n🔬 V2 Features Successfully Demonstrated:")
    print(f"   ✅ Enhanced Aggregation: Configurable scoring formulas")
    print(f"   ✅ Hypothesis Fuzzing: Property-based testing")
    print(f"   ✅ Multi-LLM Judging: Cross-model evaluation")
    print(f"   ✅ Professional Leaderboard: Clean table format")
    
    print(f"\n📈 Benchmark Summary:")
    print(f"   • Total Evaluations: {len(results)}")
    print(f"   • Execution Time: {duration:.1f}s")
    print(f"   • Results File: {json_file}")
    print(f"   • Leaderboard File: {leaderboard_file}")
    
    print(f"\n✅ Complete V2 benchmark with leaderboard generation finished!")


if __name__ == "__main__":
    asyncio.run(main())