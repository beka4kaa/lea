#!/usr/bin/env python3
"""
Alternative entry point using uvicorn module directly
"""
import os
import sys

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    # Add current directory to Python path
    sys.path.insert(0, "/app")
    
    # Run uvicorn directly
    os.system(f"python -m uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port {port}")