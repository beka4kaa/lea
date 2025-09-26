"""Core configuration for MCP UI Aggregator."""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./mcp_ui_aggregator.db",
        env="DATABASE_URL",
        description="Database connection URL"
    )
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # MCP Server
    mcp_server_name: str = Field(default="mcp-ui-aggregator", env="MCP_SERVER_NAME")
    mcp_server_version: str = Field(default="0.1.0", env="MCP_SERVER_VERSION")
    
    # Search
    enable_vector_search: bool = Field(default=False, env="ENABLE_VECTOR_SEARCH")
    vector_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        env="VECTOR_MODEL"
    )
    
    # Data directories
    data_dir: Path = Field(default=Path("./data"), env="DATA_DIR")
    cache_dir: Path = Field(default=Path("./cache"), env="CACHE_DIR")
    
    # Ingestion
    mui_docs_url: str = Field(
        default="https://mui.com/material-ui/",
        env="MUI_DOCS_URL"
    )
    shadcn_docs_url: str = Field(
        default="https://ui.shadcn.com/docs/",
        env="SHADCN_DOCS_URL"
    )
    chakra_docs_url: str = Field(
        default="https://chakra-ui.com/docs/",
        env="CHAKRA_DOCS_URL"
    )
    antd_docs_url: str = Field(
        default="https://ant.design/components/",
        env="ANTD_DOCS_URL"
    )
    mantine_docs_url: str = Field(
        default="https://mantine.dev/core/",
        env="MANTINE_DOCS_URL"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

# Ensure data directories exist
settings.data_dir.mkdir(exist_ok=True, parents=True)
settings.cache_dir.mkdir(exist_ok=True, parents=True)