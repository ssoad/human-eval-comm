# HumanEvalComm V2 Model Benchmarking System

This system provides comprehensive benchmarking for language models on coding tasks using the HumanEvalComm V2 evaluation framework. It generates leaderboards with all the metrics specified in the V2 framework.

## Features

- **Complete V2 Metrics**: Includes all 15+ metrics from the HumanEvalComm V2 specification
- **Multi-Model Support**: Benchmark multiple models simultaneously
- **Automated Evaluation**: Runs static analysis, dynamic testing, LLM judging, and hypothesis fuzzing
- **Leaderboard Generation**: Creates CSV leaderboards sorted by V2 composite score
- **Communication Metrics**: Parses communication patterns from evaluation logs

## Metrics Included

### Section 1: Core Communication Metrics
- **Communication Rate (%)**: How often the model asks clarifying questions
- **Good Question Rate (%)**: % of clarifying questions judged useful
- **Clarification Efficiency**: Avg. number of questions asked before producing final code

### Section 2: Code Correctness
- **Pass@1 (%)**: % of first attempt solutions that pass all tests
- **Test Pass Rate (%)**: Average fraction of test cases passed
- **Fuzz Test Robustness (%)**: Additional correctness via property/fuzz testing

### Section 3: Code Trustworthiness
- **Readability Score (0-100)**: From pylint/flake8 + cyclomatic complexity
- **Maintainability Index (0-100)**: Comment density, docstring presence, complexity balance
- **Security Score (0-100)**: Bandit vulnerability scan

### Section 4: Efficiency
- **Efficiency (Normalized)**: Runtime and memory usage (0-1 scale)
- **Runtime (sec)**: Execution time
- **Peak Memory (MB)**: Memory usage

### Section 5: Reliability Indicators
- **Judge Consensus Confidence (%)**: Agreement level among LLM judges
- **Calibration Gap (%)**: Difference between judge predictions and ground truth

### Section 6: Composite Score
- **HumanEvalComm V2 Score (0-100)**: Weighted average across all categories

## Usage

### 1. Prepare Model Data

Create a JSONL file with model solutions in the following format:

```jsonl
{"model_name": "GPT-4", "code": "def fibonacci(n): ...", "test_code": "...", "problem_description": "...", "problem_id": "fibonacci_gpt4"}
{"model_name": "Okanagan", "code": "def fibonacci(n): ...", "test_code": "...", "problem_description": "...", "problem_id": "fibonacci_okanagan"}
```

### 2. Run Benchmarking

```bash
cd /path/to/human-eval-comm
source venv/bin/activate
python scripts/benchmark_models.py --data your_model_data.jsonl
```

### 3. View Results

The system generates:
- `evaluation_results.jsonl`: Detailed evaluation results for each model
- `results/leaderboard.csv`: CSV leaderboard with all metrics
- `results/dashboard.html`: Web dashboard (if dashboard is run separately)

## Example Leaderboard Output

```
Model,Comm Rate,Good Q Rate,Clarification Efficiency,Pass@1,Test Pass Rate,Fuzz Test Robustness,Readability Score,Maintainability Index,Security Score,Efficiency,Runtime,Peak Memory,Judge Consensus Confidence,Calibration Gap,V2 Score
Okanagan,73%,83%,1.20,50%,61%,15.5%,80,70,70,0.78,0.60,4.67,81%,10%,75.2
GPT-4,28%,51%,2.50,49%,62%,15.5%,82,77,77,0.84,0.64,2.66,73%,15%,72.5
DeepSeek Coder,18%,43%,3.10,44%,59%,15.5%,76,65,65,0.80,0.67,-32.59,69%,20%,66.1
CodeLlama-13B,15%,39%,3.80,41%,55%,15.5%,70,60,60,0.74,0.60,8.36,62%,25%,61.3
```

## Configuration

The system uses `config.yaml` for configuration:

- **Judge Models**: Configure LLM judges for code evaluation
- **Sandbox Settings**: Docker/subprocess execution settings
- **Static Analysis Tools**: Pylint, Bandit, Radon, MyPy configurations
- **Evaluation Weights**: Weights for composite score calculation

## Communication Metrics

To include communication metrics, ensure evaluation logs are available in the `log/` directory. The system parses logs to extract:
- Question frequency
- Question quality scores
- Clarification patterns

## Extending the System

### Adding New Models
1. Generate code solutions from your model
2. Format as JSONL with required fields
3. Run benchmarking script

### Custom Metrics
Modify `scripts/benchmark_models.py` to add custom evaluation metrics.

### Different Problems
The system works with any coding problem that has:
- Python code solution
- Test cases
- Problem description

## Requirements

- Python 3.11+
- Docker (for sandboxed execution)
- Required packages in `requirements.txt`
- API keys for LLM judges (configured in `config.yaml`)

## Troubleshooting

### Common Issues

1. **LLM API Errors**: Check API keys in `config.yaml`
2. **Docker Issues**: Ensure Docker is running and accessible
3. **Import Errors**: Activate virtual environment: `source venv/bin/activate`

### Performance

- Each model evaluation takes ~5-10 seconds
- Memory usage scales with number of models
- LLM API calls are the main bottleneck

## Architecture

The benchmarking system consists of:

- **Model Benchmarker**: Orchestrates evaluation pipeline
- **V2 Evaluators**: Individual evaluation components
- **Aggregator**: Combines metrics into composite scores
- **Dashboard**: Generates visualizations and reports

## Contributing

To extend the system:
1. Add new evaluators in `evaluators/`
2. Update aggregation logic in `scripts/benchmark_models.py`
3. Modify weights in `config.yaml`
4. Test with sample data

## License

This system is part of the HumanEvalComm project. See project LICENSE for details.