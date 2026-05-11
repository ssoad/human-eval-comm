"""
SWE-bench Wrapper for HumanEvalComm V2.
Loads SWE-bench problems and injects artificial ambiguity to test agent communication at the repository level.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def inject_repo_ambiguity(issue_text: str) -> str:
    """
    Remove specific file paths and class names to force the agent to ask clarifying questions.
    In a real implementation, this uses NLP to identify and mask paths.
    """
    # Simple heuristic mask for demonstration
    lines = issue_text.split('\n')
    masked_lines = []
    for line in lines:
        if '.py' in line or '/' in line:
            masked_lines.append("[MASKED_FILE_PATH]")
        else:
            masked_lines.append(line)
    return '\n'.join(masked_lines)

def load_swe_bench_lite(max_problems: int = 5) -> List[Dict]:
    """
    Load SWE-bench Lite and format it for HumanEvalComm.
    """
    problems = []
    try:
        import datasets
        ds = datasets.load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
        
        for i, item in enumerate(ds):
            if i >= max_problems:
                break
                
            original_prompt = item['problem_statement']
            ambiguous_prompt = inject_repo_ambiguity(original_prompt)
            
            problems.append({
                "name": f"SWE-bench/{item['instance_id']}",
                "repo": item['repo'],
                "prompt": original_prompt,
                "prompt1p": ambiguous_prompt,  # Use prompt1p so it seamlessly integrates into the loop
                "solution": item['patch'],
                "entry_point": "repo_level_execution",
                "repo_level": True
            })
            
        logger.info(f"Loaded {len(problems)} SWE-bench problems.")
        
    except ImportError:
        logger.warning("datasets package not found. Using mock SWE-bench data.")
        problems.append({
            "name": "SWE-bench/mock-1",
            "repo": "django/django",
            "prompt": "Fix the QuerySet.filter() method to handle nested Q objects correctly in django/db/models/query.py.",
            "prompt1p": "Fix the QuerySet.filter() method to handle nested Q objects correctly in [MASKED_FILE_PATH].",
            "solution": "diff --git a/django/db/models/query.py ...",
            "entry_point": "repo_level_execution",
            "repo_level": True
        })
        
    return problems
