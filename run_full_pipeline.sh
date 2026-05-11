#!/bin/bash

# Full HumanEvalComm V2 Benchmark Pipeline
# Evaluates Top 10 Models via OpenRouter on all available datasets

LOG_FILE="full_run.log"
echo "==========================================================" | tee -a "$LOG_FILE"
echo "🚀 Starting Full HumanEvalComm V2 Benchmark Pipeline" | tee -a "$LOG_FILE"
echo "Date: $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

MODELS="--models gpt4o:openai/gpt-4o \
  --models claude_haiku:anthropic/claude-3-haiku \
  --models claude_opus:anthropic/claude-opus-4.6 \
  --models gemini_flash:google/gemini-3-flash-preview \
  --models llama70b:meta-llama/llama-3.3-70b-instruct \
  --models llama8b:meta-llama/llama-3.1-8b-instruct \
  --models qwencoder:qwen/qwen3-coder-next \
  --models deepseek:deepseek/deepseek-v3.2 \
  --models mistral:mistralai/mistral-large-2512 \
  --models hermes:nousresearch/hermes-3-llama-3.1-70b"

# 1. Unfeasible Benchmark (Pushback Rate, FailFast)
echo "" | tee -a "$LOG_FILE"
echo "----------------------------------------------------------" | tee -a "$LOG_FILE"
echo "▶️ Step 1: Running Unfeasible Benchmark (Pushback & FailFast)" | tee -a "$LOG_FILE"
echo "----------------------------------------------------------" | tee -a "$LOG_FILE"
mkdir -p results/unfeasible
venv/bin/python3 src/v2_benchmark.py \
  --dataset-path Benchmark/HumanEvalComm_Unfeasible.jsonl \
  --api-provider openrouter \
  $MODELS \
  --max-problems 1000 \
  --output-dir results/unfeasible 2>&1 | tee -a "$LOG_FILE"

# 2. Standard Benchmark (Comm Rate, Pass@1, etc.)
echo "" | tee -a "$LOG_FILE"
echo "----------------------------------------------------------" | tee -a "$LOG_FILE"
echo "▶️ Step 2: Running Standard Benchmark (Comm Rate & Execution)" | tee -a "$LOG_FILE"
echo "----------------------------------------------------------" | tee -a "$LOG_FILE"
mkdir -p results/standard
venv/bin/python3 src/v2_benchmark.py \
  --dataset-path Benchmark/HumanEvalComm_v2.jsonl \
  --api-provider openrouter \
  $MODELS \
  --max-problems 1000 \
  --output-dir results/standard 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"
echo "✅ Full Pipeline Execution Complete!" | tee -a "$LOG_FILE"
echo "Date: $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"
