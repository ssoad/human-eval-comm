
# HumanEvalComm: Benchmarking the Communication Skills of Code Generation for LLMs and LLM Agent

<div align="center">

<a href='https://huggingface.co/datasets/jie-jw-wu/HumanEvalComm'>
<img src="https://github.com/user-attachments/assets/3f62b151-d08f-4641-8d10-cc53024ec2c4" alt="HumanEvalComm" height=300></img>
</a>
<br></br>
  <a href="https://arxiv.org/abs/2406.00215"><img src="https://img.shields.io/badge/Paper%20on%20Arxiv-000?logoColor=FFE165&logo=arxiv&style=for-the-badge" alt="Paper on Arxiv"></a>
  <a href="https://huggingface.co/datasets/jie-jw-wu/HumanEvalComm"><img src="https://img.shields.io/badge/HuggingFace%20Dataset-000?logoColor=FFE165&logo=huggingface&style=for-the-badge" alt="Dataset"></a>
  <a href="https://jie-jw-wu.github.io/assets/PosterHumanEvalComm.pdf"><img src="https://img.shields.io/badge/One%20Pager-000?logo=googledocs&logoColor=FFE165&style=for-the-badge" alt="Check out the poster"></a>
  <a href="https://github.com/jie-jw-wu/human-eval-comm/stargazers"><img src="https://img.shields.io/github/stars/jie-jw-wu/human-eval-comm?style=for-the-badge&color=blue" alt="Stargazers"></a>
  <hr>
</div>

## Dataset Description

HumanEvalComm is a benchmark dataset for evaluating the communication skills of Large Language Models (LLMs) in code generation tasks. It is built upon the widely used [HumanEval benchmark](https://github.com/openai/human-eval). HumanEvalComm contains 762 modified problem descriptions based on the 164 problems in the HumanEval dataset. The modifications are created by applying one or a combination of the aforementioned clarification types. Each modified problem description is manually verified to ensure it triggers clarifying questions. The goal of HumanEvalComm is to evaluate the ability of LLMs to ask clarifying questions when faced with incomplete, inconsistent, or ambiguous requirements in coding problems:
- Ambiguity: Statements in the problem descriptions are modified to have multiple interpretations. For example, changing "sort the array descendingly" to "sort the array (descendingly or ascendingly)".
- Inconsistency: Modifications are made to create contradictions between the problem description and examples. For instance, changing the output of test examples to contradict the provided textual description.
- Incompleteness: Parts of the problem description are removed to make it incomplete, requiring the model to ask questions to recover the missing content.

| Clarification Category | *Ambiguity* | *Inconsistency* | *Incompleteness* | **Count** |
|------------------------|:-----------:|:---------------:|:----------------:|:---------:|
| 1a                     |      ✔️      |                 |                  |    164    |
| 1c                     |              |       ✔️        |                  |    164    |
| 1p                     |              |                 |        ✔️        |    164    |
| 2ac                    |      ✔️      |       ✔️        |                  |    162    |
| 2cp                    |              |       ✔️        |        ✔️        |     34    |
| 2ap                    |      ✔️      |                 |        ✔️        |     74    |
| **Total**              |     --     |      --        |        --       |    762    |
<sub>
*Note*: The smaller size for 2ac (same applies for 2cp and 2ap) is because we directly applied a combination of two clarification types from 1a, 1c strictly, and we create a new modified problem as 2ac only if applying a combination of 1a and 1c leads to a new problem description that is different from either 1a or 1c. 2cp and 2ap have smaller counts because the ambiguous (a) or inconsistent (c) parts are removed in (p) for a large number of problems.
</sub>

## Example
Below is an example of HumanEvalComm built upon HumanEval. The modified problem descriptions are shown in this table for problem number 42 of HumanEval. Specifically, the descriptions of the problem were modified to be inconsistent, ambiguous, or incomplete. The main goal of the HumanEvalComm dataset is to evaluate the degree of communication.

<img width="728" alt="ex" src="https://github.com/user-attachments/assets/123a2de8-0da5-429b-80e3-a9637caafcaa" />

## Getting Started
### Setup
To use LLM-based evaluator, you need to set `OPENAI_KEY` variables. 
```bash
export OPENAI_KEY='...'
```

### Install the necessary requirements
Install the dependencies that you need to run the code:
```bash
pip install requirements.txt
```

### Inference and Evaluation
The main script to run the evaluation is `./scripts/script_stepwise_phase123.bat`. Below is the command:
```bash
./scripts/script_stepwise_phase123.bat {models} {phase} {starting_problem_num} {ending_problem_num}
```
`{models}` must point to the model that you want to use to run the evaluation.
`{phase}` defines the phase to be executed in the evaluation. Below are the values of `phase` in the 
`{starting_problem_num} {ending_problem_num}` define the indices of the first and last problems that the evaluation must be run on.

evaluation:
- 0: run models to get the initial response of the given model for either HumanEvalComm or HumanEval. output: file in log/
- 1: the initial responses of the model from the previous step are evaluated by the LLM-based evaluator (for HumanEvalComm only). output: file in log/
- 2: run models again to get the 2nd response based on the responses got from LLM-based evaluator output (for HumanEvalComm only). output: file in log/
- 3: extract code and run test cases and other metrics for each problem. input: file in log/  output: file in log/record/
- 4: compute more metrics for each problem, such as test pass rate, question quality rate, comm. rate, etc. input: file in ./log/record/ output: file in ./result_data/
- 5: aggregate and display metrics for all problems. output: files in table/
- 6: aggregate and display metrics for each clarification category for all problems. output: files in table/ 

Here are some examples:
```bash
#phase 0:
    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 0 0 5 HumanEval
#phase 1:
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat Meta-Llama-3-8B-Instruct CodeLlama-13b-Instruct-hf" 1 0 -1 HumanEvalComm prompt1
#phase 2 (for HumanEvalComm):
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf CodeQwen1.5-7B-Chat" 2 0 5 HumanEvalComm
#analyze remaining open models (on HumanEvalComm):
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 3
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 4
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 5
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 6
#run original problem without modification:
    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 0 0 165 HumanEval
    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 3-1 0 165 HumanEval
    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 4-1 0 165 HumanEval
    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 5-1 0 165 HumanEval
#phase 5:
    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf CodeLlama-7b-Instruct-hf gpt-3.5-turbo-0125 Okanagan" 5

```

If you want to run the same commands but for linux environment, you must change the script_stepwise_phase123.bat file with script_stepwise_phase123_unix.sh

The steps 0 and 2 require GPU in order to run the model inference while evaluating on the provided benchmark. The rest of the steps do not require GPU power, and can be simply run on CPU.

For that reason, we present below scripts on how to run the steps 0 and 2 on GPU.
If you want to run an evaluation in Alliance Canada servers (or possibly other servers that support job running using sbatch) use the following commands:

In order to run the step 0 (do the initial evaluation using your model) you should use the file scripts/alliance_scripts/submit_evaluation_step_0.sh. Before running, please make the necessary modifications in them such as specifying the your model file path, etc.

Use the following command to run step 0

```
sbatch scripts/alliance_scripts/submit_evaluation_step_0.sh
```

Use the following command to run step 2

```
sbatch scripts/alliance_scripts/submit_evaluation_step_2.sh
```

For all other steps, the command is the same as mentioned above.


## Evaluation Methods and Results
The figure below shows the flowchart for the evaluation of models. For each programming problem in the HumanEvalComm, there are up to six modified problem descriptions as described earlier in Table 1. For
each modified problem, a prompt is used as the input of the model to either generate code or ask clarifying questions if needed. Then, if the model asks clarifying questions rather than generates code directly, the questions are sent to
an LLM-based Evaluator, which evaluates the questions and generates a reply to answer the questions, based on all of the available information, including the modified problem, original problem, and the clarifying questions. Finally, the
answers and the previous conversations are sent to the model to generate the code again directly. 

Besides the LLMs, we also released and evaluated a LLM agent approach, *Code Clarification and Generation Agent* (**Okanagan**), as an LLM-based agent with a multi-round structure and customized prompt for the code generation task. A key feature of Okanagan is the ability to ask clarifying questions about the input problem descriptions needed for generating correct code.

<p align="center">
  <img width="1000" alt="HumanEvalComm" src="https://github.com/jie-jw-wu/human-eval-comm/assets/122728498/9a7d2142-7ac5-4f64-8557-225e8b221dc7">
  <br>
  <i>Figure: Flowchart for the evaluation of models, either Code LLMs or Okanagan (LLM agent), in communication capability.</i>
</p>


The table below shows the evaluation result across all clarification categories on Pass@1, Test Pass Rate, communication rate, and Good Question Rate with different models on HumanEvalComm (*HmEvalComm* in the table). Additionally, the Pass@1 and Test Pass Rate on the original problems in HumanEval (*HmEval* in the table) are also shown. Top 4 results are marked as **bold**.

| Model                            | **Pass@1** | **Pass@1** | **Test Pass Rate** | **Test Pass Rate** | **Comm. Rate** | **Good Question Rate** |
|----------------------------------|------------|------------|--------------------|--------------------|----------------|------------------------|
|                                  | *HmEval*   | *HmEvalComm* | *HmEval*          | *HmEvalComm*       |            |          |
| **ChatGPT**                      | 65.58%     | 31.34%     | 76.42%             | 49.39%             | 14.21%         | 13.43%                 |
| **CodeLlama**                    | 29.88%     | 19.35%     | 45.71%             | 37.79%             | 10.16%         | 37.55%                 |
| **CodeQwen1.5 Chat**             | 76.83%     | **47.61%** | 84.4%              | **62.89%**         | 4.82%          | 41.68%                 |
| **DeepSeek Coder**               | 71.78%     | **45.68%** | 79.44%             | **62.25%**         | **30.76%**     | **61.42%**             |
| **DeepSeek Chat**                | 12.8%      | 26.32%     | 13.86%             | 44.52%             | **37.93%**     | **58.71%**             |
| **Okanagan (Base=ChatGPT)**      | 27.45%     | **39.62%** | 33.45%             | **56.98%**         | **72.73%**     | **52.24%**             |
| **Okanagan (Base=DeepSeek Coder)** | 21.25%     | **38.06%** | 24.3%              | **52.72%**         | **82.51%**     | **60.13%**             |

The figure below shows the comparison of the effectiveness of the models in Communication Rate, Good Question Rate (left), and Pass@1, Test Pass Rate (right). Note that in the right figure, the stars represent the original performance of the corresponding model with the same color in the HumanEval benchmark. This shows visually how the performance has changed when the problem description is modified.

<p align="center">
 <img width="1718" alt="scatter_plot" src="https://github.com/user-attachments/assets/c08f3d7b-e0e4-453f-93a8-8a63a8119e20" />
</p>

**_Key Finding_: More than 60% of responses from Code LLMs still generate code rather than ask questions when the problem descriptions are manually modified according to different clarification categories. Incompleteness category results in higher communication rates and Good Question Rates, but lower Pass@1 and Test Pass Rate for Code LLMs.**

## Acknowledgements
This code is heavily influenced by the Nondeterminism evaluation research of ChatGPT (https://github.com/CodeHero0/Nondeterminism-of-ChatGPT-in-Code-Generation), and by IdentityChain(https://github.com/marcusm117/IdentityChain/tree/main) on testing models including CodeLlama.

## V2 Evaluators Framework

<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
<img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg" alt="Status: Production Ready">

<br></br>

**A comprehensive framework for evaluating AI-generated code quality through multiple complementary approaches**

</div>

### Overview

The V2 Evaluators Framework provides multi-dimensional evaluation of AI-generated code quality beyond traditional test pass rates:

- **Multi-LLM Judges**: Structured evaluation from multiple language models
- **Static Analysis**: Code quality, security, and complexity metrics using Pylint, Bandit, Radon, and MyPy
- **Dynamic Testing**: Unit tests and property-based testing with Pytest and Hypothesis
- **Sandboxed Execution**: Safe code execution with Docker containers and resource monitoring
- **Confidence Calibration**: Calibrated confidence scores based on human annotations using scikit-learn
- **Composite Scoring**: Weighted aggregation of all metrics with configurable weights

### Quick Start

**🚀 Super Easy Setup (Recommended):**
```bash
# One-command setup
python setup_evaluators.py

# Or use Makefile commands
make setup          # Automated setup
make example        # Run example evaluation
make evaluate CODE='def add(a,b): return a+b'  # Evaluate code instantly
```

**📚 Quick Start Guide:**
- [example_usage.py](example_usage.py) - Simple code examples
- [evaluate_code.py](evaluate_code.py) - Command-line evaluation tool

**Manual Setup:**
```bash
# Install dependencies
pip install -r requirements_v2.txt

# Set API keys (at least one required)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GEMINI_API_KEY="your-gemini-key"

# Run the evaluators test suite
python test_evaluators.py

# Run comprehensive unit tests
python -m pytest tests/ -v
```

### Architecture

```
MultiLLMJudge → AutomatedStaticDynamic → SandboxRunner → Calibration → Aggregator
     ↓              ↓                      ↓              ↓            ↓
Async LLM      Static Analysis         Safe Execution   Confidence   Composite
Evaluation     + Dynamic Testing       + Monitoring     Calibration  Scoring
```

### Key Components

#### 1. MultiLLMJudge
Orchestrates multiple LLM judges for code evaluation with asynchronous API calls, structured JSON parsing, and consensus scoring.

#### 2. AutomatedStaticDynamic
Performs comprehensive static analysis (Pylint, Bandit, Radon, MyPy) and dynamic testing (Pytest, Hypothesis).

#### 3. SandboxRunner
Executes code safely with Docker containerization, resource limits, and monitoring.

#### 4. Calibration
Calibrates LLM confidence scores using isotonic/logistic regression based on human annotations.

#### 5. Aggregator
Combines all metrics into composite scores with configurable weights (default: Test Pass Rate 25%, LLM Consensus 20%, Static Analysis 15%, Security 15%, Readability 10%, Resource Efficiency 10%, Complexity Penalty 5%).

### Usage Example

```python
from evaluators import MultiLLMJudge, AutomatedStaticDynamic, SandboxRunner, Aggregator

# Initialize evaluators
judge = MultiLLMJudge()
analyzer = AutomatedStaticDynamic()
runner = SandboxRunner(use_docker=False)
aggregator = Aggregator()

# Evaluate code
code = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
test_code = "def test_fibonacci(): assert fibonacci(5) == 5"

static_results, dynamic_results = analyzer.analyze_code(code, test_code)
execution_result = runner.run_code(code, test_code)

evaluation = aggregator.evaluate_problem(
    problem_id="fibonacci_test",
    test_results=dynamic_results,
    static_results=static_results,
    sandbox_results=execution_result
)

print(f"Composite Score: {evaluation.composite_score:.2f}/10")
```

### Configuration

Configure LLM models in `config.yaml`:
```yaml
judge_models:
  - name: "gpt-4"
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"
  - name: "claude-3-sonnet"
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-sonnet-20240229"
  - name: "gemini-pro"
    api_key: "${GEMINI_API_KEY}"
    model: "gemini-pro"
```

## Hugging Face Benchmark Implementation

A comprehensive Jupyter notebook implementation of the HumanEvalComm V2 benchmark using Hugging Face models for multi-dimensional code generation evaluation.

### Features

- **Multi-dimensional evaluation** (Communication, Correctness, Trustworthiness, Reliability)
- **Hugging Face model integration** with quantization for efficiency
- **Comprehensive metrics calculation** including V2 composite scoring
- **Interactive visualizations** with Plotly dashboards
- **Export capabilities** for results and reports

### Supported Models
- DeepSeek Coder (6.7B, 1.3B variants)
- CodeLlama (7B, 13B variants)
- StarCoder2 (7B)
- Other Hugging Face code models

### Quick Start

```bash
# Install required packages
pip install transformers torch datasets evaluate plotly pandas numpy scikit-learn

# Open notebook
jupyter notebook HumanEval_HF_Benchmark_Notebook.ipynb
```

### Key Metrics

- **Communication Rate**: % of problems where model asks clarifying questions
- **Code Correctness**: Pass@1 and test execution rates
- **Trustworthiness**: Readability, security, maintainability
- **Reliability**: Efficiency and robustness metrics
- **V2 Composite Score**: Weighted combination of all metrics

### Usage

```python
from hf_benchmark import BenchmarkEvaluator, BenchmarkConfig

config = BenchmarkConfig(
    dataset_path="Benchmark/HumanEvalComm.jsonl",
    models=["deepseek-ai/deepseek-coder-6.7b-instruct"],
    max_problems=50
)

evaluator = BenchmarkEvaluator(config)
results = evaluator.run_benchmark()
```

## V2 Benchmark Runner

A configurable command-line tool for running comprehensive HumanEvalComm V2 benchmarks with multiple models and evaluation metrics.

### Quick Start

```bash
# Run with default settings (2 models, 3 problems)
./run_v2_benchmark.sh

# Run with custom models and output directory
./run_v2_benchmark.sh --models "gpt4:gpt-4:openai" \
                      --models "claude:claude-3-sonnet:anthropic" \
                      --output-dir ./my_results \
                      --max-problems 10

# Run with custom dataset
./run_v2_benchmark.sh --dataset-path ./custom_dataset.jsonl --verbose
```

### Features

- **Multi-Model Evaluation**: Cross-evaluate models as both generators and judges
- **Configurable Parameters**: Dataset path, models, output directory, problem count, API delays
- **Comprehensive Metrics**: V2 composite scores, communication rates, test pass rates, security analysis
- **Robust API Handling**: Rate limiting, retries, and error recovery
- **Timestamped Results**: Automatic result versioning and organization

For detailed documentation, see [benchmark_v2/README.md](benchmark_v2/README.md).

## Flask Leaderboard Dashboard

An interactive web dashboard for visualizing and exploring HumanEvalComm V2 benchmark results.

### Dashboard Quick Start

```bash
# Navigate to the dashboard directory
cd flask_leaderboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard (automatically finds results in benchmark_v2/)
python app.py

# Visit http://localhost:8080
```

### Dashboard Features

- **Interactive Leaderboards**: Sortable tables with model performance metrics
- **Beautiful Charts**: Radar plots, bar charts, and heatmaps powered by Plotly
- **Detailed Analysis**: Deep-dive into individual model evaluations and problem analysis
- **Configurable Data Directory**: Set `HUMANEVAL_DATA_DIR` environment variable to use custom result locations
- **Real-time Updates**: Automatically loads the latest benchmark results

### Dashboard Configuration

By default, the dashboard looks for results in the `benchmark_v2/` directory. To use a different location:

```bash
# Use custom data directory
export HUMANEVAL_DATA_DIR="/path/to/your/results"
python app.py
```

For detailed documentation, see [flask_leaderboard/README.md](flask_leaderboard/README.md).

## Reference

Please consider citing this paper if you find this useful:

Wu, Jie JW, and Fatemeh H. Fard. "HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent." ACM Trans. Softw. Eng. Methodol. (2025).

```bibtex
@article{Wu2025HumanEvalComm,
  author = {Wu, Jie JW and Fard, Fatemeh H.},
  title = {HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent},
  journal = {ACM Trans. Softw. Eng. Methodol.},
  year = {2025},
  doi = {10.1145/3715109},
  url = {https://doi.org/10.1145/3715109}
}
```
