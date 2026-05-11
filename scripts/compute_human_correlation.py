#!/usr/bin/env python3
"""
Compute correlation between human annotations and LLM-as-a-judge scores.
"""

import os
import sys
import json
try:
    import numpy as np
    from scipy.stats import pearsonr
    from sklearn.metrics import cohen_kappa_score
except ImportError:
    print("❌ Missing required packages. Please run: pip install scipy scikit-learn numpy")
    sys.exit(1)

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_leaderboard.data_manager import LeaderboardManager

def main():
    # Setup path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = LeaderboardManager()
    manager.base_dir = base_dir
    
    annotations_file = os.path.join(base_dir, 'Benchmark', 'human_annotations.json')
    
    if not os.path.exists(annotations_file):
        print("❌ No human annotations found. Please use the /annotate UI first.")
        return
        
    with open(annotations_file, 'r') as f:
        annotations = json.load(f)
        
    results_data = manager.load_detailed_results()
    if not results_data:
        print("❌ No detailed results found.")
        return
        
    # Map results by key
    results_map = {f"{r.get('model_name')}_{r.get('problem_id')}": r for r in results_data}
    
    human_scores = []
    llm_scores = []
    
    for key, ann in annotations.items():
        if key in results_map:
            h_score = ann.get('human_score')
            l_score = results_map[key].get('question_quality_score')
            
            if h_score is not None and l_score is not None:
                human_scores.append(h_score)
                llm_scores.append(int(l_score))
                
    if len(human_scores) < 3:
        print(f"⚠️ Only found {len(human_scores)} overlapping annotations. Need at least 3 for correlation.")
        return
        
    print(f"📊 Found {len(human_scores)} overlapping annotations.")
    
    # Calculate correlations
    pearson_corr, p_value = pearsonr(human_scores, llm_scores)
    kappa = cohen_kappa_score(human_scores, llm_scores)
    
    print(f"\n🧠 Human vs. LLM-as-a-Judge Alignment:")
    print(f"Pearson Correlation: {pearson_corr:.3f} (p={p_value:.3f})")
    print(f"Cohen's Kappa:       {kappa:.3f}")
    
    if pearson_corr > 0.7:
        print("\n✅ Strong alignment! The LLM-as-a-judge is highly reliable.")
    elif pearson_corr > 0.4:
        print("\n⚠️ Moderate alignment. The LLM-as-a-judge is somewhat reliable but has biases.")
    else:
        print("\n❌ Poor alignment. The LLM-as-a-judge does not match human judgements.")

if __name__ == '__main__':
    main()
