
# HumanEvalComm + HuggingFace LLM Benchmark: Step-by-Step Plan

---

## Step 1: Input Preparation

- Use the modified HumanEvalComm dataset (JSONL, in Benchmark/).
- Optionally, add “real-world issue tracker” prompts (e.g., GitHub bug reports with vague descriptions).

---

## Step 2: Model Interaction

- Round-based setup (like Okanagan):
  - If requirement is clear, skip questioning.
  - If unclear, trigger clarifying question round.
- For each round, record model output and metadata.

---

## Step 3: Clarifying Question Evaluation

- Multi-judge system:
  - Judges: GPT-4, Claude, DeepSeek, CodeQwen, etc.
  - Each judge produces JSON score + confidence.
- Consensus aggregator: reliability-weighted average.
- Calibration: fit reliability weights using human-annotated subset.

---

## Step 4: Code Evaluation

- Run in Docker sandbox with resource limits.
- Two levels of testing:
  - Unit tests (from dataset)
  - Fuzz/property tests (Hypothesis, auto-generated edge cases)

---

## Step 5: Extended Metrics

- Correctness: Test Pass Rate.
- Readability: pylint/flake8 style score, cyclomatic complexity.
- Security: bandit scan (detect vulnerable code).
- Efficiency: runtime/memory usage inside sandbox.
- Maintainability: docstring presence, comment density.

---

## Step 6: Human Calibration

- Select ~10–15% of cases:
  - Where judges disagree
  - Where consensus confidence is low
- Get human labels (good/bad question, correctness).
- Update calibration weights.

---

## Step 7: Final Scoring

- Composite score (example weighting):
  - 0.40 * Correctness
  - 0.20 * Communication (Comm Rate * Good Q Rate)
  - 0.15 * Readability
  - 0.10 * Security
  - 0.10 * Efficiency
  - 0.05 * Maintainability
- All weights configurable via config file.

---

## Step 8: Reporting

- Store raw JSON logs (per model, per task).
- Export multi-dimensional leaderboard (Kaggle/PapersWithCode style).
- Provide visualizations (heatmaps, radar plots per model).

---

## Reliability Improvements vs Paper

- No single LLM judge bias: consensus + calibration.
- No reliance only on unit tests: fuzzing + sandbox ensures robustness.
- Human labor minimized but statistically integrated.
- Transparent pipeline: reproducible, auditable results.

---

## Roadmap

- Extend repo with evaluators/ folder (multi-judge, sandbox, static analysis).
- Integrate into existing pipeline scripts.
- Build calibration set (crowdsourcing or expert review).
- Release HumanEvalComm V2 with open leaderboard + reproducible scripts.
