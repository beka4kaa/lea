"""Base ingestion functionality."""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_ui_aggregator.core.database import async_session_maker
from mcp_ui_aggregator.models.database import (
    Component, CodeExample, DocumentationSection, IngestionLog,
    ComponentType, Namespace
)

logger = logging.getLogger(__name__)


class BaseIngester(ABC):
    """Base class for component ingestion."""
    
    def __init__(self, namespace: Namespace, base_url: str):
        self.namespace = namespace
        self.base_url = base_url
        self.session: Optional[httpx.AsyncClient] = None
        
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "MCP-UI-Aggregator/0.1.0 (Component Documentation Ingester)"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a web page."""
        try:
            if not self.session:
                raise RuntimeError("Session not initialized")
                
            response = await self.session.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content."""
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    async def discover_components(self) -> List[str]:
        """Discover all component URLs."""
        pass
    
    @abstractmethod
    async def extract_component_data(self, component_url: str) -> Optional[Dict[str, Any]]:
        """Extract component data from a URL."""
        pass
    
    async def save_component(self, session: AsyncSession, component_data: Dict[str, Any]) -> Optional[Component]:
        """Save component data to database."""
        try:
            # Check if component exists
            existing = await session.get(Component, (component_data["name"], self.namespace.value))
            
            if existing:
                # Update existing component
                for key, value in component_data.items():
                    if hasattr(existing, key) and key not in ["id", "created_at"]:
                        setattr(existing, key, value)
                component = existing
            else:
                # Create new component
                component = Component(
                    namespace=self.namespace.value,
                    **component_data
                )
                session.add(component)
            
            await session.flush()
            
            # Save code examples
            if "code_examples" in component_data:
                # Remove existing examples
                for example in component.code_examples:
                    await session.delete(example)
                
                # Add new examples
                for example_data in component_data["code_examples"]:
                    example = CodeExample(
                        component_id=component.id,
                        **example_data
                    )
                    session.add(example)
            
            # Save documentation sections
            if "docs_sections" in component_data:
                # Remove existing sections
                for section in component.docs_sections:
                    await session.delete(section)
                
                # Add new sections
                for section_data in component_data["docs_sections"]:
                    section = DocumentationSection(
                        component_id=component.id,
                        **section_data
                    )
                    session.add(section)
            
            return component
            
        except Exception as e:
            logger.error(f"Error saving component {component_data.get('name', 'unknown')}: {e}")
            return None
    
    async def run_ingestion(self) -> Dict[str, Any]:
        """Run the full ingestion process."""
        start_time = datetime.utcnow()
        stats = {
            "components_processed": 0,
            "components_created": 0,
            "components_updated": 0,
            "errors": []
        }
        
        async with async_session_maker() as session:
            # Create ingestion log
            log = IngestionLog(
                namespace=self.namespace.value,
                source_url=self.base_url,
                status="started",
                started_at=start_time
            )
            session.add(log)
            await session.commit()
            
            try:
                # Discover components
                logger.info(f"Discovering components for {self.namespace.value}")
                component_urls = await self.discover_components()
                logger.info(f"Found {len(component_urls)} components")
                
                # Process each component
                for url in component_urls:
                    try:
                        component_data = await self.extract_component_data(url)
                        if component_data:
                            # Check if component already exists
                            existing = await session.get(Component, (component_data["name"], self.namespace.value))
                            
                            component = await self.save_component(session, component_data)
                            if component:
                                stats["components_processed"] += 1
                                if existing:
                                    stats["components_updated"] += 1
                                else:
                                    stats["components_created"] += 1
                                
                                logger.info(f"Processed component: {component.name}")
                        
                    except Exception as e:
                        error_msg = f"Error processing {url}: {str(e)}"
                        logger.error(error_msg)
                        stats["errors"].append(error_msg)
                
                # Update log with success
                log.status = "completed"
                log.completed_at = datetime.utcnow()
                log.components_processed = stats["components_processed"]
                log.components_created = stats["components_created"]
                log.components_updated = stats["components_updated"]
                
                await session.commit()
                
            except Exception as e:
                # Update log with failure
                log.status = "failed"
                log.completed_at = datetime.utcnow()
                log.error_message = str(e)
                log.components_processed = stats["components_processed"]
                log.components_created = stats["components_created"]
                log.components_updated = stats["components_updated"]
                
                await session.commit()
                raise
        
        return stats
    
    def infer_component_type(self, name: str, description: str = "") -> ComponentType:
        """Infer component type from name and description."""
        name_lower = name.lower()
        desc_lower = description.lower()
        
        # Button-related
        if any(word in name_lower for word in ["button", "btn", "fab", "icon-button"]):
            return ComponentType.BUTTON
        
        # Input-related
        if any(word in name_lower for word in ["input", "textfield", "textarea", "select", "autocomplete", "slider", "switch", "checkbox", "radio"]):
            return ComponentType.INPUT
        
        # Card-related
        if any(word in name_lower for word in ["card", "paper", "surface"]):
            return ComponentType.CARD
        
        # Modal-related
        if any(word in name_lower for word in ["modal", "dialog", "drawer", "popover", "tooltip", "snackbar", "alert"]):
            return ComponentType.MODAL
        
        # Navigation-related
        if any(word in name_lower for word in ["nav", "menu", "tabs", "breadcrumb", "stepper", "pagination"]):
            return ComponentType.NAVIGATION
        
        # Layout-related
        if any(word in name_lower for word in ["grid", "container", "box", "stack", "divider", "accordion", "collapse"]):
            return ComponentType.LAYOUT
        
        # Data display
        if any(word in name_lower for word in ["table", "list", "chip", "badge", "avatar", "progress", "skeleton"]):
            return ComponentType.DATA_DISPLAY
        
        # Feedback
        if any(word in name_lower for word in ["alert", "snackbar", "notification", "toast", "loading", "spinner"]):
            return ComponentType.FEEDBACK
        
        # Form
        if any(word in name_lower for word in ["form", "field", "validation"]):
            return ComponentType.FORM
        
        return ComponentType.OTHER
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove common prefixes/suffixes
        text = text.strip(".")
        
        return text