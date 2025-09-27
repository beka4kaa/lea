#!/bin/bash

# Set default port
PORT=${PORT:-8000}

# Start the MCP UI Aggregator server
exec uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port $PORT
