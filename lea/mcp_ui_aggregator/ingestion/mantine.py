"""Mantine ingestion implementation."""

import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from mcp_ui_aggregator.ingestion.base import BaseIngester
from mcp_ui_aggregator.models.database import Namespace


class MantineIngester(BaseIngester):
    """Ingester for Mantine components."""
    
    def __init__(self):
        super().__init__(
            namespace=Namespace.MANTINE,
            base_url="https://mantine.dev/"
        )
    
    async def discover_components(self) -> List[str]:
        """Discover all Mantine component URLs."""
        component_urls = []
        
        # Get the core components page
        html = await self.fetch_page(f"{self.base_url}core/")
        if not html:
            return component_urls
        
        soup = self.parse_html(html)
        
        # Find component links in the navigation
        component_links = soup.find_all("a", href=re.compile(r"/core/"))
        
        for link in component_links:
            href = link.get("href")
            if href and href != "/core/":
                full_url = urljoin(self.base_url, href)
                if full_url not in component_urls:
                    component_urls.append(full_url)
        
        # If we don't find many components, add common ones manually
        if len(component_urls) < 10:
            common_components = [
                "action-icon", "affix", "alert", "anchor", "app-shell", "aspect-ratio",
                "autocomplete", "avatar", "backdrop", "badge", "blockquote", "breadcrumbs",
                "burger", "button", "card", "center", "checkbox", "chip", "close-button",
                "code", "collapse", "color-input", "color-picker", "container", "copy-button",
                "divider", "drawer", "fieldset", "file-button", "file-input", "flex",
                "floating-indicator", "focus-trap", "grid", "group", "highlight", "hover-card",
                "image", "indicator", "input", "json-input", "kbd", "loader", "mark",
                "menu", "modal", "native-select", "notification", "number-input", "overlay",
                "pagination", "paper", "password-input", "pill", "pincode-input", "popover",
                "progress", "radio", "rating", "rem", "ring-progress", "scroll-area",
                "segmented-control", "select", "simple-grid", "skeleton", "slider", "space",
                "spoiler", "stack", "stepper", "switch", "table", "tabs", "tag-input",
                "text", "textarea", "theme-icon", "timeline", "title", "tooltip", "tree"
            ]
            
            for component in common_components:
                full_url = f"{self.base_url}core/{component}/"
                component_urls.append(full_url)
        
        return component_urls
    
    async def extract_component_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract component data from a Mantine component page."""
        html = await self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        # Extract component name from URL
        url_parts = url.rstrip('/').split("/")
        component_name = url_parts[-1] if url_parts[-1] else url_parts[-2]
        
        # Try to find the main title
        title_element = soup.find("h1") or soup.find("title")
        title = title_element.get_text().strip() if title_element else component_name.title()
        
        # Clean up title
        if " | Mantine" in title:
            title = title.replace(" | Mantine", "").strip()
        
        # Extract description
        description = ""
        # Look for description in meta tag or first paragraph
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")
        else:
            # Look for first meaningful paragraph
            paragraphs = soup.find_all("p")
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 20 and not text.startswith("Install"):
                    description = text
                    break
        
        # Determine component type
        component_type = self.categorize_component(component_name, title, description)
        
        # Extract import statement
        pascal_name = self._pascal_case(component_name)
        import_statement = f"import {{ {pascal_name} }} from '@mantine/core'"
        
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
        # Handle special cases for Mantine
        special_cases = {
            "action-icon": "ActionIcon",
            "app-shell": "AppShell",
            "aspect-ratio": "AspectRatio",
            "close-button": "CloseButton",
            "color-input": "ColorInput",
            "color-picker": "ColorPicker",
            "copy-button": "CopyButton",
            "file-button": "FileButton",
            "file-input": "FileInput",
            "floating-indicator": "FloatingIndicator",
            "focus-trap": "FocusRap",
            "hover-card": "HoverCard",
            "json-input": "JsonInput",
            "native-select": "NativeSelect",
            "number-input": "NumberInput",
            "password-input": "PasswordInput",
            "pincode-input": "PinCodeInput",
            "ring-progress": "RingProgress",
            "scroll-area": "ScrollArea",
            "segmented-control": "SegmentedControl",
            "simple-grid": "SimpleGrid",
            "tag-input": "TagInput",
            "theme-icon": "ThemeIcon"
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
            if pascal_name in code_text and len(code_text) < 200:
                # Try to extract just the component usage line
                lines = code_text.strip().split('\n')
                for line in lines:
                    if pascal_name in line and '<' in line:
                        return line.strip()
        
        # Generate a basic example if none found
        examples = {
            "button": f"<{pascal_name}>Click me</{pascal_name}>",
            "input": f"<{pascal_name} placeholder=\"Enter text...\" />",
            "textarea": f"<{pascal_name} placeholder=\"Enter text...\" />",
            "select": f"<{pascal_name} placeholder=\"Select option\" />",
            "checkbox": f"<{pascal_name} label=\"Checkbox\" />",
            "radio": f"<{pascal_name} label=\"Radio\" />",
            "switch": f"<{pascal_name} label=\"Switch\" />",
            "slider": f"<{pascal_name} />",
            "progress": f"<{pascal_name} value={{50}} />",
            "loader": f"<{pascal_name} />",
            "badge": f"<{pascal_name}>Badge</{pascal_name}>",
            "card": f"<{pascal_name}>Card content</{pascal_name}>",
            "paper": f"<{pascal_name}>Paper content</{pascal_name}>",
            "text": f"<{pascal_name}>Text content</{pascal_name}>",
            "title": f"<{pascal_name}>Title</{pascal_name}>"
        }
        
        return examples.get(component_name, f"<{pascal_name} />")
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract code examples from the page."""
        examples = []
        
        # Look for demo sections or code blocks
        demo_sections = soup.find_all(class_=re.compile(r"demo|example"))
        
        for i, section in enumerate(demo_sections):
            code_block = section.find("pre") or section.find("code")
            if code_block:
                code_text = code_block.get_text().strip()
                if len(code_text) > 20:
                    title_elem = section.find(["h2", "h3", "h4"]) or section.find(class_=re.compile(r"title"))
                    title = title_elem.get_text().strip() if title_elem else f"Example {i + 1}"
                    
                    examples.append({
                        "title": title,
                        "description": "",
                        "language": "tsx",
                        "code": code_text
                    })
        
        # If no demo sections, look for all code blocks
        if not examples:
            code_blocks = soup.find_all("pre")
            for i, block in enumerate(code_blocks):
                code_text = block.get_text().strip()
                if len(code_text) > 20 and ("import" in code_text or "export" in code_text):
                    examples.append({
                        "title": f"Example {i + 1}",
                        "description": "",
                        "language": "tsx",
                        "code": code_text
                    })
        
        return examples[:5]
    
    def _extract_documentation_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract documentation sections."""
        sections = []
        
        # Find main sections
        headings = soup.find_all(["h2", "h3"])
        
        for heading in headings[:8]:  # Limit to first 8 headings
            title = heading.get_text().strip()
            
            # Skip navigation and other non-content headings
            if title.lower() in ["navigation", "menu", "table of contents"]:
                continue
            
            # Get content until next heading
            content_parts = []
            next_elem = heading.next_sibling
            
            while next_elem and next_elem.name not in ["h1", "h2", "h3"] and len(content_parts) < 5:
                if hasattr(next_elem, "get_text"):
                    text = next_elem.get_text().strip()
                    if text and len(text) > 10:
                        content_parts.append(text)
                next_elem = next_elem.next_sibling
            
            if content_parts:
                section_type = "api" if "prop" in title.lower() or "api" in title.lower() else "documentation"
                sections.append({
                    "title": title,
                    "content": "\n".join(content_parts)[:1200],
                    "section_type": section_type
                })
        
        return sections
    
    def _extract_tags(self, component_name: str, description: str) -> List[str]:
        """Extract relevant tags for the component."""
        tags = [self.namespace.value, "mantine", "react"]
        
        # Component-specific tags
        tag_mapping = {
            "button": ["button", "interactive", "action"],
            "action-icon": ["button", "icon", "interactive"],
            "input": ["input", "form", "interactive"],
            "textarea": ["textarea", "input", "form", "interactive"],
            "select": ["select", "form", "dropdown", "interactive"],
            "native-select": ["select", "form", "dropdown", "interactive"],
            "checkbox": ["checkbox", "form", "interactive"],
            "radio": ["radio", "form", "interactive"],
            "switch": ["switch", "toggle", "form", "interactive"],
            "table": ["table", "data", "display"],
            "modal": ["modal", "overlay", "dialog"],
            "drawer": ["drawer", "overlay", "navigation"],
            "menu": ["menu", "navigation", "dropdown"],
            "card": ["card", "container", "layout"],
            "paper": ["paper", "container", "layout"],
            "grid": ["grid", "layout", "responsive"],
            "simple-grid": ["grid", "layout", "responsive"],
            "flex": ["flex", "layout"],
            "group": ["group", "layout"],
            "stack": ["stack", "layout"],
            "container": ["container", "layout"],
            "center": ["center", "layout"],
            "breadcrumbs": ["breadcrumb", "navigation"],
            "pagination": ["pagination", "navigation"],
            "stepper": ["stepper", "navigation", "wizard"],
            "tabs": ["tabs", "navigation"],
            "avatar": ["avatar", "user", "image"],
            "badge": ["badge", "label", "status"],
            "loader": ["loader", "spinner", "loading"],
            "progress": ["progress", "loading", "indicator"],
            "ring-progress": ["progress", "loading", "indicator", "circular"],
            "skeleton": ["skeleton", "loading", "placeholder"],
            "notification": ["notification", "alert", "message"],
            "alert": ["alert", "notification", "message"],
            "tooltip": ["tooltip", "overlay", "help"],
            "popover": ["popover", "overlay", "dropdown"],
            "hover-card": ["hover", "card", "overlay"],
            "slider": ["slider", "range", "form", "interactive"],
            "rating": ["rating", "star", "interactive"],
            "color-picker": ["color", "picker", "form", "interactive"],
            "date-picker": ["date", "picker", "form", "interactive"],
            "file-input": ["file", "upload", "form", "interactive"],
            "image": ["image", "media", "display"]
        }
        
        if component_name in tag_mapping:
            tags.extend(tag_mapping[component_name])
        
        # Add descriptive tags from description
        desc_lower = description.lower()
        if "responsive" in desc_lower:
            tags.append("responsive")
        if "accessible" in desc_lower:
            tags.append("accessible")
        if "typescript" in desc_lower:
            tags.append("typescript")
        if "theme" in desc_lower:
            tags.append("themeable")
        if "modern" in desc_lower:
            tags.append("modern")
        
        return list(set(tags))  # Remove duplicates