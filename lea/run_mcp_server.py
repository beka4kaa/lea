#!/usr/bin/env python
"""Run the MCP server."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_ui_aggregator.api.mcp_server import mcp


if __name__ == "__main__":
    # Initialize and run the MCP server
    mcp.run()