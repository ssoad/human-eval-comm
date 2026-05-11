# HumanEvalComm V2: The Ultimate Execution & Research Guide

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-username/human-eval-comm-v2/blob/main/HumanEvalComm_V2_Colab.ipynb)

This guide provides an exhaustive reference for running the **HumanEvalComm V2** benchmark suite. Whether you are running local models, cloud APIs, or multi-agent simulations, all commands and flags are detailed below.

---

## 1. Installation & Environment Setup

### Quick Install
```bash
# Clone and enter repo
cd human-eval-comm-v2

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_v2.txt

# Initialize configuration
cp .env.template .env
```

### API Provider Setup (.env)
You must add the relevant keys to your `.env` for the providers you plan to use:
*   **HuggingFace**: `HF_TOKEN`
*   **OpenRouter**: `OPENROUTER_API_KEY`
*   **OpenAI**: `OPENAI_API_KEY`
*   **Local**: `LOCAL_API_BASE` (e.g., `http://localhost:11434/v1` for Ollama)
*   **Custom**: `CUSTOM_API_BASE` and `CUSTOM_API_KEY`

---

## 2. Benchmark Execution Reference

The core command is `python3 src/v2_benchmark.py`. Below are the primary flags:

| Flag | Type | Description |
| :--- | :--- | :--- |
| `--dataset-path` | `str` | Path to the `.jsonl` file or `swe-bench-lite`. |
| `--models` | `list` | Model spec: `name:id[:provider][:tokens][:temp]`. Can be used multiple times. |
| `--api-provider` | `str` | Default global provider (`openai`, `local`, `openrouter`, etc.). |
| `--max-problems`| `int` | Limit the run size (useful for dry runs). Default: 3. |
| `--request-delay`| `float` | Seconds to wait between calls (important for free tiers). |
| `--output-dir` | `str` | Where to save `.csv` and `.json` results. |
| `--verbose` | `bool` | Enables detailed debug logging. |

---

## 3. Provider Configuration Examples

### A. Global Provider (Same backend for all models)
Best when testing multiple models from the same service.
```bash
python3 src/v2_benchmark.py \
  --api-provider openrouter \
  --models "claude:anthropic/claude-3-haiku" \
  --models "llama:meta-llama/llama-3-8b-instruct"
```

### B. Per-Model Provider (Mix & Match)
Essential for cross-provider benchmarking (e.g., comparing Local vs. Cloud).
```bash
python3 src/v2_benchmark.py \
  --models "local:llama3:local" \
  --models "cloud:gpt-4o:openai"
```

### C. Customized Model Parameters
Override default tokens and temperature for specific models.
```bash
# Format: nickname:model_id:provider:max_tokens:temperature
python3 src/v2_benchmark.py \
  --models "creative:gpt-4o:openai:2048:0.7" \
  --models "precise:gpt-4o:openai:512:0.1"
```

---

## 4. Benchmark Modes & Use Cases

### Mode 1: Standard Evaluation (HumanEvalComm V2)
Evaluates communication quality and code accuracy on 163 standard problems.
```bash
python3 src/v2_benchmark.py --dataset-path Benchmark/HumanEvalComm_v2.jsonl
```

### Mode 2: Pushback & Negotiation (Unfeasible Dataset)
Tests if models correctly refuse impossible or unsafe tasks. **Critical for "Pushback Rate" metric.**
```bash
python3 src/v2_benchmark.py --dataset-path Benchmark/HumanEvalComm_Unfeasible.jsonl
```

### Mode 3: Repo-Level Context (SWE-bench)
Tests how models handle ambiguity in large, multi-file codebases.
```bash
python3 src/v2_benchmark.py --dataset-path swe-bench-lite --max-problems 10
```

---

## 5. Visualization & Research Analysis

### Step 1: Launch Leaderboard
Visualize V2 metrics (Pushback, FailFast, Routing) in a beautiful web UI.
```bash
cd flask_leaderboard
python3 app.py
# Access at http://localhost:8080
```

### Step 2: Human-in-the-Loop Annotation
Validate LLM-as-a-judge scores with human oversight.
1.  Go to `http://localhost:8080/annotate`.
2.  Review and grade model responses.
3.  Data is saved to `Benchmark/human_annotations.json`.

### Step 3: Scientific Validation (Correlation)
Calculate Pearson Correlation and Cohen’s Kappa for your research paper.
```bash
python3 scripts/compute_human_correlation.py
```

---

## 6. Testing & Maintenance

### Verify Logic Integrity
Run this after making changes to the benchmark logic or adding new heuristics.
```bash
python3 -m pytest tests/test_v2_features.py -v
```

### Clean Up Results
```bash
# Remove temporary evaluation results
rm results/*.csv benchmark_results/*.json
```

---

## 7. Key File Architecture
*   `src/v2_benchmark.py`: Main engine.
*   `Benchmark/HumanEvalComm_v2.jsonl`: Primary dataset.
*   `Benchmark/HumanEvalComm_Unfeasible.jsonl`: Pushback dataset.
*   `src/datasets/swe_bench_comm.py`: SWE-bench adapter.
*   `flask_leaderboard/`: Web dashboard source.
