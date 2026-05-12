import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1: Markdown Setup
setup_md = """# HumanEvalComm V2 Benchmark (Local Model Execution via Colab)

This notebook is configured to run the full HumanEvalComm V2 benchmark natively inside Google Colab using **100% Free Local Open-Source Models** via Ollama. 

It completely bypasses API rate limits and OpenRouter credits by pulling and running models directly in your Colab GPU instance.

## Top 5 Models Evaluated:
1. **qwen2.5-coder:7b**
2. **deepseek-coder-v2:16b**
3. **llama3.1:8b**
4. **phi3:14b**
5. **codegemma:7b**"""

nb.cells.append(nbf.v4.new_markdown_cell(setup_md))

# Cell 2: Mount Google Drive
drive_code = """# Mount Google Drive to save results persistently
from google.colab import drive
drive.mount('/content/drive')
print("\\n✅ Google Drive Mounted! All results will be saved to your Drive.")
"""
nb.cells.append(nbf.v4.new_code_cell(drive_code))

# Cell 3: Clone Repo & Install dependencies
clone_code = """import os
# Clone the repository
!git clone -b beta https://github.com/ssoad/human-eval-comm.git human-eval-comm-v2
os.chdir('human-eval-comm-v2')

# Install required dependencies
!pip install -r requirements.txt
!pip install scikit-learn nbformat statsmodels kaleido plotly
"""
nb.cells.append(nbf.v4.new_code_cell(clone_code))

# Cell 4: Setup Ollama
ollama_code = """import subprocess
import time
import os

# Set environment variable for Local API
os.environ["LOCAL_API_BASE"] = "http://localhost:11434/v1"

# Install Ollama
!curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server in background
print("Starting Ollama server...")
subprocess.Popen(["ollama", "serve"])
time.sleep(5)

# Pull Top 5 Models
models = [
    "qwen2.5-coder:7b",
    "deepseek-coder-v2:16b",
    "llama3.1:8b",
    "phi3:14b",
    "codegemma:7b"
]

for model in models:
    print(f"\\nPulling {model}...")
    !ollama pull {model}
    
print("\\nAll models downloaded and ready!")
"""
nb.cells.append(nbf.v4.new_code_cell(ollama_code))

# Cell 5: Run Unfeasible
unfeasible_code = """# Run Unfeasible Benchmark Pipeline
!mkdir -p "/content/drive/MyDrive/HumanEvalComm_V2_Results/unfeasible"

!python src/v2_benchmark.py \\
  --dataset-path Benchmark/HumanEvalComm_Unfeasible.jsonl \\
  --api-provider local \\
  --models "qwen:qwen2.5-coder:7b" \\
  --models "deepseek:deepseek-coder-v2:16b" \\
  --models "llama:llama3.1:8b" \\
  --models "phi:phi3:14b" \\
  --models "codegemma:codegemma:7b" \\
  --max-problems 1000 \\
  --output-dir "/content/drive/MyDrive/HumanEvalComm_V2_Results/unfeasible"
"""
nb.cells.append(nbf.v4.new_code_cell(unfeasible_code))

# Cell 6: Run Standard
standard_code = """# Run Standard Benchmark Pipeline
!mkdir -p "/content/drive/MyDrive/HumanEvalComm_V2_Results/standard"

!python src/v2_benchmark.py \\
  --dataset-path Benchmark/HumanEvalComm_v2.jsonl \\
  --api-provider local \\
  --models "qwen:qwen2.5-coder:7b" \\
  --models "deepseek:deepseek-coder-v2:16b" \\
  --models "llama:llama3.1:8b" \\
  --models "phi:phi3:14b" \\
  --models "codegemma:codegemma:7b" \\
  --max-problems 1000 \\
  --output-dir "/content/drive/MyDrive/HumanEvalComm_V2_Results/standard"
"""
nb.cells.append(nbf.v4.new_code_cell(standard_code))

# Cell 7: Show results
results_code = """import pandas as pd
import glob
import os

print("====== UNFEASIBLE LEADERBOARD ======")
unf_files = glob.glob('/content/drive/MyDrive/HumanEvalComm_V2_Results/unfeasible/*.csv')
if unf_files:
    latest_unf = max(unf_files, key=os.path.getctime)
    df_unf = pd.read_csv(latest_unf)
    display(df_unf)

print("\\n====== STANDARD LEADERBOARD ======")
std_files = glob.glob('/content/drive/MyDrive/HumanEvalComm_V2_Results/standard/*.csv')
if std_files:
    latest_std = max(std_files, key=os.path.getctime)
    df_std = pd.read_csv(latest_std)
    display(df_std)
"""
nb.cells.append(nbf.v4.new_code_cell(results_code))

with open('HumanEvalComm_V2_Colab.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook successfully generated with Google Drive integration!")
