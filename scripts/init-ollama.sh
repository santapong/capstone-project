#!/bin/bash
# Wait for Ollama to be ready, then pull the embedding model
set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://ollama:11434}"
MODEL="${EMBEDDING_MODEL:-bge-m3}"

echo "Waiting for Ollama at $OLLAMA_HOST..."
until curl -sf "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; do
    echo "Ollama not ready yet, retrying in 5s..."
    sleep 5
done

echo "Ollama is ready. Pulling model: $MODEL"
curl -sf "$OLLAMA_HOST/api/pull" -d "{\"name\": \"$MODEL\"}" | while read -r line; do
    echo "$line"
done

echo "Model $MODEL is ready."
