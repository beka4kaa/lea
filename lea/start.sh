#!/usr/bin/env bash#!/bin/bash

set -euo pipefail# start.sh



# Update pip and install dependenciesset -e  # если что-то падает — выходим

python -m pip install --upgrade pip

pip install -r requirements.txt# Установка зависимостей (если нужно)

pip install --no-cache-dir -r requirements.txt

# Check if FastAPI app exists and start accordingly

if python - <<'PY' 2>/dev/null; then# Запускаем твой MCP сервер

import importlib.util, syspython run_mcp_server.py --host 0.0.0.0 --port $PORT
mod = importlib.util.find_spec("mcp_ui_aggregator.api.app")
sys.exit(0 if mod else 1)
PY
then
  # FastAPI app path - start with uvicorn
  exec uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
else
  # Fallback - just run the railway_start.py
  exec python railway_start.py
fi