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
    """Root endpoint."""
    return {
        "name": "MCP UI Aggregator",
        "version": "0.1.0",
        "description": "A Model Context Protocol server for UI component management",
        "mcp_server": settings.mcp_server_name,
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp",
            "docs": "/docs",
            "redoc": "/redoc",
        }
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mcp_ui_aggregator.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )