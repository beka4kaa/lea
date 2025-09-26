#!/usr/bin/env python3
"""
Production server for MCP UI Aggregator
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Start the server"""
    logger.info("Starting MCP UI Aggregator...")
    
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    
    # Ensure data directory exists
    Path('data').mkdir(exist_ok=True)
    
    # Start server
    try:
        import uvicorn
        from mcp_ui_aggregator.api.app import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()