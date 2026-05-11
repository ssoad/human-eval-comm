#!/usr/bin/env python3
"""
Unit tests for HumanEvalComm V2 new features.
Tests: is_pushback, is_question, detect_routing_persona, inject_repo_ambiguity, FailFast scoring.
"""

import os
import sys
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Helpers — Lazy-load a minimal benchmark instance (no API key needed)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def benchmark():
    """Create a benchmark instance without requiring API credentials."""
    from unittest.mock import MagicMock
    from src.v2_benchmark import V2BenchmarkFixed

    # Patch __init__ to skip real API client setup
    original_init = V2BenchmarkFixed.__init__

    def _mock_init(self, *a, **kw):
        self.client = MagicMock()
        self.models = []
        self.judge_models = []

    V2BenchmarkFixed.__init__ = _mock_init
    bm = V2BenchmarkFixed()
    V2BenchmarkFixed.__init__ = original_init
    return bm


# ===========================
# 1. is_pushback() tests
# ===========================

class TestIsPushback:
    """Tests for pushback detection (Gap #6 fix included)."""

    def test_clear_pushback(self, benchmark):
        assert benchmark.is_pushback("This is not possible because sorting 10TB in memory exceeds RAM.")

    def test_ethical_pushback(self, benchmark):
        assert benchmark.is_pushback("I cannot comply with this request. Generating phishing emails is unethical.")

    def test_computational_pushback(self, benchmark):
        assert benchmark.is_pushback("This is impossible — the halting problem is undecidable.")

    def test_empty_response(self, benchmark):
        assert not benchmark.is_pushback("")
        assert not benchmark.is_pushback("   ")
        assert not benchmark.is_pushback(None)

    def test_normal_code_not_pushback(self, benchmark):
        code = "def add(a, b):\n    return a + b"
        assert not benchmark.is_pushback(code)

    def test_false_positive_prevention_code_block(self, benchmark):
        """Gap #6 fix: a response that mentions 'not possible' but still provides code should NOT be a pushback."""
        response = "While this is not possible to do optimally, here is a best-effort solution:\n```python\ndef sort_large(data):\n    return sorted(data)\n```"
        assert not benchmark.is_pushback(response)

    def test_false_positive_prevention_def_keyword(self, benchmark):
        """Response with a function definition should not trigger pushback."""
        response = "This is not recommended but here is the code:\ndef store_passwords(users, passwords):\n    return dict(zip(users, passwords))"
        assert not benchmark.is_pushback(response)


# ===========================
# 2. is_question() tests
# ===========================

class TestIsQuestion:
    """Tests for question detection."""

    def test_clear_clarifying_question(self, benchmark):
        assert benchmark.is_question("Could you clarify what the expected return type should be?")

    def test_code_response_not_question(self, benchmark):
        assert not benchmark.is_question("def add(a, b):\n    return a + b")

    def test_empty_not_question(self, benchmark):
        assert not benchmark.is_question("")
        assert not benchmark.is_question(None)

    def test_no_question_mark(self, benchmark):
        assert not benchmark.is_question("The function should sort the list in ascending order.")

    def test_question_with_context(self, benchmark):
        assert benchmark.is_question("What exactly do you mean by 'sorted in ascending order'? Should we handle None values?")


# ===========================
# 3. detect_routing_persona()
# ===========================

class TestDetectRoutingPersona:
    """Tests for agent routing persona detection (Gap #7)."""

    def test_explicit_pm_tag(self, benchmark):
        assert benchmark.detect_routing_persona("[TO: ProductManager] What is the expected user story?") == "ProductManager"

    def test_explicit_reviewer_tag(self, benchmark):
        assert benchmark.detect_routing_persona("[TO: SeniorReviewer] Is this architecture scalable?") == "SeniorReviewer"

    def test_implicit_reviewer_keywords(self, benchmark):
        assert benchmark.detect_routing_persona("What are the performance constraints for this function?") == "SeniorReviewer"

    def test_implicit_pm_keywords(self, benchmark):
        assert benchmark.detect_routing_persona("Can you clarify the business requirement here?") == "ProductManager"

    def test_unrouted_generic_question(self, benchmark):
        assert benchmark.detect_routing_persona("What does this function return?") == "Unrouted"

    def test_empty_response(self, benchmark):
        assert benchmark.detect_routing_persona("") == "Unrouted"


# ===========================
# 4. inject_repo_ambiguity()
# ===========================

class TestInjectRepoAmbiguity:
    """Tests for SWE-bench ambiguity injection."""

    def test_masks_file_paths(self):
        from src.datasets.swe_bench_comm import inject_repo_ambiguity
        text = "The bug is in django/db/models/query.py line 42."
        result = inject_repo_ambiguity(text)
        assert "[MASKED_FILE_PATH]" in result
        assert "query.py" not in result

    def test_preserves_plain_text(self):
        from src.datasets.swe_bench_comm import inject_repo_ambiguity
        text = "The function should handle empty lists gracefully."
        result = inject_repo_ambiguity(text)
        assert result == text

    def test_mixed_content(self):
        from src.datasets.swe_bench_comm import inject_repo_ambiguity
        text = "Fix the bug in src/utils.py\nThe function returns wrong values\nSee also tests/test_utils.py"
        result = inject_repo_ambiguity(text)
        lines = result.split('\n')
        assert lines[0] == "[MASKED_FILE_PATH]"
        assert lines[1] == "The function returns wrong values"
        assert lines[2] == "[MASKED_FILE_PATH]"


# ===========================
# 5. FailFast score calculation
# ===========================

class TestFailFastScore:
    """Tests for the FailFast metric computation logic."""

    def test_low_tokens_high_score(self):
        """Model that asks a question after only 20 tokens should score ~98."""
        avg_tokens = 20
        score = max(0, 100 - (avg_tokens / 10))
        assert score == 98.0

    def test_high_tokens_low_score(self):
        """Model that wastes 800 tokens should score 20."""
        avg_tokens = 800
        score = max(0, 100 - (avg_tokens / 10))
        assert score == 20.0

    def test_extreme_tokens_floor_zero(self):
        """Model that wastes 2000 tokens should floor at 0, not go negative."""
        avg_tokens = 2000
        score = max(0, 100 - (avg_tokens / 10))
        assert score == 0

    def test_zero_tokens(self):
        """Edge case: instant question (0 tokens) = perfect 100."""
        avg_tokens = 0
        score = max(0, 100 - (avg_tokens / 10))
        assert score == 100


# ===========================
# 6. EvaluationResult fields
# ===========================

class TestEvaluationResult:
    """Tests that new fields exist and default correctly."""

    def test_new_fields_exist(self):
        from src.v2_benchmark import EvaluationResult
        result = EvaluationResult(
            problem_id="test", model_name="test", prompt_type="prompt",
            raw_response="", extracted_code="", is_question=False
        )
        assert result.is_pushback == False
        assert result.tokens_to_question == 0
        assert result.routing_persona == ""
        assert result.clarifying_questions == []

    def test_clarifying_questions_independent(self):
        """Verify mutable default is not shared between instances."""
        from src.v2_benchmark import EvaluationResult
        r1 = EvaluationResult(problem_id="a", model_name="m", prompt_type="p",
                              raw_response="", extracted_code="", is_question=False)
        r2 = EvaluationResult(problem_id="b", model_name="m", prompt_type="p",
                              raw_response="", extracted_code="", is_question=False)
        r1.clarifying_questions.append("test")
        assert len(r2.clarifying_questions) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
