#!/bin/bash
# Development server launcher
# Usage: ./scripts/run_dev.sh

set -e

echo "Starting AI Reflection Service (development mode)..."
echo "Docs: http://localhost:8000/docs"

uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level debug
