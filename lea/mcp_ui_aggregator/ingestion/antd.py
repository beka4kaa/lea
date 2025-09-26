"""Ant Design ingestion implementation."""

import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from mcp_ui_aggregator.ingestion.base import BaseIngester
from mcp_ui_aggregator.models.database import Namespace


class AntDesignIngester(BaseIngester):
    """Ingester for Ant Design components."""
    
    def __init__(self):
        super().__init__(
            namespace=Namespace.ANTD,
            base_url="https://ant.design/"
        )
    
    async def discover_components(self) -> List[str]:
        """Discover all Ant Design component URLs."""
        component_urls = []
        
        # Get the components page
        html = await self.fetch_page(f"{self.base_url}components/overview")
        if not html:
            return component_urls
        
        soup = self.parse_html(html)
        
        # Find component links
        component_links = soup.find_all("a", href=re.compile(r"/components/"))
        
        for link in component_links:
            href = link.get("href")
            if href and href not in ["/components/overview", "/components/"]:
                full_url = urljoin(self.base_url, href)
                if full_url not in component_urls:
                    component_urls.append(full_url)
        
        # If we don't find many components, add common ones manually
        if len(component_urls) < 10:
            common_components = [
                "affix", "alert", "anchor", "auto-complete", "avatar", "back-top",
                "badge", "breadcrumb", "button", "calendar", "card", "carousel",
                "cascader", "checkbox", "col", "collapse", "comment", "config-provider",
                "date-picker", "descriptions", "divider", "drawer", "dropdown", "empty",
                "form", "grid", "icon", "image", "input", "input-number", "layout",
                "list", "mention", "menu", "message", "modal", "notification",
                "page-header", "pagination", "popconfirm", "popover", "progress",
                "radio", "rate", "result", "row", "select", "skeleton", "slider",
                "space", "spin", "statistic", "steps", "switch", "table", "tabs",
                "tag", "time-picker", "timeline", "tooltip", "transfer", "tree",
                "tree-select", "typography", "upload"
            ]
            
            for component in common_components:
                full_url = f"{self.base_url}components/{component}"
                component_urls.append(full_url)
        
        return component_urls
    
    async def extract_component_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract component data from an Ant Design component page."""
        html = await self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        # Extract component name from URL
        component_name = url.split("/")[-1]
        
        # Try to find the main title
        title_element = soup.find("h1") or soup.find("title")
        title = title_element.get_text().strip() if title_element else component_name.title()
        
        # Clean up title if it contains "Ant Design"
        if "Ant Design" in title:
            title = title.replace("Ant Design", "").strip()
        if title.startswith("-"):
            title = title[1:].strip()
        
        # Extract description
        description = ""
        # Look for description in various places
        desc_selectors = [
            ".markdown p:first-of-type",
            ".ant-typography p:first-of-type", 
            "p:first-of-type"
        ]
        
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                description = desc_elem.get_text().strip()
                break
        
        if not description:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                description = meta_desc.get("content", "")
        
        # Determine component type
        component_type = self.categorize_component(component_name, title, description)
        
        # Extract import statement
        import_statement = f"import {{ {self._pascal_case(component_name)} }} from 'antd'"
        
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
        # Handle special cases for Ant Design
        special_cases = {
            "auto-complete": "AutoComplete",
            "back-top": "BackTop",
            "date-picker": "DatePicker",
            "input-number": "InputNumber",
            "page-header": "PageHeader",
            "time-picker": "TimePicker",
            "tree-select": "TreeSelect",
            "config-provider": "ConfigProvider"
        }
        
        if text in special_cases:
            return special_cases[text]
        
        return "".join(word.capitalize() for word in text.split("-"))
    
    def _extract_basic_usage(self, soup: BeautifulSoup, component_name: str) -> str:
        """Extract basic usage example."""
        pascal_name = self._pascal_case(component_name)
        
        # Look for code blocks that might contain basic usage
        code_blocks = soup.find_all("code") + soup.find_all("pre")
        
        for block in code_blocks:
            code_text = block.get_text()
            if pascal_name in code_text and len(code_text) < 300:
                # Clean up the code
                lines = code_text.strip().split('\n')
                # Find the line with the component
                for line in lines:
                    if pascal_name in line and '<' in line:
                        return line.strip()
        
        # Generate a basic example if none found
        if component_name == "button":
            return f"<{pascal_name} type=\"primary\">Click me</{pascal_name}>"
        elif component_name == "input":
            return f"<{pascal_name} placeholder=\"Enter text...\" />"
        elif component_name == "select":
            return f"<{pascal_name} placeholder=\"Select option\" />"
        elif component_name == "checkbox":
            return f"<{pascal_name}>Checkbox</{pascal_name}>"
        elif component_name == "radio":
            return f"<{pascal_name}>Radio</{pascal_name}>"
        else:
            return f"<{pascal_name} />"
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract code examples from the page."""
        examples = []
        
        # Look for code blocks within demo sections
        demo_sections = soup.find_all(class_=re.compile(r"demo|example"))
        
        for i, section in enumerate(demo_sections):
            code_block = section.find("pre") or section.find("code")
            if code_block:
                code_text = code_block.get_text().strip()
                if len(code_text) > 20:
                    # Try to find a title for this example
                    title_elem = section.find(["h3", "h4", "h5"]) or section.find(class_=re.compile(r"title|heading"))
                    title = title_elem.get_text().strip() if title_elem else f"Example {i + 1}"
                    
                    examples.append({
                        "title": title,
                        "description": "",
                        "language": "jsx",
                        "code": code_text
                    })
        
        # If no demo sections found, look for all code blocks
        if not examples:
            code_blocks = soup.find_all("pre")
            for i, block in enumerate(code_blocks):
                code_text = block.get_text().strip()
                if len(code_text) > 20 and "import" in code_text:
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
        
        # Find API section specifically
        api_section = soup.find(string=re.compile(r"API|Props", re.IGNORECASE))
        if api_section:
            api_parent = api_section.find_parent()
            if api_parent:
                # Get the content after this heading
                content_parts = []
                next_elem = api_parent.next_sibling
                
                while next_elem and len(content_parts) < 10:
                    if hasattr(next_elem, "get_text"):
                        text = next_elem.get_text().strip()
                        if text and len(text) > 10:
                            content_parts.append(text)
                    next_elem = next_elem.next_sibling
                
                if content_parts:
                    sections.append({
                        "title": "API",
                        "content": "\n".join(content_parts)[:1500],
                        "section_type": "api"
                    })
        
        # Find other headings
        headings = soup.find_all(["h2", "h3", "h4"])
        
        for heading in headings[:5]:  # Limit to first 5 headings
            title = heading.get_text().strip()
            
            if title.lower() in ["api", "props"] and any(s["title"] == "API" for s in sections):
                continue  # Skip if we already have API section
            
            # Get content until next heading
            content_parts = []
            next_elem = heading.next_sibling
            
            while next_elem and next_elem.name not in ["h1", "h2", "h3", "h4"] and len(content_parts) < 5:
                if hasattr(next_elem, "get_text"):
                    text = next_elem.get_text().strip()
                    if text:
                        content_parts.append(text)
                next_elem = next_elem.next_sibling
            
            if content_parts:
                sections.append({
                    "title": title,
                    "content": "\n".join(content_parts)[:1000],
                    "section_type": "documentation"
                })
        
        return sections
    
    def _extract_tags(self, component_name: str, description: str) -> List[str]:
        """Extract relevant tags for the component."""
        tags = [self.namespace.value, "antd"]
        
        # Add component-specific tags
        tag_mapping = {
            "button": ["button", "interactive", "action"],
            "input": ["input", "form", "interactive"],
            "select": ["select", "form", "dropdown", "interactive"],
            "checkbox": ["checkbox", "form", "interactive"],
            "radio": ["radio", "form", "interactive"],
            "table": ["table", "data", "display"],
            "modal": ["modal", "overlay", "dialog"],
            "drawer": ["drawer", "overlay", "navigation"],
            "menu": ["menu", "navigation"],
            "dropdown": ["dropdown", "menu", "navigation"],
            "card": ["card", "container", "layout"],
            "form": ["form", "input", "validation"],
            "layout": ["layout", "grid", "structure"],
            "grid": ["grid", "layout", "responsive"],
            "breadcrumb": ["breadcrumb", "navigation"],
            "pagination": ["pagination", "navigation", "data"],
            "upload": ["upload", "file", "interactive"],
            "date-picker": ["date", "picker", "form", "interactive"],
            "time-picker": ["time", "picker", "form", "interactive"]
        }
        
        if component_name in tag_mapping:
            tags.extend(tag_mapping[component_name])
        
        # Add descriptive tags from description
        desc_lower = description.lower()
        if "responsive" in desc_lower:
            tags.append("responsive")
        if "accessible" in desc_lower:
            tags.append("accessible")
        if "enterprise" in desc_lower:
            tags.append("enterprise")
        if "data" in desc_lower:
            tags.append("data")
        
        return list(set(tags))  # Remove duplicates