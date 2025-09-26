"""Material UI ingestion implementation."""

import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag

from mcp_ui_aggregator.ingestion.base import BaseIngester
from mcp_ui_aggregator.models.database import Namespace


class MaterialUIIngester(BaseIngester):
    """Ingester for Material UI components."""
    
    def __init__(self):
        super().__init__(
            namespace=Namespace.MATERIAL,
            base_url="https://mui.com/material-ui/"
        )
        
        # Common MUI component categories and their URL patterns
        self.component_categories = [
            "components/",
            # We'll focus on the main components section
        ]
    
    async def discover_components(self) -> List[str]:
        """Discover all Material UI component URLs."""
        component_urls = []
        
        # Get the main components page
        html = await self.fetch_page(f"{self.base_url}components/")
        if not html:
            return component_urls
        
        soup = self.parse_html(html)
        
        # Find component links in the navigation or component grid
        # MUI typically has component links in the sidebar navigation
        component_links = soup.find_all("a", href=re.compile(r"/material-ui/react-"))
        
        for link in component_links:
            href = link.get("href")
            if href:
                # Convert relative URLs to absolute
                full_url = urljoin("https://mui.com", href)
                if full_url not in component_urls:
                    component_urls.append(full_url)
        
        # Also check for components in the main content area
        content_links = soup.find_all("a", href=re.compile(r"/components/"))
        for link in content_links:
            href = link.get("href")
            if href and "react-" in href:
                full_url = urljoin("https://mui.com", href)
                if full_url not in component_urls:
                    component_urls.append(full_url)
        
        # If we don't find many components, add some common ones manually
        if len(component_urls) < 5:
            common_components = [
                "accordion", "alert", "app-bar", "autocomplete", "avatar",
                "badge", "bottom-navigation", "box", "breadcrumbs", "button",
                "button-group", "card", "checkbox", "chip", "circular-progress",
                "container", "data-grid", "date-time-picker", "dialog", "divider",
                "drawer", "fab", "grid", "icon", "icon-button", "image-list",
                "input", "linear-progress", "list", "menu", "modal", "navigation-rail",
                "pagination", "paper", "popover", "radio", "rating", "select",
                "skeleton", "slider", "snackbar", "stack", "stepper", "switch",
                "table", "tabs", "text-field", "timeline", "toggle-button",
                "tooltip", "transfer-list", "tree-view", "typography"
            ]
            
            for component in common_components:
                url = f"https://mui.com/material-ui/react-{component}/"
                component_urls.append(url)
        
        return list(set(component_urls))  # Remove duplicates
    
    async def extract_component_data(self, component_url: str) -> Optional[Dict[str, Any]]:
        """Extract component data from Material UI documentation page."""
        html = await self.fetch_page(component_url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        # Extract component name from URL
        component_name = self._extract_component_name(component_url)
        if not component_name:
            return None
        
        # Extract title and description
        title = self._extract_title(soup, component_name)
        description = self._extract_description(soup)
        
        # Extract import statement and basic usage
        import_statement, basic_usage = self._extract_code_info(soup, component_name)
        
        # Extract code examples
        code_examples = self._extract_code_examples(soup)
        
        # Extract documentation sections
        docs_sections = self._extract_docs_sections(soup)
        
        # Extract tags/keywords
        tags = self._extract_tags(soup, component_name, description)
        
        # Build component data
        component_data = {
            "name": component_name,
            "title": title,
            "description": description,
            "component_type": self.infer_component_type(component_name, description).value,
            "documentation_url": component_url,
            "api_reference_url": f"{component_url}#api",
            "import_statement": import_statement,
            "basic_usage": basic_usage,
            "tags": json.dumps(tags),
            "code_examples": code_examples,
            "docs_sections": docs_sections,
        }
        
        return component_data
    
    def _extract_component_name(self, url: str) -> Optional[str]:
        """Extract component name from URL."""
        # MUI URLs are like: https://mui.com/material-ui/react-button/
        match = re.search(r'/react-([^/]+)/?$', url)
        if match:
            # Convert kebab-case to PascalCase
            name = match.group(1)
            return ''.join(word.capitalize() for word in name.split('-'))
        return None
    
    def _extract_title(self, soup: BeautifulSoup, component_name: str) -> str:
        """Extract component title."""
        # Try h1 tag first
        h1 = soup.find("h1")
        if h1:
            return self.clean_text(h1.get_text())
        
        # Try title tag
        title = soup.find("title")
        if title:
            title_text = title.get_text()
            # Remove site name suffix
            title_text = re.sub(r' - Material-UI$', '', title_text)
            return self.clean_text(title_text)
        
        # Fallback to component name
        return component_name
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract component description."""
        # Look for description in meta tag
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            return self.clean_text(meta_desc.get("content", ""))
        
        # Look for first paragraph after h1
        h1 = soup.find("h1")
        if h1:
            next_p = h1.find_next("p")
            if next_p:
                return self.clean_text(next_p.get_text())
        
        return ""
    
    def _extract_code_info(self, soup: BeautifulSoup, component_name: str) -> tuple[str, str]:
        """Extract import statement and basic usage."""
        import_statement = f"import {component_name} from '@mui/material/{component_name}';"
        basic_usage = f"<{component_name}>\n  Content\n</{component_name}>"
        
        # Try to find actual import in code blocks
        code_blocks = soup.find_all("code")
        for code in code_blocks:
            code_text = code.get_text()
            if "import" in code_text and component_name in code_text:
                import_statement = self.clean_text(code_text)
                break
        
        # Try to find basic usage example
        pre_blocks = soup.find_all("pre")
        for pre in pre_blocks:
            code_text = pre.get_text()
            if f"<{component_name}" in code_text and len(code_text) < 200:
                basic_usage = self.clean_text(code_text)
                break
        
        return import_statement, basic_usage
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract code examples."""
        examples = []
        
        # Find demo sections
        demo_sections = soup.find_all(["div", "section"], class_=re.compile(r'demo|example'))
        
        for i, section in enumerate(demo_sections[:5]):  # Limit to 5 examples
            # Try to find code block in this section
            code_block = section.find("pre") or section.find("code")
            if code_block:
                code = self.clean_text(code_block.get_text())
                if len(code) > 10:  # Only include substantial code
                    # Try to find title
                    title_elem = section.find(["h2", "h3", "h4", "h5", "h6"])
                    title = title_elem.get_text() if title_elem else f"Example {i + 1}"
                    
                    examples.append({
                        "title": self.clean_text(title),
                        "description": "",
                        "code": code,
                        "language": "tsx",
                        "framework": "react",
                        "is_basic": i == 0,
                        "is_advanced": False,
                    })
        
        return examples
    
    def _extract_docs_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract documentation sections."""
        sections = []
        
        # Find main content sections
        headings = soup.find_all(["h2", "h3", "h4"], string=re.compile(r'API|Props|Usage|Examples|Accessibility'))
        
        for i, heading in enumerate(headings):
            title = self.clean_text(heading.get_text())
            
            # Get content until next heading of same or higher level
            content_parts = []
            current = heading.next_sibling
            
            while current and len(content_parts) < 10:  # Limit content length
                if hasattr(current, 'name'):
                    if current.name in ['h1', 'h2', 'h3', 'h4'] and current != heading:
                        break
                    if current.name in ['p', 'div', 'ul', 'ol', 'table']:
                        text = current.get_text()
                        if text.strip():
                            content_parts.append(text.strip())
                current = current.next_sibling
            
            if content_parts:
                content = "\n\n".join(content_parts)
                section_type = self._categorize_section(title)
                
                sections.append({
                    "title": title,
                    "content": self.clean_text(content),
                    "section_type": section_type,
                    "order_index": i,
                })
        
        return sections
    
    def _extract_tags(self, soup: BeautifulSoup, component_name: str, description: str) -> List[str]:
        """Extract relevant tags/keywords."""
        tags = set()
        
        # Add component name variations
        tags.add(component_name.lower())
        
        # Add common Material UI tags
        tags.add("material-ui")
        tags.add("mui")
        tags.add("react")
        
        # Extract from description
        if description:
            desc_words = re.findall(r'\b\w+\b', description.lower())
            tags.update(word for word in desc_words if len(word) > 3)
        
        # Add component type-specific tags
        component_type = self.infer_component_type(component_name, description)
        tags.add(component_type.value)
        
        return list(tags)[:10]  # Limit to 10 tags
    
    def _categorize_section(self, title: str) -> str:
        """Categorize documentation section type."""
        title_lower = title.lower()
        
        if "api" in title_lower or "props" in title_lower:
            return "api"
        elif "usage" in title_lower or "how to" in title_lower:
            return "usage"
        elif "example" in title_lower:
            return "examples"
        elif "accessibility" in title_lower or "a11y" in title_lower:
            return "accessibility"
        elif "theme" in title_lower or "theming" in title_lower:
            return "theming"
        else:
            return "general"