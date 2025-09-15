# 🚀 V2 Evaluators Framework - Quick Start Guide

Get up and running with the V2 Evaluators Framework in under 5 minutes!

## ⚡ Super Quick Start

### 1. **One-Command Setup**
```bash
python setup_evaluators.py
```

This script will:
- ✅ Check Python version and dependencies
- ✅ Install required packages
- ✅ Verify API keys
- ✅ Run quick functionality test
- ✅ Create environment template

### 2. **Set Your API Keys**
```bash
# Copy the template and add your keys
cp .env.template .env

# Edit .env with your API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GEMINI_API_KEY="your-gemini-key"
```

### 3. **Evaluate Code Instantly**
```bash
# Evaluate code directly
python evaluate_code.py "def add(a, b): return a + b" --problem "Add two numbers"

# Evaluate from file
python evaluate_code.py my_code.py --test my_tests.py

# Get JSON output
python evaluate_code.py my_code.py --output json

# Include LLM evaluation
python evaluate_code.py my_code.py --llm
```

## 🎯 Common Use Cases

### **Evaluate a Single Function**
```bash
python evaluate_code.py "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
```

### **Evaluate with Tests**
```bash
python evaluate_code.py fibonacci.py --test test_fibonacci.py
```

### **Full Evaluation with LLM Judges**
```bash
python evaluate_code.py solution.py --test tests.py --problem "Implement sorting algorithm" --llm
```

### **Batch Evaluation**
```bash
# Evaluate multiple files
for file in solutions/*.py; do
    echo "Evaluating $file"
    python evaluate_code.py "$file" --output json > "results/$(basename $file .py).json"
done
```

## 📊 Understanding Results

### **Composite Score (0-10)**
- **9-10**: Excellent code quality
- **7-8**: Good code quality  
- **5-6**: Average code quality
- **3-4**: Below average
- **0-2**: Poor code quality

### **Individual Metrics**
- **Test Pass Rate**: How many tests pass
- **Static Analysis**: Code quality (pylint, complexity)
- **Security Score**: Security vulnerabilities found
- **Readability**: Code clarity and maintainability
- **Resource Efficiency**: Memory and CPU usage

### **Example Output**
```json
{
  "composite_score": 7.85,
  "test_pass_rate": 8.0,
  "static_analysis_score": 8.5,
  "security_score": 9.0,
  "readability_score": 7.5,
  "resource_efficiency_score": 6.5,
  "execution_success": true,
  "execution_time": 2.3,
  "memory_used": 45.2
}
```

## 🔧 Configuration Made Easy

### **Using config.yaml**
The framework automatically loads from `config.yaml`. Key sections:

```yaml
# LLM Models (add your preferred models)
judge_models:
  - name: "gpt-4"
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"

# Evaluation Weights (customize importance)
evaluation_weights:
  test_pass_rate: 0.25
  llm_consensus: 0.20
  static_analysis: 0.15
  security_score: 0.15
```

### **Quick Configuration Changes**
```bash
# Focus on test correctness
# Edit config.yaml: test_pass_rate: 0.5

# Focus on code quality
# Edit config.yaml: static_analysis: 0.4

# Focus on security
# Edit config.yaml: security_score: 0.3
```

## 🧪 Testing Your Setup

### **Run All Tests**
```bash
python -m pytest tests/ -v
```

### **Quick Functionality Test**
```bash
python test_evaluators.py
```

### **Test Specific Components**
```bash
python -m pytest tests/test_aggregator.py -v
python -m pytest tests/test_multi_llm_judge.py -v
```

## 🚨 Troubleshooting

### **"No API keys found"**
```bash
# Set at least one API key
export OPENAI_API_KEY="your-key"
python setup_evaluators.py
```

### **"Import failed"**
```bash
# Install dependencies manually
pip install -r requirements_v2.txt
```

### **"Docker not available"**
```bash
# Framework automatically falls back to subprocess
# No action needed - it will work without Docker
```

### **"LLM evaluation failed"**
```bash
# Check API keys and network
export OPENAI_API_KEY="your-key"
python -c "import openai; print('API key works')"
```

## 📚 Next Steps

1. **Read the full documentation**: [README_Evaluators.md](README_Evaluators.md)
2. **Explore examples**: Check the `examples/` directory
3. **Customize evaluation**: Modify `config.yaml`
4. **Integrate with your workflow**: Use the Python API directly

## 💡 Pro Tips

### **For Better Results**
- Provide clear problem descriptions
- Include comprehensive test cases
- Use descriptive variable names
- Follow Python best practices

### **For Faster Evaluation**
- Use subprocess mode (no Docker required)
- Cache static analysis results
- Run evaluations in parallel
- Use async LLM calls

### **For Production Use**
- Set up proper API key management
- Use Docker for better isolation
- Monitor resource usage
- Implement result caching

---

**Need help?** Check the [full documentation](README_Evaluators.md) or run `python setup_evaluators.py` for guided setup!
