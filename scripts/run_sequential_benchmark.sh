#!/bin/bash

# Configuration
DATASET="Benchmark/HumanEvalComm_v2.jsonl"
OUTPUT_DIR="results_v2_sequential"
MAX_PROBLEMS=5
DELAY=20

mkdir -p $OUTPUT_DIR

# List of models to run sequentially
MODELS=(
    "Qwen3CoderFree:qwen/qwen3-coder:free:openrouter"
    "Llama3.2Free:meta-llama/llama-3.2-3b-instruct:free:openrouter"
)

echo "🚀 Starting sequential benchmark execution..."
echo "=========================================="

for MODEL in "${MODELS[@]}"; do
    MODEL_NAME=$(echo $MODEL | cut -d':' -f1)
    echo "Evaluating model: $MODEL_NAME"
    
    venv/bin/python3 src/v2_benchmark.py \
        --dataset-path "$DATASET" \
        --output-dir "$OUTPUT_DIR" \
        --api-provider openrouter \
        --models "$MODEL" \
        --max-problems $MAX_PROBLEMS \
        --request-delay $DELAY
        
    echo "------------------------------------------"
    echo "Sleeping for 60 seconds between models to clear rate limits..."
    sleep 60
done

echo "✅ All models evaluated sequentially!"
