import uvicorn

uvicorn.run("mcp_ui_aggregator.api.app:app", host="0.0.0.0", port=8000)