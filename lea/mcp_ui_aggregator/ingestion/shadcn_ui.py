"""shadcn/ui ingestion implementation."""

import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from mcp_ui_aggregator.ingestion.base import BaseIngester
from mcp_ui_aggregator.models.database import Namespace


class ShadcnUIIngester(BaseIngester):
    """Ingester for shadcn/ui components."""
    
    def __init__(self):
        super().__init__(
            namespace=Namespace.SHADCN,
            base_url="https://ui.shadcn.com/"
        )
    
    async def discover_components(self) -> List[str]:
        """Discover all shadcn/ui component URLs."""
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
                "accordion", "alert", "alert-dialog", "aspect-ratio", "avatar",
                "badge", "breadcrumb", "button", "calendar", "card", "carousel",
                "checkbox", "collapsible", "combobox", "command", "context-menu",
                "data-table", "date-picker", "dialog", "drawer", "dropdown-menu",
                "form", "hover-card", "input", "label", "menubar", "navigation-menu",
                "pagination", "popover", "progress", "radio-group", "scroll-area",
                "select", "separator", "sheet", "skeleton", "slider", "switch",
                "table", "tabs", "textarea", "toast", "toggle", "toggle-group",
                "tooltip"
            ]
            
            for component in common_components:
                url = f"https://ui.shadcn.com/docs/components/{component}"
                component_urls.append(url)
        
        return list(set(component_urls))  # Remove duplicates
    
    async def extract_component_data(self, component_url: str) -> Optional[Dict[str, Any]]:
        """Extract component data from shadcn/ui documentation page."""
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
            "api_reference_url": component_url,  # shadcn/ui doesn't have separate API pages
            "import_statement": import_statement,
            "basic_usage": basic_usage,
            "tags": json.dumps(tags),
            "code_examples": code_examples,
            "docs_sections": docs_sections,
        }
        
        return component_data
    
    def _extract_component_name(self, url: str) -> Optional[str]:
        """Extract component name from URL."""
        # shadcn/ui URLs are like: https://ui.shadcn.com/docs/components/button
        match = re.search(r'/components/([^/]+)/?$', url)
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
            title_text = re.sub(r' - shadcn/ui$', '', title_text)
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
        
        # Look for lead text or subtitle
        lead = soup.find(class_=re.compile(r'lead|subtitle|description'))
        if lead:
            return self.clean_text(lead.get_text())
        
        return ""
    
    def _extract_code_info(self, soup: BeautifulSoup, component_name: str) -> tuple[str, str]:
        """Extract import statement and basic usage."""
        import_statement = f"import {{ {component_name} }} from '@/components/ui/{component_name.lower()}'"
        basic_usage = f"<{component_name}>\n  Content\n</{component_name}>"
        
        # Look for installation or usage sections
        install_section = soup.find(string=re.compile(r'Installation|Import|Usage', re.I))
        if install_section:
            # Find the next code block
            code_block = install_section.find_next("code") or install_section.find_next("pre")
            if code_block:
                code_text = code_block.get_text()
                if "import" in code_text:
                    import_statement = self.clean_text(code_text)
        
        # Try to find basic usage example in code blocks
        pre_blocks = soup.find_all("pre")
        for pre in pre_blocks:
            code_text = pre.get_text()
            if f"<{component_name}" in code_text and len(code_text) < 300:
                basic_usage = self.clean_text(code_text)
                break
        
        return import_statement, basic_usage
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract code examples."""
        examples = []
        
        # Find sections with examples
        example_headings = soup.find_all(["h2", "h3"], string=re.compile(r'Example|Usage|Demo|Variant', re.I))
        
        for i, heading in enumerate(example_headings[:5]):  # Limit to 5 examples
            # Find the next code block after this heading
            code_block = heading.find_next("pre") or heading.find_next("code")
            if code_block:
                code = self.clean_text(code_block.get_text())
                if len(code) > 10:  # Only include substantial code
                    title = self.clean_text(heading.get_text())
                    
                    # Look for description between heading and code
                    description = ""
                    next_elem = heading.next_sibling
                    while next_elem and next_elem != code_block:
                        if hasattr(next_elem, 'get_text') and next_elem.name == 'p':
                            description = self.clean_text(next_elem.get_text())
                            break
                        next_elem = next_elem.next_sibling
                    
                    examples.append({
                        "title": title,
                        "description": description,
                        "code": code,
                        "language": "tsx",
                        "framework": "react",
                        "is_basic": i == 0,
                        "is_advanced": "advanced" in title.lower(),
                    })
        
        return examples
    
    def _extract_docs_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract documentation sections."""
        sections = []
        
        # Find main content sections
        headings = soup.find_all(["h2", "h3"], string=re.compile(r'Installation|Usage|API|Props|Examples|Accessibility|Variants'))
        
        for i, heading in enumerate(headings):
            title = self.clean_text(heading.get_text())
            
            # Get content until next heading of same or higher level
            content_parts = []
            current = heading.next_sibling
            
            while current and len(content_parts) < 8:  # Limit content length
                if hasattr(current, 'name'):
                    if current.name in ['h1', 'h2', 'h3'] and current != heading:
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
        
        # Add common shadcn/ui tags
        tags.add("shadcn")
        tags.add("shadcn-ui")
        tags.add("react")
        tags.add("tailwind")
        tags.add("radix")
        
        # Extract from description
        if description:
            desc_words = re.findall(r'\b\w+\b', description.lower())
            tags.update(word for word in desc_words if len(word) > 3)
        
        # Add component type-specific tags
        component_type = self.infer_component_type(component_name, description)
        tags.add(component_type.value)
        
        # Look for design system terms in content
        content_text = soup.get_text().lower()
        design_terms = ['accessible', 'headless', 'customizable', 'unstyled', 'composable']
        for term in design_terms:
            if term in content_text:
                tags.add(term)
        
        return list(tags)[:10]  # Limit to 10 tags
    
    def _categorize_section(self, title: str) -> str:
        """Categorize documentation section type."""
        title_lower = title.lower()
        
        if "installation" in title_lower or "install" in title_lower:
            return "installation"
        elif "api" in title_lower or "props" in title_lower:
            return "api"
        elif "usage" in title_lower or "how to" in title_lower:
            return "usage"
        elif "example" in title_lower or "demo" in title_lower:
            return "examples"
        elif "variant" in title_lower or "style" in title_lower:
            return "variants"
        elif "accessibility" in title_lower or "a11y" in title_lower:
            return "accessibility"
        else:
            return "general"