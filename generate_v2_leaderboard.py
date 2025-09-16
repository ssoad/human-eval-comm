#!/usr/bin/env python3
"""
V2 Leaderboard Generator

Generates a clean leaderboard table from V2 benchmark results in the format:
Model | Comm Rate | Good Q Rate | Pass@1 | Test Pass | Readability | Security | Efficiency | Reliability | V2 Score
"""

import pandas as pd
import json
import sys
from typing import Dict, List, Any

def load_v2_results(json_file: str) -> List[Dict[str, Any]]:
    """Load V2 benchmark results from JSON file."""
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading results: {e}")
        return []

def calculate_leaderboard_metrics(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Calculate leaderboard metrics from V2 results."""
    
    # Group by model
    model_groups = {}
    for result in results:
        model_name = result['model_name']
        if model_name not in model_groups:
            model_groups[model_name] = []
        model_groups[model_name].append(result)
    
    leaderboard_data = []
    
    for model_name, model_results in model_groups.items():
        # Communication metrics
        total_evals = len(model_results)
        questions_asked = sum(1 for r in model_results if r.get('is_question', False))
        comm_rate = (questions_asked / total_evals * 100) if total_evals > 0 else 0
        
        # Good question rate (based on question quality)
        question_results = [r for r in model_results if r.get('is_question', False)]
        if question_results:
            avg_question_quality = sum(r.get('question_quality', 0) for r in question_results) / len(question_results)
            good_q_rate = avg_question_quality * 100  # Convert to percentage
        else:
            good_q_rate = 0
        
        # Code generation metrics
        code_results = [r for r in model_results if not r.get('is_question', False)]
        
        if code_results:
            # Pass@1 (execution success rate)
            pass_at_1 = sum(1 for r in code_results if r.get('execution_success', False)) / len(code_results) * 100
            
            # Test pass rate (average of test pass scores)
            test_pass = sum(r.get('test_pass_rate', 0) for r in code_results) / len(code_results)
            
            # Readability (static analysis score converted to 0-100)
            readability = sum(r.get('static_analysis_score', 0) for r in code_results) / len(code_results) * 10
            
            # Security (security score converted to 0-100)
            security = sum(r.get('security_score', 0) for r in code_results) / len(code_results) * 10
            
            # Efficiency (normalized based on execution time and memory)
            efficiency_scores = []
            for r in code_results:
                if r.get('execution_success', False):
                    exec_time = r.get('execution_time', 1.0)
                    memory = r.get('memory_usage', 50.0)
                    # Normalize: lower time and memory = higher efficiency
                    time_eff = max(0, 1 - (exec_time / 10.0))  # Normalize to 0-1
                    memory_eff = max(0, 1 - (abs(memory) / 100.0))  # Normalize to 0-1
                    efficiency_scores.append((time_eff + memory_eff) / 2)
                else:
                    efficiency_scores.append(0.0)
            
            efficiency = sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0
            
            # Reliability (based on LLM consensus confidence and execution success)
            reliability_scores = []
            for r in code_results:
                exec_reliability = 1.0 if r.get('execution_success', False) else 0.0
                llm_confidence = r.get('llm_mean_confidence', 0.5)
                judge_count = r.get('judge_count', 0)
                
                # Combine execution reliability with LLM confidence
                if judge_count > 0:
                    reliability = (exec_reliability + llm_confidence) / 2
                else:
                    reliability = exec_reliability
                reliability_scores.append(reliability)
            
            reliability = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0
            
            # V2 Score (weighted composite score)
            v2_score = sum(r.get('v2_weighted_score', 0) for r in code_results) / len(code_results)
            
        else:
            # No code generated, only questions
            pass_at_1 = 0
            test_pass = 0
            readability = 0
            security = 0
            efficiency = 0
            reliability = 0
            v2_score = 0
        
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
    
    return pd.DataFrame(leaderboard_data)

def generate_leaderboard(json_file: str):
    """Generate and display the V2 leaderboard."""
    print("🏆 HumanEvalComm V2 Enhanced Benchmark Leaderboard")
    print("=" * 80)
    
    # Load results
    results = load_v2_results(json_file)
    if not results:
        print("❌ No results found!")
        return
    
    # Calculate metrics
    leaderboard_df = calculate_leaderboard_metrics(results)
    
    # Sort by V2 Score (descending)
    leaderboard_df['V2_Score_Numeric'] = leaderboard_df['V2 Score'].str.replace('%', '').astype(float)
    leaderboard_df = leaderboard_df.sort_values('V2_Score_Numeric', ascending=False)
    leaderboard_df = leaderboard_df.drop('V2_Score_Numeric', axis=1)
    
    # Display table
    print(leaderboard_df.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("📊 Metrics Explanation:")
    print("• Comm Rate: Percentage of responses that asked clarifying questions")
    print("• Good Q Rate: Quality of clarifying questions (0-100%)")
    print("• Pass@1: Percentage of code that executed successfully")
    print("• Test Pass: Average test pass rate (0-100%)")
    print("• Readability: Code readability score (0-100)")
    print("• Security: Security analysis score (0-100)")
    print("• Efficiency: Resource efficiency score (0.00-1.00)")
    print("• Reliability: Execution + LLM judge confidence (0.00-1.00)")
    print("• V2 Score: Enhanced weighted composite score (0-10)")
    
    print(f"\n🔬 V2 Features Used:")
    print(f"• Enhanced Aggregation: ✅ Configurable scoring formulas")
    print(f"• Hypothesis Fuzzing: ✅ Property-based testing")
    print(f"• Multi-LLM Judging: ✅ Cross-model evaluation")
    print(f"• Robust Pipeline: ✅ Error handling and fallbacks")
    
    # Save leaderboard
    timestamp = json_file.split('_')[-1].replace('.json', '')
    leaderboard_file = f'v2_leaderboard_{timestamp}.csv'
    leaderboard_df.to_csv(leaderboard_file, index=False)
    print(f"\n💾 Leaderboard saved to: {leaderboard_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_v2_leaderboard.py <results.json>")
        print("Example: python generate_v2_leaderboard.py v2_robust_benchmark_results_20250917_011831.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    generate_leaderboard(json_file)