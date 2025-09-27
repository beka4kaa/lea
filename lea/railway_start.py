#!/usr/bin/env python3
"""
Railway-specific entry point
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, "/app")
sys.path.insert(0, os.getcwd())

if __name__ == "__main__":
    try:
        # Get port from Railway environment
        port = int(os.environ.get("PORT", 8000))
        
        # Import and run the app
        import uvicorn
        uvicorn.run(
            "mcp_ui_aggregator.api.app:app",
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)