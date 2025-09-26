#!/bin/bash

# Start script for production deployment
set -e

echo "🚀 Starting Lea MCP Server..."

# Set default port if not provided
PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

# Try to find python executable
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ Python not found!"
        exit 1
    fi
fi

echo "🐍 Using Python: $PYTHON_CMD"

# Initialize database if it doesn't exist
if [ ! -f "mcp_ui_aggregator.db" ]; then
    echo "📊 Initializing database..."
    $PYTHON_CMD init_db.py
fi

echo "🌟 Starting server on $HOST:$PORT"

# Start the FastAPI server
exec $PYTHON_CMD -m uvicorn mcp_ui_aggregator.api.app:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers 1 \
    --access-log \
    --log-level info