# HuggingFace Model Benchmarking Notebook

A comprehensive Jupyter notebook for testing multiple LLM models from HuggingFace Inference API and generating benchmarks using the HumanEvalComm evaluation framework.

## 🎯 Overview

This notebook provides a complete pipeline for:
- **Model Testing**: Evaluate multiple HuggingFace code generation models
- **Communication Assessment**: Test models' ability to ask clarifying questions
- **Comprehensive Evaluation**: Use the V2 Evaluators Framework for multi-dimensional scoring
- **Visualization**: Interactive charts and detailed analysis
- **Export**: Results in CSV, JSON, and Markdown formats

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install requirements
pip install -r requirements_notebook.txt

# Set up environment variables
cp .env.template .env
# Edit .env and add your HUGGINGFACE_API_TOKEN
```

### 2. Get HuggingFace API Token

1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a new token with "Read" permissions
3. Add it to your `.env` file:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   ```

### 3. Launch Notebook

```bash
jupyter notebook huggingface_model_benchmark.ipynb
```

### 4. Run Evaluation

1. Execute the setup cells to configure models and load data
2. Run the benchmark cells to evaluate models
3. Analyze results using visualization cells
4. Export results for further analysis

## 📊 Features

### Model Support
- **CodeLlama**: 7B and 13B instruction-tuned models
- **DeepSeek Coder**: 6.7B instruction model
- **CodeQwen**: 1.5-7B chat model
- **StarCoder2**: 7B model
- **Phi-3 Mini**: 4K instruction model
- **Extensible**: Easy to add new models

### Evaluation Metrics
- **Composite Score**: Overall code quality assessment
- **Test Pass Rate**: Functional correctness
- **Static Analysis**: Code quality, security, complexity
- **Communication Rate**: Frequency of asking clarifying questions
- **Question Quality**: Quality of clarifying questions asked
- **Execution Metrics**: Runtime performance and resource usage

### Prompt Types
- **Original** (`prompt`): Unmodified HumanEval problems
- **Ambiguous** (`prompt1a`): Problems with multiple interpretations
- **Inconsistent** (`prompt1c`): Problems with contradictory information
- **Incomplete** (`prompt1p`): Problems with missing information

### Visualization
- **Model Comparison**: Box plots and bar charts
- **Interactive Dashboard**: Plotly-based interactive visualizations
- **Performance Heatmaps**: Performance across prompt types
- **Statistical Analysis**: Significance tests and effect sizes

## 🔧 Configuration

### Model Configuration

Add new models by updating the `MODELS` dictionary:

```python
MODELS['your-model'] = ModelConfig(
    name="Your Model Name",
    model_id="huggingface/model-id",
    api_url="https://api-inference.huggingface.co/models/huggingface/model-id",
    description="Description of your model"
)
```

### Evaluation Parameters

Modify the `CONFIG` dictionary to adjust evaluation settings:

```python
CONFIG = {
    'max_tokens': 512,        # Maximum tokens to generate
    'temperature': 0.1,       # Sampling temperature
    'timeout': 30,            # API timeout in seconds
    'max_retries': 3,         # Maximum retry attempts
    'batch_size': 5,          # Batch size for processing
    'use_docker_sandbox': False,  # Enable Docker sandboxing
}
```

## 📈 Results Analysis

### Model Performance Summary

The notebook generates comprehensive performance summaries including:

- **Overall Rankings**: Models ranked by composite score
- **Communication Analysis**: Models' ability to ask clarifying questions
- **Code Quality Metrics**: Static analysis, security, and test pass rates
- **Performance Degradation**: Impact of ambiguous/incomplete prompts

### Statistical Analysis

- **Significance Testing**: Pairwise t-tests between models
- **Effect Sizes**: Cohen's d for practical significance
- **Confidence Intervals**: Statistical confidence in results

### Export Formats

Results are exported in multiple formats:

1. **CSV**: Tabular data for spreadsheet analysis
2. **JSON**: Detailed results with full metadata
3. **Markdown**: Human-readable summary report
4. **Model Summary**: Aggregated performance metrics

## 🛠️ Advanced Usage

### Custom Evaluation

Run targeted evaluations on specific problems:

```python
result = await custom_evaluation('HumanEval/0', 'codellama-7b', 'prompt1a')
```

### Batch Processing

Process large datasets efficiently with caching:

```python
results = await batch_processor.process_batch(
    benchmark=benchmark,
    problems=problems,
    models=SELECTED_MODELS,
    prompt_types=PROMPT_TYPES,
    use_cache=True
)
```

### Response Inspection

Analyze model responses in detail:

```python
inspect_model_responses(df_results, 'CodeLlama-7B-Instruct', n_samples=5)
compare_models_on_problem(df_results, 'HumanEval/0', 'prompt1a')
get_best_worst_problems(df_results, 'CodeLlama-7B-Instruct')
```

## 📋 Notebook Structure

1. **Setup and Configuration**: Environment setup and imports
2. **Model Configuration**: HuggingFace model definitions
3. **Dataset Loading**: HumanEvalComm dataset processing
4. **HuggingFace Integration**: API client and inference logic
5. **Evaluation Pipeline**: Core evaluation orchestration
6. **Benchmark Execution**: Running evaluations
7. **Results Analysis**: Statistical analysis and summaries
8. **Visualization**: Charts and interactive dashboards
9. **Export and Reporting**: Multi-format result export
10. **Advanced Analysis**: Statistical significance testing
11. **Custom Evaluation**: Targeted problem evaluation
12. **Batch Processing**: Efficient large-scale processing
13. **Utilities**: Helper functions for analysis
14. **Setup Validation**: Configuration verification

## 🔍 Evaluation Process

### 1. Code Generation
- Send problem prompt to HuggingFace model
- Extract code from response or identify clarifying questions
- Handle different response formats and edge cases

### 2. Code Evaluation
- **Static Analysis**: Pylint, Bandit, Radon, MyPy
- **Dynamic Testing**: Execute generated tests
- **Sandbox Execution**: Safe code execution with resource monitoring
- **LLM Judging**: Multi-LLM consensus scoring (if API keys available)

### 3. Communication Assessment
- **Question Detection**: Identify clarifying questions in responses
- **Question Quality**: Evaluate quality of questions asked
- **Communication Rate**: Frequency of asking questions vs. generating code

### 4. Aggregation
- **Composite Scoring**: Weighted combination of all metrics
- **Confidence Intervals**: Statistical confidence in results
- **Comparative Analysis**: Model-to-model comparisons

## 🚨 Troubleshooting

### Common Issues

1. **API Token Issues**
   - Ensure your HuggingFace token has correct permissions
   - Check token is properly set in `.env` file

2. **Model Loading Errors**
   - Some models may take time to load (503 errors)
   - The notebook automatically retries with exponential backoff

3. **Rate Limiting**
   - Built-in delays between requests
   - Adjust `timeout` and `max_retries` in CONFIG if needed

4. **Memory Issues**
   - Start with smaller datasets (`max_problems=10`)
   - Use batch processing for large evaluations

5. **Evaluation Failures**
   - Check that evaluators dependencies are installed
   - Ensure Docker is available if using sandbox mode

### Performance Tips

- **Use Caching**: Enable caching for large evaluations
- **Batch Processing**: Use batch processor for efficiency
- **Selective Models**: Test with fewer models initially
- **Progressive Evaluation**: Start small, then scale up

## 📚 Integration with Existing Framework

This notebook seamlessly integrates with the existing HumanEvalComm framework:

- **V2 Evaluators**: Uses [`evaluators/`](evaluators/) package
- **Configuration**: Leverages [`config.yaml`](config.yaml) settings
- **Dataset**: Works with [`Benchmark/HumanEvalComm.jsonl`](Benchmark/HumanEvalComm.jsonl)
- **Results Format**: Compatible with existing result processing scripts

## 🤝 Contributing

To add new models or evaluation metrics:

1. **New Models**: Add to `MODELS` dictionary with proper configuration
2. **New Metrics**: Extend `EvaluationResult` dataclass and evaluation pipeline
3. **New Visualizations**: Add functions to visualization section
4. **New Analysis**: Extend analysis functions with additional insights

## 📄 License

This notebook is part of the HumanEvalComm project. Please refer to the main project license.

## 🙏 Acknowledgments

Built on top of the HumanEvalComm framework by Wu, Jie JW and Fard, Fatemeh H.

**Citation:**
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

**Happy Benchmarking! 🎉**