"""Chakra UI ingestion implementation."""

import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from mcp_ui_aggregator.ingestion.base import BaseIngester
from mcp_ui_aggregator.models.database import Namespace


class ChakraUIIngester(BaseIngester):
    """Ingester for Chakra UI components."""
    
    def __init__(self):
        super().__init__(
            namespace=Namespace.CHAKRA,
            base_url="https://chakra-ui.com/"
        )
    
    async def discover_components(self) -> List[str]:
        """Discover all Chakra UI component URLs."""
        component_urls = []
        
        # Get the docs components page
        html = await self.fetch_page(f"{self.base_url}docs/components")
        if not html:
            return component_urls
        
        soup = self.parse_html(html)
        
        # Find component links in the navigation
        component_links = soup.find_all("a", href=re.compile(r"/docs/components/"))
        
        for link in component_links:
            href = link.get("href")
            if href and href != "/docs/components":  # Exclude the main components page
                full_url = urljoin(self.base_url, href)
                if full_url not in component_urls:
                    component_urls.append(full_url)
        
        # If we don't find many components, add some common ones manually
        if len(component_urls) < 5:
            common_components = [
                "accordion", "alert", "aspect-ratio", "avatar", "badge", "breadcrumb",
                "button", "card", "checkbox", "circular-progress", "close-button",
                "code", "divider", "editable", "form-control", "heading", "highlight",
                "icon", "icon-button", "image", "input", "kbd", "link", "list",
                "menu", "modal", "number-input", "pin-input", "popover", "progress",
                "radio", "range-slider", "select", "skeleton", "slider", "spinner",
                "stat", "switch", "table", "tabs", "tag", "text", "textarea",
                "toast", "tooltip", "visually-hidden"
            ]
            
            for component in common_components:
                full_url = f"{self.base_url}docs/components/{component}"
                component_urls.append(full_url)
        
        return component_urls
    
    async def extract_component_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract component data from a Chakra UI component page."""
        html = await self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        # Extract component name from URL
        component_name = url.split("/")[-1]
        
        # Try to find the main title
        title_element = soup.find("h1") or soup.find("title")
        title = title_element.get_text().strip() if title_element else component_name.title()
        
        # Extract description from meta description or first paragraph
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")
        else:
            # Try to find the first meaningful paragraph
            first_p = soup.find("p")
            if first_p:
                description = first_p.get_text().strip()
        
        # Determine component type
        component_type = self.categorize_component(component_name, title, description)
        
        # Extract import statement
        import_statement = f"import {{ {self._pascal_case(component_name)} }} from '@chakra-ui/react'"
        
        # Extract basic usage example
        basic_usage = self._extract_basic_usage(soup, component_name)
        
        # Extract code examples
        code_examples = self._extract_code_examples(soup)
        
        # Extract documentation sections
        docs_sections = self._extract_documentation_sections(soup)
        
        return {
            "name": component_name,
            "title": title,
            "description": description,
            "component_type": component_type,
            "documentation_url": url,
            "import_statement": import_statement,
            "basic_usage": basic_usage,
            "tags": self._extract_tags(component_name, description),
            "code_examples": code_examples,
            "docs_sections": docs_sections
        }
    
    def _pascal_case(self, text: str) -> str:
        """Convert kebab-case to PascalCase."""
        return "".join(word.capitalize() for word in text.split("-"))
    
    def _extract_basic_usage(self, soup: BeautifulSoup, component_name: str) -> str:
        """Extract basic usage example."""
        pascal_name = self._pascal_case(component_name)
        
        # Look for code blocks that might contain basic usage
        code_blocks = soup.find_all("code") + soup.find_all("pre")
        
        for block in code_blocks:
            code_text = block.get_text()
            if pascal_name in code_text and len(code_text) < 200:
                return code_text.strip()
        
        # Generate a basic example if none found
        if component_name == "button":
            return f"<{pascal_name}>Click me</{pascal_name}>"
        elif component_name in ["input", "textarea"]:
            return f"<{pascal_name} placeholder=\"Enter text...\" />"
        else:
            return f"<{pascal_name} />"
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract code examples from the page."""
        examples = []
        
        # Find all code blocks
        code_blocks = soup.find_all("pre") + soup.find_all("code")
        
        for i, block in enumerate(code_blocks):
            code_text = block.get_text().strip()
            if len(code_text) > 20:  # Only include substantial code blocks
                examples.append({
                    "title": f"Example {i + 1}",
                    "description": "",
                    "language": "jsx",
                    "code": code_text
                })
        
        return examples[:5]  # Limit to 5 examples
    
    def _extract_documentation_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract documentation sections."""
        sections = []
        
        # Find all headings and their content
        headings = soup.find_all(["h2", "h3", "h4"])
        
        for heading in headings:
            title = heading.get_text().strip()
            
            # Get content until next heading
            content_parts = []
            next_elem = heading.next_sibling
            
            while next_elem and next_elem.name not in ["h1", "h2", "h3", "h4"]:
                if hasattr(next_elem, "get_text"):
                    text = next_elem.get_text().strip()
                    if text:
                        content_parts.append(text)
                next_elem = next_elem.next_sibling
            
            if content_parts:
                sections.append({
                    "title": title,
                    "content": "\n".join(content_parts)[:1000],  # Limit content length
                    "section_type": "documentation"
                })
        
        return sections[:10]  # Limit to 10 sections
    
    def _extract_tags(self, component_name: str, description: str) -> List[str]:
        """Extract relevant tags for the component."""
        tags = [self.namespace.value]
        
        # Add component type as tag
        if "button" in component_name.lower():
            tags.extend(["button", "interactive", "action"])
        elif "input" in component_name.lower() or "form" in component_name.lower():
            tags.extend(["input", "form", "interactive"])
        elif "modal" in component_name.lower() or "dialog" in component_name.lower():
            tags.extend(["modal", "overlay", "dialog"])
        elif "menu" in component_name.lower() or "dropdown" in component_name.lower():
            tags.extend(["menu", "navigation", "dropdown"])
        elif "table" in component_name.lower():
            tags.extend(["table", "data", "display"])
        elif "card" in component_name.lower():
            tags.extend(["card", "container", "layout"])
        elif "navigation" in component_name.lower() or "nav" in component_name.lower():
            tags.extend(["navigation", "menu"])
        
        # Add descriptive tags from description
        if "responsive" in description.lower():
            tags.append("responsive")
        if "accessible" in description.lower():
            tags.append("accessible")
        if "animated" in description.lower() or "animation" in description.lower():
            tags.append("animated")
        
        return list(set(tags))  # Remove duplicates