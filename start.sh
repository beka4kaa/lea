#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="${SCRIPT_DIR}/lea"

PORT="${PORT:-8000}"

echo "Starting MCP UI Aggregator from ${APP_ROOT} on port ${PORT}"
cd "${APP_ROOT}"
export PYTHONPATH="${APP_ROOT}:${PYTHONPATH:-}"
exec uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port "${PORT}"
