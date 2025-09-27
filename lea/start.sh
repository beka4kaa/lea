#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt

# Start the FastAPI application
exec uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
