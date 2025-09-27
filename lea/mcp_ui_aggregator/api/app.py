"""FastAPI application for MCP UI Aggregator."""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_ui_aggregator.core.config import settings
from mcp_ui_aggregator.core.database import get_session, create_tables
from mcp_ui_aggregator.api.providers_api_simple import router as providers_router
from mcp_ui_aggregator.api.mcp_bridge import router as mcp_router
from mcp_ui_aggregator.api.blocks_api import router as blocks_router
from mcp_ui_aggregator.api.mcp_discovery import router as discovery_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting MCP UI Aggregator...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down MCP UI Aggregator...")


# Create FastAPI app
app = FastAPI(
    title="MCP UI Aggregator",
    description="A Model Context Protocol server for UI component management",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configured for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
async def root():
    """Root endpoint with AI agent integration information."""
    return {
        "name": "LEA UI Components MCP Server",
        "version": "1.0.0",
        "description": "Production-ready UI component aggregator with 66 components from 11 providers",
        "mcp_server": settings.mcp_server_name,
        "protocol": "MCP 2024-11-05 (JSON-RPC 2.0)",
        "components": {
            "total": 66,
            "providers": {
                "count": 11,
                "active": ["magicui", "shadcn", "daisyui", "reactbits", "tremor", "nextui", "chakra", "mantine", "antd", "arco", "semi"]
            },
            "enhanced_features": [
                "Production-ready TSX code with TypeScript interfaces",
                "Interactive components (forms, modals, galleries, calculators)",
                "Enhanced template system for consistent code quality",
                "Framer Motion animations support",
                "Tailwind CSS v4 compatibility"
            ]
        },
        "ai_agent_integration": {
            "auto_discovery": "GET /mcp-discovery - Complete server capabilities and examples",
            "tools_manifest": "GET /mcp-tools-manifest.json - Standard MCP tools specification",
            "quick_start": "Use search_component with natural language queries",
            "documentation": "https://github.com/beka4kaa/lea/blob/main/MCP_AI_AGENT_GUIDE.md",
            "example_query": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "search_component",
                    "arguments": {"query": "animated button with hover effects", "limit": 5}
                }
            }
        },
        "endpoints": {
            "mcp": "/mcp",
            "discovery": "/mcp-discovery",
            "tools_manifest": "/mcp-tools-manifest.json",
            "status": "/mcp-status",
            "health": "/health",
            "openapi": "/openapi-mcp.json",
            "docs": "/docs",
            "redoc": "/redoc",
            "api_v1": "/api/v1"
        },
        "tools_available": [
            "search_component",
            "get_component_code", 
            "list_components",
            "get_component_docs",
            "get_block",
            "install_plan",
            "verify"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "server": settings.mcp_server_name,
        "version": "0.1.0",
        "database": "connected"
    }


# Include routers
app.include_router(providers_router, prefix="/api/v1")
app.include_router(mcp_router, prefix="")
app.include_router(blocks_router, prefix="/api/v1")
app.include_router(discovery_router, prefix="")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mcp_ui_aggregator.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )