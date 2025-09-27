#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"

echo "Starting MCP UI Aggregator on port ${PORT}"
exec uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port "${PORT}"
