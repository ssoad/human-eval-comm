#!/usr/bin/env python3
"""
HumanEvalComm V2 — Perfect Resumable Ollama Benchmark Runner
-----------------------------------------------------------
This script automates the full HumanEvalComm V2 benchmark process using local Ollama.
It is designed to be fully resumable, portable, and robust against interruptions.

Features:
- Auto-installation of Ollama if missing.
- Smart state management via JSON and filesystem checks.
- Real-time logging to both console and file.
- Handles both Standard and Unfeasible benchmark datasets.
"""

import os
import sys
import json
import time
import subprocess
import requests
import shutil
import logging
from pathlib import Path
from datetime import datetime

# --- Configuration ---
OLLAMA_MODELS = [
    {"name": "qwen25_coder_7b",   "ollama": "qwen2.5-coder:7b"},
    {"name": "deepseek_coder_6b", "ollama": "deepseek-coder:6.7b"},
    {"name": "codegemma_7b",      "ollama": "codegemma:7b"},
    {"name": "starcoder2_7b",     "ollama": "starcoder2:7b"},
    {"name": "codellama_7b",      "ollama": "codellama:7b-instruct"},
]

RESULTS_ROOT = Path("results_v2_ollama")
LOG_DIR = RESULTS_ROOT / "logs"
STATE_FILE = RESULTS_ROOT / "benchmark_state.json"
LOCAL_API_BASE = "http://localhost:11434/v1"
MODEL_TIMEOUT = 300
MAX_PROBLEMS = 1000

# Setup Logging
RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = LOG_DIR / f"benchmark_run_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- Helper Functions ---

def run_command(cmd, env=None, capture=False, shell=False):
    """Run a shell command and return its exit code or output."""
    logger.debug(f"Executing: {cmd if shell else ' '.join(cmd)}")
    try:
        if capture:
            result = subprocess.run(cmd, env=env, text=True, capture_output=True, shell=shell)
            return result.stdout.strip()
        else:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                bufsize=1,
                universal_newlines=True,
                shell=shell
            )
            for line in proc.stdout:
                print(line, end="", flush=True)
                # Also log to file but without the 'INFO' prefix to keep it clean
                with open(log_path, "a") as f:
                    f.write(line)
            proc.wait()
            return proc.returncode
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return 1

def check_ollama_ready():
    """Check if Ollama server is responding."""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        return resp.status_code == 200
    except:
        return False

def ensure_ollama():
    """Ensure Ollama is installed and running."""
    ollama_path = shutil.which("ollama")
    
    if not ollama_path:
        logger.info("⚠️ Ollama not found in PATH. Attempting to install...")
        if sys.platform == "darwin" or sys.platform == "linux":
            ret = run_command("curl -fsSL https://ollama.com/install.sh | sh", shell=True)
            if ret != 0:
                logger.error("❌ Failed to install Ollama. Please install it manually from https://ollama.com")
                return False
            ollama_path = shutil.which("ollama") or "/usr/local/bin/ollama"
        else:
            logger.error("❌ Auto-install not supported on this OS. Please install Ollama manually.")
            return False

    if not check_ollama_ready():
        logger.info("🚀 Starting Ollama server...")
        subprocess.Popen([ollama_path, "serve"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        
        for i in range(15):
            time.sleep(2)
            if check_ollama_ready():
                logger.info("✅ Ollama server is ready.")
                return True
        logger.error("❌ Ollama server failed to start.")
        return False
    
    logger.info("✅ Ollama is running.")
    return True

def load_state():
    """Load the current benchmark state."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load state file: {e}. Starting fresh.")
    return {
        "pulled_models": [],
        "completed_tasks": [],
        "last_update": ""
    }

def save_state(state):
    """Save the current benchmark state."""
    state["last_update"] = datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def check_task_already_done(benchmark_type, model_name, state):
    """Check if task is in state OR if result files exist on disk."""
    task_id = f"{benchmark_type}:{model_name}"
    if task_id in state["completed_tasks"]:
        return True
    
    # Check filesystem for safety (v2_benchmark generates files containing model name)
    output_dir = RESULTS_ROOT / benchmark_type
    if output_dir.exists():
        # Look for a .csv or .json file that contains the model name
        for file in output_dir.glob(f"v2_fixed_results_*{model_name}*.json"):
            logger.info(f"🔍 Found existing result file for {task_id}: {file.name}")
            return True
    return False

def run_benchmark_for_model(benchmark_type, model_info):
    """Run the benchmark for a specific model and task."""
    dataset_map = {
        "standard": "Benchmark/HumanEvalComm_v2.jsonl",
        "unfeasible": "Benchmark/HumanEvalComm_Unfeasible.jsonl"
    }
    
    dataset_path = Path(dataset_map[benchmark_type])
    if not dataset_path.exists():
        logger.error(f"❌ Dataset not found: {dataset_path}")
        return False
        
    output_dir = RESULTS_ROOT / benchmark_type
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Arg format: name|ollama_tag|provider|max_tokens|temperature
    model_arg = f"{model_info['name']}|{model_info['ollama']}|local|1024|0.1"
    
    cmd = [
        sys.executable, "src/v2_benchmark.py",
        "--dataset-path", str(dataset_path),
        "--api-provider", "local",
        "--max-problems", str(MAX_PROBLEMS),
        "--request-delay", "0",
        "--model-timeout", str(MODEL_TIMEOUT),
        "--output-dir", str(output_dir),
        "--models", model_arg
    ]
    
    env = os.environ.copy()
    env["LOCAL_API_BASE"] = LOCAL_API_BASE
    
    logger.info(f"\n{'='*60}\nTASK: {benchmark_type.upper()} | MODEL: {model_info['name']}\n{'='*60}")
    returncode = run_command(cmd, env=env)
    return returncode == 0

# --- Main Execution ---

def main():
    try:
        logger.info("🌟 Starting Perfect HumanEvalComm V2 Runner")
        
        if not ensure_ollama():
            sys.exit(1)
            
        state = load_state()
        
        # Phase 1: Pulling Models
        logger.info("\n--- Phase 1: Model Availability ---")
        for m in OLLAMA_MODELS:
            if m["ollama"] in state["pulled_models"]:
                logger.info(f"⏩ {m['ollama']} already pulled.")
                continue
                
            logger.info(f"⬇️ Pulling {m['ollama']}...")
            ret = run_command(["ollama", "pull", m["ollama"]])
            if ret == 0:
                state["pulled_models"].append(m["ollama"])
                save_state(state)
            else:
                logger.warning(f"⚠️ Pulling {m['ollama']} returned code {ret}. Proceeding anyway.")

        # Phase 2: Run Benchmarks
        tasks = ["standard", "unfeasible"]
        
        for task_type in tasks:
            logger.info(f"\n--- Phase 2: {task_type.upper()} Benchmark ---")
            for m in OLLAMA_MODELS:
                task_id = f"{task_type}:{m['name']}"
                
                if check_task_already_done(task_type, m["name"], state):
                    logger.info(f"⏩ {task_id} already completed. Skipping.")
                    if task_id not in state["completed_tasks"]:
                        state["completed_tasks"].append(task_id)
                        save_state(state)
                    continue
                
                success = run_benchmark_for_model(task_type, m)
                if success:
                    state["completed_tasks"].append(task_id)
                    save_state(state)
                    logger.info(f"✅ Successfully finished {task_id}")
                else:
                    logger.error(f"❌ Failed {task_id}. Stopping for manual inspection.")
                    logger.info("💡 You can resume the process later by running this script again.")
                    sys.exit(1)

        logger.info("\n" + "✨"*20)
        logger.info("🏆 ALL BENCHMARKS COMPLETED!")
        logger.info(f"Results are in: {RESULTS_ROOT.absolute()}")
        logger.info(f"Detailed logs: {log_path.absolute()}")
        logger.info("✨"*20)

    except KeyboardInterrupt:
        logger.info("\n🛑 Process interrupted by user. Saving state and exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
