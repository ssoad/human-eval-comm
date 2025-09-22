# HumanEvalComm V2 Evaluators Framework# HumanEvalComm V2 Evaluators Framework# HumanEvalComm V2 Evaluators Framework# HumanEvalComm V2 Evaluators Framework# HumanEvalComm V2 Evaluators Framework



A comprehensive framework for evaluating AI-generated code quality.



## InstallationA comprehensive framework for evaluating AI-generated code quality.



```bash

pip install -r requirements_v2.txt

```## Installation<div align="center">



## Quick Start



```python```bash

from src.evaluators import MultiLLMJudge

pip install -r requirements_v2.txt

judge = MultiLLMJudge()

result = judge.evaluate_code("def add(a,b): return a+b", "Add two numbers")```[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)<div align="center"># HumanEvalComm: Benchmarking the Communication Skills of Code Generation for LLMs and LLM Agent

print(result)

```


## Quick Start[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)



```python[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/jie-jw-wu/human-eval-comm)

from src.evaluators import MultiLLMJudge



judge = MultiLLMJudge()

result = judge.evaluate_code("def add(a,b): return a+b", "Add two numbers")**A comprehensive framework for evaluating the communication competence and code quality of AI-generated code**[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)<div align="center">

print(result)

```

[📖 Documentation](#documentation) • [🚀 Quick Start](#quick-start) • [📊 Examples](#examples) • [🔧 Installation](#installation)[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)



<a href='https://huggingface.co/datasets/jie-jw-wu/HumanEvalComm'><img src="https://github.com/user-attachments/assets/3f62b151-d08f-4641-8d10-cc53024ec2c4" alt="HumanEvalComm" height=300></a>[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/jie-jw-wu/human-eval-comm)<div align="center">



</div>



---**A comprehensive framework for evaluating the communication competence and code quality of AI-generated code**[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)



## 🌟 Overview



HumanEvalComm V2 is a cutting-edge framework designed to evaluate the communication skills and code quality of Large Language Models (LLMs) and LLM-based agents in code generation tasks. Built upon the widely-used [HumanEval benchmark](https://github.com/openai/human-eval), this framework provides multi-dimensional evaluation capabilities beyond traditional pass rates.[📖 Documentation](#documentation) • [🚀 Quick Start](#quick-start) • [📊 Examples](#examples) • [🔧 Installation](#installation)[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)<a href='https://huggingface.co/datasets/jie-jw-wu/HumanEvalComm'>



### Key Features



- 🤖 **Multi-LLM Evaluation**: Structured assessment from multiple language models</div>[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/jie-jw-wu/human-eval-comm)<img src="https://github.com/user-attachments/assets/3f62b151-d08f-4641-8d10-cc53024ec2c4" alt="HumanEvalComm" height=300></img>

- 🔒 **Secure Code Analysis**: Static analysis for security, complexity, and maintainability

- 🧪 **Dynamic Testing**: Comprehensive unit and property-based testing

- 🐳 **Sandboxed Execution**: Safe code execution with Docker containerization

- 📊 **Advanced Metrics**: Communication rates, test pass rates, and composite scoring---</a>

- 🎯 **Calibration System**: Confidence calibration using human annotations

- 📈 **Interactive Dashboards**: Beautiful visualizations and leaderboards



## 📋 Table of Contents## 🌟 Overview**A comprehensive framework for evaluating the communication competence and code quality of AI-generated code**<br></br>



- [Installation](#installation)

- [Quick Start](#quick-start)

- [Framework Architecture](#framework-architecture)HumanEvalComm V2 is a cutting-edge framework designed to evaluate the communication skills and code quality of Large Language Models (LLMs) and LLM-based agents in code generation tasks. Built upon the widely-used [HumanEval benchmark](https://github.com/openai/human-eval), this framework provides multi-dimensional evaluation capabilities beyond traditional pass rates.  <a href="https://arxiv.org/abs/2406.00215"><img src="https://img.shields.io/badge/Paper%20on%20Arxiv-000?logoColor=FFE165&logo=arxiv&style=for-the-badge" alt="Paper on Arxiv"></a>

- [Core Components](#core-components)

- [Usage Examples](#usage-examples)

- [Configuration](#configuration)

- [Benchmark Datasets](#benchmark-datasets)### Key Features[📖 Documentation](#documentation) • [🚀 Quick Start](#quick-start) • [📊 Examples](#examples) • [🔧 Installation](#installation)  <a href="https://huggingface.co/datasets/jie-jw-wu/HumanEvalComm"><img src="https://img.shields.io/badge/HuggingFace%20Dataset-000?logoColor=FFE165&logo=huggingface&style=for-the-badge" alt="Dataset"></a>

- [API Reference](#api-reference)

- [Contributing](#contributing)

- [Citation](#citation)

- 🤖 **Multi-LLM Evaluation**: Structured assessment from multiple language models  <a href="https://jie-jw-wu.github.io/assets/PosterHumanEvalComm.pdf"><img src="https://img.shields.io/badge/One%20Pager-000?logo=googledocs&logoColor=FFE165&style=for-the-badge" alt="Check out the poster"></a>

## 🔧 Installation

- 🔒 **Secure Code Analysis**: Static analysis for security, complexity, and maintainability

### Option 1: Automated Setup (Recommended)

- 🧪 **Dynamic Testing**: Comprehensive unit and property-based testing</div>  <a href="https://github.com/jie-jw-wu/human-eval-comm/stargazers"><img src="https://img.shields.io/github/stars/jie-jw-wu/human-eval-comm?style=for-the-badge&color=blue" alt="Stargazers"></a>

```bash

# Clone the repository- 🐳 **Sandboxed Execution**: Safe code execution with Docker containerization

git clone https://github.com/your-username/human-eval-comm.git

cd human-eval-comm- 📊 **Advanced Metrics**: Communication rates, test pass rates, and composite scoring  <hr>



# Run automated setup- 🎯 **Calibration System**: Confidence calibration using human annotations

python scripts/setup_evaluators.py

# or- 📈 **Interactive Dashboards**: Beautiful visualizations and leaderboards---</div>

make setup

```



### Option 2: Manual Installation## 📋 Table of Contents



```bash

# Install core dependencies

pip install -r requirements_v2.txt- [Installation](#installation)## 🌟 Overview## Dataset Description



# For development features- [Quick Start](#quick-start)

pip install -e ".[dev]"

- [Framework Architecture](#framework-architecture)

# For Hugging Face integration

pip install -e ".[huggingface]"- [Core Components](#core-components)

```

- [Usage Examples](#usage-examples)HumanEvalComm V2 is a cutting-edge framework designed to evaluate the communication skills and code quality of Large Language Models (LLMs) and LLM-based agents in code generation tasks. Built upon the widely-used [HumanEval benchmark](https://github.com/openai/human-eval), this framework provides multi-dimensional evaluation capabilities beyond traditional pass rates.HumanEvalComm is a benchmark dataset for evaluating the communication skills of Large Language Models (LLMs) in code generation tasks. It is built upon the widely used [HumanEval benchmark](https://github.com/openai/human-eval). HumanEvalComm contains 762 modified problem descriptions based on the 164 problems in the HumanEval dataset. The modifications are created by applying one or a combination of the aforementioned clarification types. Each modified problem description is manually verified to ensure it triggers clarifying questions. The goal of HumanEvalComm is to evaluate the ability of LLMs to ask clarifying questions when faced with incomplete, inconsistent, or ambiguous requirements in coding problems:

### System Requirements

- [Configuration](#configuration)

- **Python**: 3.8 or higher

- **Docker**: For sandboxed execution (optional but recommended)- [Benchmark Datasets](#benchmark-datasets)- Ambiguity: Statements in the problem descriptions are modified to have multiple interpretations. For example, changing "sort the array descendingly" to "sort the array (descendingly or ascendingly)".

- **API Keys**: At least one LLM provider (OpenAI, Anthropic, or Google)

- [API Reference](#api-reference)

## 🚀 Quick Start

- [Contributing](#contributing)### Key Features- Inconsistency: Modifications are made to create contradictions between the problem description and examples. For instance, changing the output of test examples to contradict the provided textual description.

### 1. Basic Code Evaluation

- [Citation](#citation)

```python

from src.evaluators import MultiLLMJudge, AutomatedStaticDynamic, Aggregator- Incompleteness: Parts of the problem description are removed to make it incomplete, requiring the model to ask questions to recover the missing content.



# Initialize evaluators## 🔧 Installation

judge = MultiLLMJudge()

analyzer = AutomatedStaticDynamic()- 🤖 **Multi-LLM Evaluation**: Structured assessment from multiple language models

aggregator = Aggregator()

### Option 1: Automated Setup (Recommended)

# Evaluate code

code = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"- 🔒 **Secure Code Analysis**: Static analysis for security, complexity, and maintainability| Clarification Category | *Ambiguity* | *Inconsistency* | *Incompleteness* | **Count** |

test_code = "def test_fib(): assert fibonacci(5) == 5"

```bash

# Run analysis

static_results, dynamic_results = analyzer.analyze_code(code, test_code)# Clone the repository- 🧪 **Dynamic Testing**: Comprehensive unit and property-based testing|------------------------|:-----------:|:---------------:|:----------------:|:---------:|



# Get composite scoregit clone https://github.com/your-username/human-eval-comm.git

evaluation = aggregator.evaluate_problem(

    problem_id="fibonacci_test",cd human-eval-comm- 🐳 **Sandboxed Execution**: Safe code execution with Docker containerization| 1a                     |      ✔️      |                 |                  |    164    |

    test_results=dynamic_results,

    static_results=static_results

)

# Run automated setup- 📊 **Advanced Metrics**: Communication rates, test pass rates, and composite scoring| 1c                     |              |       ✔️        |                  |    164    |

print(f"Composite Score: {evaluation.composite_score:.2f}/10")

```python scripts/setup_evaluators.py



### 2. Command Line Evaluation# or- 🎯 **Calibration System**: Confidence calibration using human annotations| 1p                     |              |                 |        ✔️        |    164    |



```bashmake setup

# Evaluate code from command line

evaluate-code --code "def add(a,b): return a+b" --test "assert add(2,3) == 5"```- 📈 **Interactive Dashboards**: Beautiful visualizations and leaderboards| 2ac                    |      ✔️      |       ✔️        |                  |    162    |



# Run benchmark evaluation

./scripts/run_v2_benchmark.sh --models "gpt4:gpt-4:openai" --max-problems 10

```### Option 2: Manual Installation| 2cp                    |              |       ✔️        |        ✔️        |     34    |



### 3. Run Examples



```bash```bash## 📋 Table of Contents| 2ap                    |      ✔️      |                 |        ✔️        |     74    |

# Basic usage examples

python examples/example_usage.py# Install core dependencies



# Command-line evaluation toolpip install -r requirements_v2.txt| **Total**              |     --     |      --        |        --       |    762    |

python examples/evaluate_code.py --help

```



## 🏗️ Framework Architecture# For development features- [Installation](#installation)<sub>



```pip install -e ".[dev]"

┌─────────────────────────────────────────────────────────────────┐

│                    HumanEvalComm V2 Framework                   │- [Quick Start](#quick-start)*Note*: The smaller size for 2ac (same applies for 2cp and 2ap) is because we directly applied a combination of two clarification types from 1a, 1c strictly, and we create a new modified problem as 2ac only if applying a combination of 1a and 1c leads to a new problem description that is different from either 1a or 1c. 2cp and 2ap have smaller counts because the ambiguous (a) or inconsistent (c) parts are removed in (p) for a large number of problems.

├─────────────────────────────────────────────────────────────────┤

│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐     │# For Hugging Face integration

│  │ MultiLLM    │ -> │ Static/Dynamic  │ -> │ Sandbox     │     │

│  │ Judge       │    │ Analysis        │    │ Runner      │     │pip install -e ".[huggingface]"- [Framework Architecture](#framework-architecture)</sub>

│  └─────────────┘    └─────────────────┘    └─────────────┘     │

│         ↓                      ↓                      ↓         │```

├─────────────────────────────────────────────────────────────────┤

│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │- [Core Components](#core-components)

│  │ Calibration │ -> │ Aggregation │ -> │ Dashboard   │         │

│  │ System      │    │ Engine      │    │ & Reports   │         │### System Requirements

│  └─────────────┘    └─────────────┘    └─────────────┘         │

└─────────────────────────────────────────────────────────────────┘- [Usage Examples](#usage-examples)## Example

```

- **Python**: 3.8 or higher

## 🧩 Core Components

- **Docker**: For sandboxed execution (optional but recommended)- [Configuration](#configuration)Below is an example of HumanEvalComm built upon HumanEval. The modified problem descriptions are shown in this table for problem number 42 of HumanEval. Specifically, the descriptions of the problem were modified to be inconsistent, ambiguous, or incomplete. The main goal of the HumanEvalComm dataset is to evaluate the degree of communication.

### 1. MultiLLMJudge

- **API Keys**: At least one LLM provider (OpenAI, Anthropic, or Google)

**Purpose**: Orchestrates multiple LLM judges for comprehensive code evaluation

- [Benchmark Datasets](#benchmark-datasets)

**Features**:

- Asynchronous API calls to multiple LLM providers## 🚀 Quick Start

- Structured JSON response parsing

- Consensus scoring algorithms- [API Reference](#api-reference)<img width="728" alt="ex" src="https://github.com/user-attachments/assets/123a2de8-0da5-429b-80e3-a9637caafcaa" />

- Configurable evaluation prompts

### 1. Basic Code Evaluation

### 2. AutomatedStaticDynamic

- [Contributing](#contributing)

**Purpose**: Performs static and dynamic code analysis

```python

**Tools Included**:

- **Pylint**: Code quality and style checkingfrom src.evaluators import MultiLLMJudge, AutomatedStaticDynamic, Aggregator- [Citation](#citation)## Getting Started

- **Bandit**: Security vulnerability detection

- **Radon**: Cyclomatic complexity analysis

- **MyPy**: Type checking

- **Pytest**: Unit testing framework# Initialize evaluators### Setup

- **Hypothesis**: Property-based testing

judge = MultiLLMJudge()

### 3. SandboxRunner

analyzer = AutomatedStaticDynamic()## 🔧 InstallationTo use LLM-based evaluator, you need to set `OPENAI_KEY` variables. 

**Purpose**: Safe code execution with resource monitoring

aggregator = Aggregator()

**Capabilities**:

- Docker containerization```bash

- CPU and memory limits

- Network isolation# Evaluate code

- Timeout protection

- Resource usage trackingcode = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"### Option 1: Automated Setup (Recommended)export OPENAI_KEY='...'



### 4. Calibration Systemtest_code = "def test_fib(): assert fibonacci(5) == 5"



**Purpose**: Calibrates LLM confidence scores using human annotations```



**Methods**:# Run analysis

- Isotonic regression

- Logistic regressionstatic_results, dynamic_results = analyzer.analyze_code(code, test_code)```bash

- Platt scaling



### 5. Aggregator

# Get composite score# Clone the repository### Install the necessary requirements

**Purpose**: Combines all metrics into composite scores

evaluation = aggregator.evaluate_problem(

**Default Weights**:

- Correctness: 40%    problem_id="fibonacci_test",git clone https://github.com/your-username/human-eval-comm.gitInstall the dependencies that you need to run the code:

- Communication: 20%

- Readability: 15%    test_results=dynamic_results,

- Security: 10%

- Efficiency: 10%    static_results=static_resultscd human-eval-comm```bash

- Maintainability: 5%

)

## 📖 Usage Examples

pip install requirements.txt

### Basic Evaluation Pipeline

print(f"Composite Score: {evaluation.composite_score:.2f}/10")

```python

from src.evaluators import (```# Run automated setup```

    MultiLLMJudge,

    AutomatedStaticDynamic,

    SandboxRunner,

    Aggregator### 2. Command Line Evaluationpython scripts/setup_evaluators.py

)



# Initialize components

judge = MultiLLMJudge()```bash# or### Inference and Evaluation

analyzer = AutomatedStaticDynamic()

runner = SandboxRunner(use_docker=True)# Evaluate code from command line

aggregator = Aggregator()

evaluate-code --code "def add(a,b): return a+b" --test "assert add(2,3) == 5"make setupThe main script to run the evaluation is `./scripts/run_v2_benchmark.sh`. Below is the command:

# Your code and tests

code = '''

def binary_search(arr, target):

    """Binary search implementation"""# Run benchmark evaluation``````bash

    left, right = 0, len(arr) - 1

    while left <= right:./scripts/run_v2_benchmark.sh --models "gpt4:gpt-4:openai" --max-problems 10

        mid = (left + right) // 2

        if arr[mid] == target:```./scripts/script_stepwise_phase123.bat {models} {phase} {starting_problem_num} {ending_problem_num}

            return mid

        elif arr[mid] < target:

            left = mid + 1

        else:### 3. Run Examples### Option 2: Manual Installation```

            right = mid - 1

    return -1

'''

```bash`{models}` must point to the model that you want to use to run the evaluation.

test_code = '''

import pytest# Basic usage examples

def test_binary_search():

    assert binary_search([1, 2, 3, 4, 5], 3) == 2python examples/example_usage.py```bash`{phase}` defines the phase to be executed in the evaluation. Below are the values of `phase` in the 

    assert binary_search([1, 2, 3, 4, 5], 6) == -1

    assert binary_search([], 1) == -1

'''

# Command-line evaluation tool# Install core dependencies`{starting_problem_num} {ending_problem_num}` define the indices of the first and last problems that the evaluation must be run on.

# Run evaluations

llm_scores = judge.evaluate_code(code, "Implement binary search")python examples/evaluate_code.py --help

static_results, dynamic_results = analyzer.analyze_code(code, test_code)

sandbox_results = runner.run_code(code, test_code)```pip install -r requirements_v2.txt



# Aggregate results

final_evaluation = aggregator.evaluate_problem(

    problem_id="binary_search_implementation",## 🏗️ Framework Architectureevaluation:

    llm_scores=llm_scores,

    test_results=dynamic_results,

    static_results=static_results,

    sandbox_results=sandbox_results```# For development features- 0: run models to get the initial response of the given model for either HumanEvalComm or HumanEval. output: file in log/

)

┌─────────────────────────────────────────────────────────────────┐

print(f"Final Score: {final_evaluation.composite_score:.2f}/10")

print(f"Breakdown: {final_evaluation.score_breakdown}")│                    HumanEvalComm V2 Framework                   │pip install -e ".[dev]"- 1: the initial responses of the model from the previous step are evaluated by the LLM-based evaluator (for HumanEvalComm only). output: file in log/

```

├─────────────────────────────────────────────────────────────────┤

### Benchmark Evaluation

│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐     │- 2: run models again to get the 2nd response based on the responses got from LLM-based evaluator output (for HumanEvalComm only). output: file in log/

```python

from src.hf_multi_llm_judge import BenchmarkEvaluator, BenchmarkConfig│  │ MultiLLM    │ -> │ Static/Dynamic  │ -> │ Sandbox     │     │



# Configure benchmark│  │ Judge       │    │ Analysis        │    │ Runner      │     │# For Hugging Face integration- 3: extract code and run test cases and other metrics for each problem. input: file in log/  output: file in log/record/

config = BenchmarkConfig(

    dataset_path="data/benchmark/HumanEvalComm.jsonl",│  └─────────────┘    └─────────────────┘    └─────────────┘     │

    models=["deepseek-ai/deepseek-coder-6.7b-instruct"],

    max_problems=50,│         ↓                      ↓                      ↓         │pip install -e ".[huggingface]"- 4: compute more metrics for each problem, such as test pass rate, question quality rate, comm. rate, etc. input: file in ./log/record/ output: file in ./result_data/

    evaluation_metrics=["communication", "correctness", "efficiency"]

)├─────────────────────────────────────────────────────────────────┤



# Run evaluation│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │```- 5: aggregate and display metrics for all problems. output: files in table/

evaluator = BenchmarkEvaluator(config)

results = evaluator.run_benchmark()│  │ Calibration │ -> │ Aggregation │ -> │ Dashboard   │         │



# Display results│  │ System      │    │ Engine      │    │ & Reports   │         │- 6: aggregate and display metrics for each clarification category for all problems. output: files in table/ 

evaluator.display_results(results)

```│  └─────────────┘    └─────────────┘    └─────────────┘         │



## ⚙️ Configuration└─────────────────────────────────────────────────────────────────┘### System Requirements



### Environment Variables```



Create a `.env` file or set environment variables:Here are some examples:



```bash## 🧩 Core Components

# Required: At least one LLM provider

export OPENAI_API_KEY="your-openai-key"- **Python**: 3.8 or higher```bash

export ANTHROPIC_API_KEY="your-anthropic-key"

export GEMINI_API_KEY="your-gemini-key"### 1. MultiLLMJudge



# Optional: Custom settings**Purpose**: Orchestrates multiple LLM judges for comprehensive code evaluation- **Docker**: For sandboxed execution (optional but recommended)#phase 0:

export DOCKER_HOST="unix:///var/run/docker.sock"

export PYTHONPATH="${PYTHONPATH}:/path/to/human-eval-comm"

```

**Features**:- **API Keys**: At least one LLM provider (OpenAI, Anthropic, or Google)    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 0 0 5 HumanEval

### Configuration File

- Asynchronous API calls to multiple LLM providers

Edit `config.yaml` to customize evaluation settings:

- Structured JSON response parsing#phase 1:

```yaml

judge_models:- Consensus scoring algorithms

  - name: "gpt-4"

    api_key: "${OPENAI_API_KEY}"- Configurable evaluation prompts## 🚀 Quick Start    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat Meta-Llama-3-8B-Instruct CodeLlama-13b-Instruct-hf" 1 0 -1 HumanEvalComm prompt1

    model: "gpt-4"

    temperature: 0.1



evaluation_weights:### 2. AutomatedStaticDynamic#phase 2 (for HumanEvalComm):

  correctness: 0.40

  communication: 0.20**Purpose**: Performs static and dynamic code analysis

  readability: 0.15

  security: 0.10### 1. Basic Code Evaluation    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf CodeQwen1.5-7B-Chat" 2 0 5 HumanEvalComm

  efficiency: 0.10

  maintainability: 0.05**Tools Included**:



sandbox:- **Pylint**: Code quality and style checking#analyze remaining open models (on HumanEvalComm):

  use_docker: true

  resource_limits:- **Bandit**: Security vulnerability detection

    cpu_time_limit: 30.0

    memory_limit: 256- **Radon**: Cyclomatic complexity analysis```python    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 3

```

- **MyPy**: Type checking

## 📊 Benchmark Datasets

- **Pytest**: Unit testing frameworkfrom src.evaluators import MultiLLMJudge, AutomatedStaticDynamic, Aggregator    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 4

The framework includes several benchmark datasets in the `data/benchmark/` directory:

- **Hypothesis**: Property-based testing

- **HumanEval.jsonl**: Original HumanEval benchmark (164 problems)

- **HumanEvalComm.jsonl**: Modified problems for communication evaluation (762 problems)    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 5

- **HumanEvalComm_v2.jsonl**: Enhanced version with additional metadata

### 3. SandboxRunner

### Dataset Categories

**Purpose**: Safe code execution with resource monitoring# Initialize evaluators    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf" 6

| Category | Description | Count |

|----------|-------------|-------|

| Ambiguity | Problems with multiple interpretations | 164 |

| Inconsistency | Contradictory requirements | 164 |**Capabilities**:judge = MultiLLMJudge()#run original problem without modification:

| Incompleteness | Missing information | 164 |

| Combined | Multiple clarification types | 270 |- Docker containerization



## 📚 API Reference- CPU and memory limitsanalyzer = AutomatedStaticDynamic()    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 0 0 165 HumanEval



### MultiLLMJudge- Network isolation



```python- Timeout protectionaggregator = Aggregator()    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 3-1 0 165 HumanEval

class MultiLLMJudge:

    def __init__(self, config_path: str = "config.yaml")- Resource usage tracking

    def evaluate_code(self, code: str, problem: str) -> Dict[str, float]

    async def evaluate_batch(self, codes: List[str], problems: List[str]) -> List[Dict[str, float]]    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 4-1 0 165 HumanEval

```

### 4. Calibration System

### AutomatedStaticDynamic

**Purpose**: Calibrates LLM confidence scores using human annotations# Evaluate code    ./scripts/script_stepwise_phase123.bat "gpt-3.5-turbo-0125 Okanagan" 5-1 0 165 HumanEval

```python

class AutomatedStaticDynamic:

    def analyze_code(self, code: str, test_code: str = None) -> Tuple[Dict, Dict]

    def run_static_analysis(self, code: str) -> Dict[str, Any]**Methods**:code = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"#phase 5:

    def run_dynamic_testing(self, code: str, test_code: str) -> Dict[str, Any]

```- Isotonic regression



### SandboxRunner- Logistic regressiontest_code = "def test_fib(): assert fibonacci(5) == 5"    ./scripts/script_stepwise_phase123.bat "deepseek-coder-6.7b-instruct deepseek-llm-7b-chat CodeQwen1.5-7B-Chat CodeLlama-13b-Instruct-hf CodeLlama-7b-Instruct-hf gpt-3.5-turbo-0125 Okanagan" 5



```python- Platt scaling

class SandboxRunner:

    def __init__(self, use_docker: bool = True, config: Dict = None)

    def run_code(self, code: str, test_code: str = None) -> Dict[str, Any]

    def execute_with_limits(self, code: str, limits: Dict) -> Dict[str, Any]### 5. Aggregator

```

**Purpose**: Combines all metrics into composite scores# Run analysis```

## 🧪 Testing



Run the comprehensive test suite:

**Default Weights**:static_results, dynamic_results = analyzer.analyze_code(code, test_code)

```bash

# Run all tests- Correctness: 40%

python -m pytest tests/ -v

- Communication: 20%If you want to run the same commands but for linux environment, you must change the script_stepwise_phase123.bat file with script_stepwise_phase123_unix.sh

# Run with coverage

python -m pytest tests/ --cov=src/ --cov-report=html- Readability: 15%



# Run specific test categories- Security: 10%# Get composite score

python -m pytest tests/test_multi_llm_judge.py -v

python -m pytest tests/test_sandbox_runner.py -v- Efficiency: 10%

```

- Maintainability: 5%evaluation = aggregator.evaluate_problem(The steps 0 and 2 require GPU in order to run the model inference while evaluating on the provided benchmark. The rest of the steps do not require GPU power, and can be simply run on CPU.

## 🤝 Contributing



We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📖 Usage Examples    problem_id="fibonacci_test",

### Development Setup



```bash

# Install development dependencies### Basic Evaluation Pipeline    test_results=dynamic_results,For that reason, we present below scripts on how to run the steps 0 and 2 on GPU.

pip install -e ".[dev]"



# Run linting and formatting

black src/ examples/ tests/```python    static_results=static_resultsIf you want to run an evaluation in Alliance Canada servers (or possibly other servers that support job running using sbatch) use the following commands:

isort src/ examples/ tests/

flake8 src/ examples/ tests/from src.evaluators import (



# Run tests before submitting    MultiLLMJudge,)

python -m pytest tests/ -v

```    AutomatedStaticDynamic,



### Code Style    SandboxRunner,In order to run the step 0 (do the initial evaluation using your model) you should use the file scripts/alliance_scripts/submit_evaluation_step_0.sh. Before running, please make the necessary modifications in them such as specifying the your model file path, etc.



- Follow PEP 8 guidelines    Aggregator

- Use type hints for function signatures

- Write comprehensive docstrings)print(f"Composite Score: {evaluation.composite_score:.2f}/10")

- Add unit tests for new features



## 📄 License

# Initialize components```Use the following command to run step 0

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

judge = MultiLLMJudge()

## 🙏 Acknowledgments

analyzer = AutomatedStaticDynamic()

- Based on the [HumanEval benchmark](https://github.com/openai/human-eval)

- Inspired by research on LLM evaluation and communication competencerunner = SandboxRunner(use_docker=True)

- Built with contributions from the AI evaluation research community

aggregator = Aggregator()### 2. Command Line Evaluation```

## 📞 Support



- **Issues**: [GitHub Issues](https://github.com/jie-jw-wu/human-eval-comm/issues)

- **Discussions**: [GitHub Discussions](https://github.com/jie-jw-wu/human-eval-comm/discussions)# Your code and testssbatch scripts/alliance_scripts/submit_evaluation_step_0.sh

- **Documentation**: [Full Documentation](docs/)

code = '''

## 📖 Citation

def binary_search(arr, target):```bash```

If you use HumanEvalComm in your research, please cite:

    """Binary search implementation"""

```bibtex

@article{Wu2025HumanEvalComm,    left, right = 0, len(arr) - 1# Evaluate code from command line

  author = {Wu, Jie JW and Fard, Fatemeh H.},

  title = {HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent},    while left <= right:

  journal = {ACM Trans. Softw. Eng. Methodol.},

  year = {2025},        mid = (left + right) // 2evaluate-code --code "def add(a,b): return a+b" --test "assert add(2,3) == 5"Use the following command to run step 2

  doi = {10.1145/3715109},

  url = {https://doi.org/10.1145/3715109}        if arr[mid] == target:

}

```            return mid



---        elif arr[mid] < target:



<div align="center">            left = mid + 1# Run benchmark evaluation```



**Made with ❤️ for the AI evaluation research community**        else:



[⭐ Star us on GitHub](https://github.com/jie-jw-wu/human-eval-comm) • [📧 Contact](mailto:your-email@example.com)            right = mid - 1./scripts/run_v2_benchmark.sh --models "gpt4:gpt-4:openai" --max-problems 10sbatch scripts/alliance_scripts/submit_evaluation_step_2.sh



</div>    return -1

'''``````



test_code = '''

import pytest

def test_binary_search():### 3. Run ExamplesFor all other steps, the command is the same as mentioned above.

    assert binary_search([1, 2, 3, 4, 5], 3) == 2

    assert binary_search([1, 2, 3, 4, 5], 6) == -1

    assert binary_search([], 1) == -1

'''```bash



# Run evaluations# Basic usage examples## Evaluation Methods and Results

llm_scores = judge.evaluate_code(code, "Implement binary search")

static_results, dynamic_results = analyzer.analyze_code(code, test_code)python examples/example_usage.pyThe figure below shows the flowchart for the evaluation of models. For each programming problem in the HumanEvalComm, there are up to six modified problem descriptions as described earlier in Table 1. For

sandbox_results = runner.run_code(code, test_code)

each modified problem, a prompt is used as the input of the model to either generate code or ask clarifying questions if needed. Then, if the model asks clarifying questions rather than generates code directly, the questions are sent to

# Aggregate results

final_evaluation = aggregator.evaluate_problem(# Command-line evaluation toolan LLM-based Evaluator, which evaluates the questions and generates a reply to answer the questions, based on all of the available information, including the modified problem, original problem, and the clarifying questions. Finally, the

    problem_id="binary_search_implementation",

    llm_scores=llm_scores,python examples/evaluate_code.py --helpanswers and the previous conversations are sent to the model to generate the code again directly. 

    test_results=dynamic_results,

    static_results=static_results,```

    sandbox_results=sandbox_results

)Besides the LLMs, we also released and evaluated a LLM agent approach, *Code Clarification and Generation Agent* (**Okanagan**), as an LLM-based agent with a multi-round structure and customized prompt for the code generation task. A key feature of Okanagan is the ability to ask clarifying questions about the input problem descriptions needed for generating correct code.



print(f"Final Score: {final_evaluation.composite_score:.2f}/10")## 🏗️ Framework Architecture

print(f"Breakdown: {final_evaluation.score_breakdown}")

```<p align="center">



### Benchmark Evaluation```  <img width="1000" alt="HumanEvalComm" src="https://github.com/jie-jw-wu/human-eval-comm/assets/122728498/9a7d2142-7ac5-4f64-8557-225e8b221dc7">



```python┌─────────────────────────────────────────────────────────────────┐  <br>

from src.hf_multi_llm_judge import BenchmarkEvaluator, BenchmarkConfig

│                    HumanEvalComm V2 Framework                   │  <i>Figure: Flowchart for the evaluation of models, either Code LLMs or Okanagan (LLM agent), in communication capability.</i>

# Configure benchmark

config = BenchmarkConfig(├─────────────────────────────────────────────────────────────────┤</p>

    dataset_path="data/benchmark/HumanEvalComm.jsonl",

    models=["deepseek-ai/deepseek-coder-6.7b-instruct"],│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐     │

    max_problems=50,

    evaluation_metrics=["communication", "correctness", "efficiency"]│  │ MultiLLM    │ -> │ Static/Dynamic  │ -> │ Sandbox     │     │

)

│  │ Judge       │    │ Analysis        │    │ Runner      │     │The table below shows the evaluation result across all clarification categories on Pass@1, Test Pass Rate, communication rate, and Good Question Rate with different models on HumanEvalComm (*HmEvalComm* in the table). Additionally, the Pass@1 and Test Pass Rate on the original problems in HumanEval (*HmEval* in the table) are also shown. Top 4 results are marked as **bold**.

# Run evaluation

evaluator = BenchmarkEvaluator(config)│  └─────────────┘    └─────────────────┘    └─────────────┘     │

results = evaluator.run_benchmark()

│         ↓                      ↓                      ↓         │| Model                            | **Pass@1** | **Pass@1** | **Test Pass Rate** | **Test Pass Rate** | **Comm. Rate** | **Good Question Rate** |

# Display results

evaluator.display_results(results)├─────────────────────────────────────────────────────────────────┤|----------------------------------|------------|------------|--------------------|--------------------|----------------|------------------------|

```

│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │|                                  | *HmEval*   | *HmEvalComm* | *HmEval*          | *HmEvalComm*       |            |          |

## ⚙️ Configuration

│  │ Calibration │ -> │ Aggregation │ -> │ Dashboard   │         │| **ChatGPT**                      | 65.58%     | 31.34%     | 76.42%             | 49.39%             | 14.21%         | 13.43%                 |

### Environment Variables

│  │ System      │    │ Engine      │    │ & Reports   │         │| **CodeLlama**                    | 29.88%     | 19.35%     | 45.71%             | 37.79%             | 10.16%         | 37.55%                 |

Create a `.env` file or set environment variables:

│  └─────────────┘    └─────────────┘    └─────────────┘         │| **CodeQwen1.5 Chat**             | 76.83%     | **47.61%** | 84.4%              | **62.89%**         | 4.82%          | 41.68%                 |

```bash

# Required: At least one LLM provider└─────────────────────────────────────────────────────────────────┘| **DeepSeek Coder**               | 71.78%     | **45.68%** | 79.44%             | **62.25%**         | **30.76%**     | **61.42%**             |

export OPENAI_API_KEY="your-openai-key"

export ANTHROPIC_API_KEY="your-anthropic-key"```| **DeepSeek Chat**                | 12.8%      | 26.32%     | 13.86%             | 44.52%             | **37.93%**     | **58.71%**             |

export GEMINI_API_KEY="your-gemini-key"

| **Okanagan (Base=ChatGPT)**      | 27.45%     | **39.62%** | 33.45%             | **56.98%**         | **72.73%**     | **52.24%**             |

# Optional: Custom settings

export DOCKER_HOST="unix:///var/run/docker.sock"## 🧩 Core Components| **Okanagan (Base=DeepSeek Coder)** | 21.25%     | **38.06%** | 24.3%              | **52.72%**         | **82.51%**     | **60.13%**             |

export PYTHONPATH="${PYTHONPATH}:/path/to/human-eval-comm"

```



### Configuration File### 1. MultiLLMJudgeThe figure below shows the comparison of the effectiveness of the models in Communication Rate, Good Question Rate (left), and Pass@1, Test Pass Rate (right). Note that in the right figure, the stars represent the original performance of the corresponding model with the same color in the HumanEval benchmark. This shows visually how the performance has changed when the problem description is modified.



Edit `config.yaml` to customize evaluation settings:**Purpose**: Orchestrates multiple LLM judges for comprehensive code evaluation



```yaml<p align="center">

judge_models:

  - name: "gpt-4"**Features**: <img width="1718" alt="scatter_plot" src="https://github.com/user-attachments/assets/c08f3d7b-e0e4-453f-93a8-8a63a8119e20" />

    api_key: "${OPENAI_API_KEY}"

    model: "gpt-4"- Asynchronous API calls to multiple LLM providers</p>

    temperature: 0.1

- Structured JSON response parsing

evaluation_weights:

  correctness: 0.40- Consensus scoring algorithms**_Key Finding_: More than 60% of responses from Code LLMs still generate code rather than ask questions when the problem descriptions are manually modified according to different clarification categories. Incompleteness category results in higher communication rates and Good Question Rates, but lower Pass@1 and Test Pass Rate for Code LLMs.**

  communication: 0.20

  readability: 0.15- Configurable evaluation prompts

  security: 0.10

  efficiency: 0.10## Acknowledgements

  maintainability: 0.05

### 2. AutomatedStaticDynamicThis code is heavily influenced by the Nondeterminism evaluation research of ChatGPT (https://github.com/CodeHero0/Nondeterminism-of-ChatGPT-in-Code-Generation), and by IdentityChain(https://github.com/marcusm117/IdentityChain/tree/main) on testing models including CodeLlama.

sandbox:

  use_docker: true**Purpose**: Performs static and dynamic code analysis

  resource_limits:

    cpu_time_limit: 30.0## V2 Evaluators Framework

    memory_limit: 256

```**Tools Included**:



## 📊 Benchmark Datasets- **Pylint**: Code quality and style checking<div align="center">



The framework includes several benchmark datasets in the `data/benchmark/` directory:- **Bandit**: Security vulnerability detection



- **HumanEval.jsonl**: Original HumanEval benchmark (164 problems)- **Radon**: Cyclomatic complexity analysis<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">

- **HumanEvalComm.jsonl**: Modified problems for communication evaluation (762 problems)

- **HumanEvalComm_v2.jsonl**: Enhanced version with additional metadata- **MyPy**: Type checking<img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">



### Dataset Categories- **Pytest**: Unit testing framework<img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg" alt="Status: Production Ready">



| Category | Description | Count |- **Hypothesis**: Property-based testing

|----------|-------------|-------|

| Ambiguity | Problems with multiple interpretations | 164 |<br></br>

| Inconsistency | Contradictory requirements | 164 |

| Incompleteness | Missing information | 164 |### 3. SandboxRunner

| Combined | Multiple clarification types | 270 |

**Purpose**: Safe code execution with resource monitoring**A comprehensive framework for evaluating AI-generated code quality through multiple complementary approaches**

## 📚 API Reference



### MultiLLMJudge

**Capabilities**:</div>

```python

class MultiLLMJudge:- Docker containerization

    def __init__(self, config_path: str = "config.yaml")

    def evaluate_code(self, code: str, problem: str) -> Dict[str, float]- CPU and memory limits### Overview

    async def evaluate_batch(self, codes: List[str], problems: List[str]) -> List[Dict[str, float]]

```- Network isolation



### AutomatedStaticDynamic- Timeout protectionThe V2 Evaluators Framework provides multi-dimensional evaluation of AI-generated code quality beyond traditional test pass rates:



```python- Resource usage tracking

class AutomatedStaticDynamic:

    def analyze_code(self, code: str, test_code: str = None) -> Tuple[Dict, Dict]- **Multi-LLM Judges**: Structured evaluation from multiple language models

    def run_static_analysis(self, code: str) -> Dict[str, Any]

    def run_dynamic_testing(self, code: str, test_code: str) -> Dict[str, Any]### 4. Calibration System- **Static Analysis**: Code quality, security, and complexity metrics using Pylint, Bandit, Radon, and MyPy

```

**Purpose**: Calibrates LLM confidence scores using human annotations- **Dynamic Testing**: Unit tests and property-based testing with Pytest and Hypothesis

### SandboxRunner

- **Sandboxed Execution**: Safe code execution with Docker containers and resource monitoring

```python

class SandboxRunner:**Methods**:- **Confidence Calibration**: Calibrated confidence scores based on human annotations using scikit-learn

    def __init__(self, use_docker: bool = True, config: Dict = None)

    def run_code(self, code: str, test_code: str = None) -> Dict[str, Any]- Isotonic regression- **Composite Scoring**: Weighted aggregation of all metrics with configurable weights

    def execute_with_limits(self, code: str, limits: Dict) -> Dict[str, Any]

```- Logistic regression



## 🧪 Testing- Platt scaling### Quick Start



Run the comprehensive test suite:



```bash### 5. Aggregator**🚀 Super Easy Setup (Recommended):**

# Run all tests

python -m pytest tests/ -v**Purpose**: Combines all metrics into composite scores```bash



# Run with coverage# One-command setup

python -m pytest tests/ --cov=src/ --cov-report=html

**Default Weights**:python setup_evaluators.py

# Run specific test categories

python -m pytest tests/test_multi_llm_judge.py -v- Correctness: 40%

python -m pytest tests/test_sandbox_runner.py -v

```- Communication: 20%# Or use Makefile commands



## 🤝 Contributing- Readability: 15%make setup          # Automated setup



We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.- Security: 10%make example        # Run example evaluation



### Development Setup- Efficiency: 10%make evaluate CODE='def add(a,b): return a+b'  # Evaluate code instantly



```bash- Maintainability: 5%```

# Install development dependencies

pip install -e ".[dev]"



# Run linting and formatting## 📖 Usage Examples**📚 Quick Start Guide:**

black src/ examples/ tests/

isort src/ examples/ tests/- [examples/example_usage.py](examples/example_usage.py) - Simple code examples

flake8 src/ examples/ tests/

### Basic Evaluation Pipeline- [examples/evaluate_code.py](examples/evaluate_code.py) - Command-line evaluation tool

# Run tests before submitting

python -m pytest tests/ -v

```

```python**Manual Setup:**

### Code Style

from src.evaluators import (```bash

- Follow PEP 8 guidelines

- Use type hints for function signatures    MultiLLMJudge,# Install dependencies

- Write comprehensive docstrings

- Add unit tests for new features    AutomatedStaticDynamic,pip install -r requirements_v2.txt



## 📄 License    SandboxRunner,



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.    Aggregator# Set API keys (at least one required)



## 🙏 Acknowledgments)export OPENAI_API_KEY="your-key"



- Based on the [HumanEval benchmark](https://github.com/openai/human-eval)export ANTHROPIC_API_KEY="your-anthropic-key"

- Inspired by research on LLM evaluation and communication competence

- Built with contributions from the AI evaluation research community# Initialize componentsexport GEMINI_API_KEY="your-gemini-key"



## 📞 Supportjudge = MultiLLMJudge()



- **Issues**: [GitHub Issues](https://github.com/jie-jw-wu/human-eval-comm/issues)analyzer = AutomatedStaticDynamic()# Run the evaluators test suite

- **Discussions**: [GitHub Discussions](https://github.com/jie-jw-wu/human-eval-comm/discussions)

- **Documentation**: [Full Documentation](docs/)runner = SandboxRunner(use_docker=True)python test_evaluators.py



## 📖 Citationaggregator = Aggregator()



If you use HumanEvalComm in your research, please cite:# Run comprehensive unit tests



```bibtex# Your code and testspython -m pytest tests/ -v

@article{Wu2025HumanEvalComm,

  author = {Wu, Jie JW and Fard, Fatemeh H.},code = '''```

  title = {HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent},

  journal = {ACM Trans. Softw. Eng. Methodol.},def binary_search(arr, target):

  year = {2025},

  doi = {10.1145/3715109},    """Binary search implementation"""### Architecture

  url = {https://doi.org/10.1145/3715109}

}    left, right = 0, len(arr) - 1

```

    while left <= right:```

---

        mid = (left + right) // 2MultiLLMJudge → AutomatedStaticDynamic → SandboxRunner → Calibration → Aggregator

<div align="center">

        if arr[mid] == target:     ↓              ↓                      ↓              ↓            ↓

**Made with ❤️ for the AI evaluation research community**

            return midAsync LLM      Static Analysis         Safe Execution   Confidence   Composite

[⭐ Star us on GitHub](https://github.com/jie-jw-wu/human-eval-comm) • [📧 Contact](mailto:your-email@example.com)

        elif arr[mid] < target:Evaluation     + Dynamic Testing       + Monitoring     Calibration  Scoring

</div>
            left = mid + 1```

        else:

            right = mid - 1### Key Components

    return -1

'''#### 1. MultiLLMJudge

Orchestrates multiple LLM judges for code evaluation with asynchronous API calls, structured JSON parsing, and consensus scoring.

test_code = '''

import pytest#### 2. AutomatedStaticDynamic

def test_binary_search():Performs comprehensive static analysis (Pylint, Bandit, Radon, MyPy) and dynamic testing (Pytest, Hypothesis).

    assert binary_search([1, 2, 3, 4, 5], 3) == 2

    assert binary_search([1, 2, 3, 4, 5], 6) == -1#### 3. SandboxRunner

    assert binary_search([], 1) == -1Executes code safely with Docker containerization, resource limits, and monitoring.

'''

#### 4. Calibration

# Run evaluationsCalibrates LLM confidence scores using isotonic/logistic regression based on human annotations.

llm_scores = judge.evaluate_code(code, "Implement binary search")

static_results, dynamic_results = analyzer.analyze_code(code, test_code)#### 5. Aggregator

sandbox_results = runner.run_code(code, test_code)Combines all metrics into composite scores with configurable weights (default: Test Pass Rate 25%, LLM Consensus 20%, Static Analysis 15%, Security 15%, Readability 10%, Resource Efficiency 10%, Complexity Penalty 5%).



# Aggregate results### Usage Example

final_evaluation = aggregator.evaluate_problem(

    problem_id="binary_search_implementation",```python

    llm_scores=llm_scores,from evaluators import MultiLLMJudge, AutomatedStaticDynamic, SandboxRunner, Aggregator

    test_results=dynamic_results,

    static_results=static_results,# Initialize evaluators

    sandbox_results=sandbox_resultsjudge = MultiLLMJudge()

)analyzer = AutomatedStaticDynamic()

runner = SandboxRunner(use_docker=False)

print(f"Final Score: {final_evaluation.composite_score:.2f}/10")aggregator = Aggregator()

print(f"Breakdown: {final_evaluation.score_breakdown}")

```# Evaluate code

code = "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"

### Benchmark Evaluationtest_code = "def test_fibonacci(): assert fibonacci(5) == 5"



```pythonstatic_results, dynamic_results = analyzer.analyze_code(code, test_code)

from src.hf_multi_llm_judge import BenchmarkEvaluator, BenchmarkConfigexecution_result = runner.run_code(code, test_code)



# Configure benchmarkevaluation = aggregator.evaluate_problem(

config = BenchmarkConfig(    problem_id="fibonacci_test",

    dataset_path="data/benchmark/HumanEvalComm.jsonl",    test_results=dynamic_results,

    models=["deepseek-ai/deepseek-coder-6.7b-instruct"],    static_results=static_results,

    max_problems=50,    sandbox_results=execution_result

    evaluation_metrics=["communication", "correctness", "efficiency"])

)

print(f"Composite Score: {evaluation.composite_score:.2f}/10")

# Run evaluation```

evaluator = BenchmarkEvaluator(config)

results = evaluator.run_benchmark()### Configuration



# Display resultsConfigure LLM models in `config.yaml`:

evaluator.display_results(results)```yaml

```judge_models:

  - name: "gpt-4"

## ⚙️ Configuration    api_key: "${OPENAI_API_KEY}"

    model: "gpt-4"

### Environment Variables  - name: "claude-3-sonnet"

    api_key: "${ANTHROPIC_API_KEY}"

Create a `.env` file or set environment variables:    model: "claude-3-sonnet-20240229"

  - name: "gemini-pro"

```bash    api_key: "${GEMINI_API_KEY}"

# Required: At least one LLM provider    model: "gemini-pro"

export OPENAI_API_KEY="your-openai-key"```

export ANTHROPIC_API_KEY="your-anthropic-key"

export GEMINI_API_KEY="your-gemini-key"## Hugging Face Benchmark Implementation



# Optional: Custom settingsA comprehensive Jupyter notebook implementation of the HumanEvalComm V2 benchmark using Hugging Face models for multi-dimensional code generation evaluation.

export DOCKER_HOST="unix:///var/run/docker.sock"

export PYTHONPATH="${PYTHONPATH}:/path/to/human-eval-comm"### Features

```

- **Multi-dimensional evaluation** (Communication, Correctness, Trustworthiness, Reliability)

### Configuration File- **Hugging Face model integration** with quantization for efficiency

- **Comprehensive metrics calculation** including V2 composite scoring

Edit `config.yaml` to customize evaluation settings:- **Interactive visualizations** with Plotly dashboards

- **Export capabilities** for results and reports

```yaml

judge_models:### Supported Models

  - name: "gpt-4"- DeepSeek Coder (6.7B, 1.3B variants)

    api_key: "${OPENAI_API_KEY}"- CodeLlama (7B, 13B variants)

    model: "gpt-4"- StarCoder2 (7B)

    temperature: 0.1- Other Hugging Face code models



evaluation_weights:### Quick Start

  correctness: 0.40

  communication: 0.20```bash

  readability: 0.15# Install required packages

  security: 0.10pip install transformers torch datasets evaluate plotly pandas numpy scikit-learn

  efficiency: 0.10

  maintainability: 0.05# Open notebook

jupyter notebook HumanEval_HF_Benchmark_Notebook.ipynb

sandbox:```

  use_docker: true

  resource_limits:### Key Metrics

    cpu_time_limit: 30.0

    memory_limit: 256- **Communication Rate**: % of problems where model asks clarifying questions

```- **Code Correctness**: Pass@1 and test execution rates

- **Trustworthiness**: Readability, security, maintainability

## 📊 Benchmark Datasets- **Reliability**: Efficiency and robustness metrics

- **V2 Composite Score**: Weighted combination of all metrics

The framework includes several benchmark datasets in the `data/benchmark/` directory:

### Usage

- **HumanEval.jsonl**: Original HumanEval benchmark (164 problems)

- **HumanEvalComm.jsonl**: Modified problems for communication evaluation (762 problems)```python

- **HumanEvalComm_v2.jsonl**: Enhanced version with additional metadatafrom hf_benchmark import BenchmarkEvaluator, BenchmarkConfig



### Dataset Categoriesconfig = BenchmarkConfig(

    dataset_path="data/benchmark/HumanEvalComm.jsonl",

| Category | Description | Count |    models=["deepseek-ai/deepseek-coder-6.7b-instruct"],

|----------|-------------|-------|    max_problems=50

| Ambiguity | Problems with multiple interpretations | 164 |)

| Inconsistency | Contradictory requirements | 164 |

| Incompleteness | Missing information | 164 |evaluator = BenchmarkEvaluator(config)

| Combined | Multiple clarification types | 270 |results = evaluator.run_benchmark()

```

## 📚 API Reference

## V2 Benchmark Runner

### MultiLLMJudge

A configurable command-line tool for running comprehensive HumanEvalComm V2 benchmarks with multiple models and evaluation metrics.

```python

class MultiLLMJudge:### Quick Start

    def __init__(self, config_path: str = "config.yaml")

    def evaluate_code(self, code: str, problem: str) -> Dict[str, float]```bash

    async def evaluate_batch(self, codes: List[str], problems: List[str]) -> List[Dict[str, float]]# Run with default settings (2 models, 3 problems)

```./run_v2_benchmark.sh



### AutomatedStaticDynamic# Run with custom models and output directory

./run_v2_benchmark.sh --models "gpt4:gpt-4:openai" \

```python                      --models "claude:claude-3-sonnet:anthropic" \

class AutomatedStaticDynamic:                      --output-dir ./my_results \

    def analyze_code(self, code: str, test_code: str = None) -> Tuple[Dict, Dict]                      --max-problems 10

    def run_static_analysis(self, code: str) -> Dict[str, Any]

    def run_dynamic_testing(self, code: str, test_code: str) -> Dict[str, Any]# Run with custom dataset

```./run_v2_benchmark.sh --dataset-path ./custom_dataset.jsonl --verbose

```

### SandboxRunner

### Features

```python

class SandboxRunner:- **Multi-Model Evaluation**: Cross-evaluate models as both generators and judges

    def __init__(self, use_docker: bool = True, config: Dict = None)- **Configurable Parameters**: Dataset path, models, output directory, problem count, API delays

    def run_code(self, code: str, test_code: str = None) -> Dict[str, Any]- **Comprehensive Metrics**: V2 composite scores, communication rates, test pass rates, security analysis

    def execute_with_limits(self, code: str, limits: Dict) -> Dict[str, Any]- **Robust API Handling**: Rate limiting, retries, and error recovery

```- **Timestamped Results**: Automatic result versioning and organization



## 🧪 TestingFor detailed documentation, see [benchmark_v2/README.md](benchmark_v2/README.md).



Run the comprehensive test suite:## Flask Leaderboard Dashboard



```bashAn interactive web dashboard for visualizing and exploring HumanEvalComm V2 benchmark results.

# Run all tests

python -m pytest tests/ -v### Dashboard Quick Start



# Run with coverage```bash

python -m pytest tests/ --cov=src/ --cov-report=html# Navigate to the dashboard directory

cd flask_leaderboard

# Run specific test categories

python -m pytest tests/test_multi_llm_judge.py -v# Install dependencies

python -m pytest tests/test_sandbox_runner.py -vpip install -r requirements.txt

```

# Run the dashboard (automatically finds results in benchmark_v2/)

## 🤝 Contributingpython app.py



We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.# Visit http://localhost:8080

```

### Development Setup

### Dashboard Features

```bash

# Install development dependencies- **Interactive Leaderboards**: Sortable tables with model performance metrics

pip install -e ".[dev]"- **Beautiful Charts**: Radar plots, bar charts, and heatmaps powered by Plotly

- **Detailed Analysis**: Deep-dive into individual model evaluations and problem analysis

# Run linting and formatting- **Configurable Data Directory**: Set `HUMANEVAL_DATA_DIR` environment variable to use custom result locations

black src/ examples/ tests/- **Real-time Updates**: Automatically loads the latest benchmark results

isort src/ examples/ tests/

flake8 src/ examples/ tests/### Dashboard Configuration



# Run tests before submittingBy default, the dashboard looks for results in the `benchmark_v2/` directory. To use a different location:

python -m pytest tests/ -v

``````bash

# Use custom data directory

### Code Styleexport HUMANEVAL_DATA_DIR="/path/to/your/results"

python app.py

- Follow PEP 8 guidelines```

- Use type hints for function signatures

- Write comprehensive docstringsFor detailed documentation, see [flask_leaderboard/README.md](flask_leaderboard/README.md).

- Add unit tests for new features

## Reference

## 📄 License

Please consider citing this paper if you find this useful:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Wu, Jie JW, and Fatemeh H. Fard. "HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent." ACM Trans. Softw. Eng. Methodol. (2025).

## 🙏 Acknowledgments

```bibtex

- Based on the [HumanEval benchmark](https://github.com/openai/human-eval)@article{Wu2025HumanEvalComm,

- Inspired by research on LLM evaluation and communication competence  author = {Wu, Jie JW and Fard, Fatemeh H.},

- Built with contributions from the AI evaluation research community  title = {HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent},

  journal = {ACM Trans. Softw. Eng. Methodol.},

## 📞 Support  year = {2025},

  doi = {10.1145/3715109},

- **Issues**: [GitHub Issues](https://github.com/jie-jw-wu/human-eval-comm/issues)  url = {https://doi.org/10.1145/3715109}

- **Discussions**: [GitHub Discussions](https://github.com/jie-jw-wu/human-eval-comm/discussions)}

- **Documentation**: [Full Documentation](docs/)```


## 📖 Citation

If you use HumanEvalComm in your research, please cite:

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

---

<div align="center">

**Made with ❤️ for the AI evaluation research community**

[⭐ Star us on GitHub](https://github.com/jie-jw-wu/human-eval-comm) • [📧 Contact](mailto:your-email@example.com)

</div>