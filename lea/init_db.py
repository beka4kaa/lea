#!/usr/bin/env python3
"""Initialize database with demo data for production deployment."""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


async def init_database():
    """Initialize database with schema and basic data."""
    try:
        logger.info("Creating database tables...")
        
        # Import and create tables
        from mcp_ui_aggregator.core.database import create_tables
        await create_tables()
        logger.info("Database tables created successfully")
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.exception(e)
        return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    success = asyncio.run(init_database())
    sys.exit(0 if success else 1)