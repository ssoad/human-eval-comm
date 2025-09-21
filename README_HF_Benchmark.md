# HumanEvalComm V2 Benchmark - Hugging Face Implementation

A comprehensive Jupyter notebook implementation of the HumanEvalComm V2 benchmark using Hugging Face models for multi-dimensional code generation evaluation.

## 📋 Overview

This notebook implements the complete HumanEvalComm V2 benchmark pipeline as outlined in the `HumanEval_HF_Benchmark_Plan.md`, featuring:

- **Multi-dimensional evaluation** (Communication, Correctness, Trustworthiness, Reliability)
- **Hugging Face model integration** with quantization for efficiency
- **Comprehensive metrics calculation** including V2 composite scoring
- **Interactive visualizations** with Plotly dashboards
- **Export capabilities** for results and reports

## 🚀 Features

### Core Components
- **Dataset Loading**: Robust JSONL dataset loading with validation
- **Model Interface**: Unified Hugging Face model interface with 4-bit quantization
- **Evaluation Pipeline**: Complete multi-dimensional evaluation system
- **Results Analysis**: Comprehensive analysis and visualization tools
- **Export System**: Multiple export formats (CSV, JSON, reports)

### Metrics Evaluated
- **Communication Rate**: Ability to ask clarifying questions
- **Code Correctness**: Pass@1 and test execution rates
- **Trustworthiness**: Readability, security, maintainability
- **Reliability**: Efficiency and robustness metrics
- **V2 Composite Score**: Weighted combination of all metrics

### Supported Models
- DeepSeek Coder (6.7B, 1.3B variants)
- CodeLlama (7B, 13B variants)
- StarCoder2 (7B)
- Other Hugging Face code models

## 📦 Installation

```bash
# Install required packages
pip install transformers torch datasets evaluate plotly pandas numpy scikit-learn matplotlib seaborn
pip install sentencepiece protobuf

# For GPU support (optional)
pip install accelerate
```

## 🏃‍♂️ Quick Start

1. **Open the notebook**:
   ```bash
   jupyter notebook HumanEval_HF_Benchmark_Notebook.ipynb
   ```

2. **Configure the benchmark**:
   ```python
   config = BenchmarkConfig(
       dataset_path="Benchmark/HumanEvalComm.jsonl",
       max_problems=50,  # Start with subset for testing
       output_dir="hf_benchmark_results"
   )
   ```

3. **Run the evaluation**:
   ```python
   # Initialize evaluator
   evaluator = BenchmarkEvaluator(config)
   evaluator.load_models()

   # Run benchmark
   results = evaluator.run_benchmark(problems)
   ```

4. **Analyze results**:
   ```python
   # Create visualizations
   analyzer = ResultsAnalyzer(results)
   dashboard = analyzer.plot_comprehensive_dashboard()
   dashboard.show()
   ```

## 📊 Usage Examples

### Basic Evaluation
```python
# Load dataset
loader = DatasetLoader(config)
problems = loader.load_dataset()

# Initialize model
model = HFModelInterface("deepseek-ai/deepseek-coder-1.3b-instruct")
model.load_model()

# Generate solution
solution = model.generate_solution(problem)
```

### Custom Model List
```python
config = BenchmarkConfig(
    models=[
        "deepseek-ai/deepseek-coder-6.7b-instruct",
        "codellama/CodeLlama-7b-Instruct-hf",
        "microsoft/DialoGPT-medium"
    ]
)
```

### Export Results
```python
exporter = ResultsExporter(analyzer, config.output_dir)
files = exporter.export_all()  # CSV, JSON, and text reports
```

## 📈 Output Formats

### 1. Leaderboard CSV
- Ranked model comparison
- All metrics included
- Ready for further analysis

### 2. Detailed Results JSON
- Individual problem evaluations
- Raw model outputs
- Timing information

### 3. Summary Report
- Human-readable analysis
- Key insights and recommendations
- Statistical summaries

### 4. Interactive Visualizations
- Comprehensive dashboard
- Radar charts for multi-dimensional comparison
- Performance heatmaps

## 🔧 Configuration Options

### BenchmarkConfig Parameters
- `dataset_path`: Path to HumanEvalComm JSONL file
- `models`: List of Hugging Face model names
- `max_problems`: Limit number of problems (None for all)
- `output_dir`: Directory for saving results

### Model Interface Options
- `model_name`: Hugging Face model identifier
- `device`: "cpu", "cuda", or "auto"
- `quantization`: 4-bit quantization for memory efficiency

## 📋 Benchmark Steps

1. **Dataset Preparation**
   - Load HumanEvalComm problems
   - Validate data structure
   - Prepare for evaluation

2. **Model Inference**
   - Load Hugging Face models
   - Generate clarifying questions
   - Produce code solutions

3. **Multi-dimensional Evaluation**
   - Communication metrics
   - Code correctness testing
   - Trustworthiness analysis
   - Reliability assessment

4. **Results Analysis**
   - Calculate composite scores
   - Generate visualizations
   - Create leaderboard

5. **Export & Reporting**
   - Save results in multiple formats
   - Generate summary reports
   - Export interactive charts

## 🎯 Key Metrics

### Communication Metrics
- **Communication Rate**: % of problems where model asks clarifying questions
- **Question Quality**: Effectiveness of clarifying questions

### Code Correctness
- **Pass@1**: % of problems solved correctly on first attempt
- **Test Pass Rate**: % of test cases passed
- **Syntax Validity**: % of syntactically correct solutions

### Trustworthiness
- **Readability**: Code clarity and documentation
- **Security**: Absence of security vulnerabilities
- **Maintainability**: Code structure and organization

### Reliability
- **Efficiency**: Code performance and resource usage
- **Robustness**: Error handling and edge case management

### Composite Score (V2)
```
V2 Score = 0.40 × Correctness + 0.20 × Communication + 0.15 × Readability + 0.10 × Security + 0.10 × Efficiency + 0.05 × Maintainability
```

## 🔍 Troubleshooting

### Common Issues

1. **Memory Issues**
   - Use 4-bit quantization
   - Reduce batch size
   - Use smaller models for testing

2. **Model Loading Errors**
   - Check internet connection
   - Verify model names
   - Ensure sufficient disk space

3. **CUDA Issues**
   - Install PyTorch with CUDA support
   - Check GPU compatibility
   - Use CPU fallback if needed

### Performance Tips

- Start with smaller models for testing
- Use `max_problems` to limit evaluation scope
- Enable quantization for faster inference
- Save intermediate results frequently

## 📚 Dependencies

- **Core**: transformers, torch, datasets
- **Evaluation**: evaluate, scikit-learn
- **Visualization**: plotly, matplotlib, seaborn
- **Data Processing**: pandas, numpy
- **Utilities**: tqdm, pathlib

## 🤝 Contributing

To extend the benchmark:

1. Add new models to the model list
2. Implement additional evaluation metrics
3. Create new visualization types
4. Enhance export formats

## 📄 License

This implementation follows the same license as the original HumanEvalComm benchmark.

## 🔗 References

- [HumanEvalComm V2 Benchmark Plan](HumanEval_HF_Benchmark_Plan.md)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [HumanEval Benchmark](https://github.com/openai/human-eval)

---

**Happy benchmarking!** 🎉

For questions or issues, please refer to the troubleshooting section or check the Hugging Face documentation.