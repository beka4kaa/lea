"""shadcn/ui provider implementation."""

import json
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import GitHubProvider, ComponentNotFoundError
from .registry import register_provider
from ..models.component_manifest import (
    ComponentManifest,
    Provider,
    License,
    LicenseType,
    Source,
    Framework,
    TailwindConfig,
    TailwindVersion,
    ComponentCode,
    ComponentAccess,
    InstallPlan,
    ComponentCategory
)


@register_provider
class ShadcnUIProvider(GitHubProvider):
    """shadcn/ui component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.SHADCN
    
    @property
    def base_url(self) -> str:
        return "https://ui.shadcn.com"
    
    @property
    def github_repo(self) -> str:
        return "shadcn-ui/ui"
    
    @property
    def supports_cli(self) -> bool:
        return True
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List shadcn/ui components from registry."""
        try:
            # Get registry data
            registry_content = await self.get_file_content("apps/www/registry/registry-components.ts")
            components = self._parse_registry_file(registry_content)
            
            manifests = []
            for component_data in components:
                manifest = await self._create_manifest_from_registry(component_data)
                if manifest:
                    manifests.append(manifest)
            
            # Apply pagination
            start = offset
            end = offset + limit
            return manifests[start:end]
            
        except Exception as e:
            # Fallback to hardcoded components
            return await self._get_fallback_components()
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific shadcn/ui component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in shadcn/ui")
    
    def _parse_registry_file(self, content: str) -> List[Dict[str, Any]]:
        """Parse the TypeScript registry file to extract component data."""
        components = []
        
        # This is a simplified parser - in production you'd want a proper TS parser
        # Look for component definitions
        component_pattern = r'{\s*name:\s*["\']([^"\']+)["\'].*?}'
        matches = re.findall(component_pattern, content, re.DOTALL)
        
        for match in matches:
            components.append({
                "name": match,
                "slug": match.lower().replace(" ", "-"),
                "category": self._infer_category_from_name(match)
            })
        
        return components
    
    def _infer_category_from_name(self, name: str) -> str:
        """Infer category from component name."""
        name_lower = name.lower()
        
        if any(word in name_lower for word in ["button", "toggle"]):
            return "buttons"
        elif any(word in name_lower for word in ["input", "textarea", "select", "checkbox", "radio", "form"]):
            return "forms"
        elif any(word in name_lower for word in ["card", "sheet", "dialog", "modal"]):
            return "layouts"
        elif any(word in name_lower for word in ["nav", "menu", "breadcrumb", "pagination"]):
            return "navigation"
        elif any(word in name_lower for word in ["table", "avatar", "badge", "progress"]):
            return "data_display"
        elif any(word in name_lower for word in ["alert", "toast", "tooltip"]):
            return "feedback"
        else:
            return "other"
    
    async def _create_manifest_from_registry(
        self,
        component_data: Dict[str, Any]
    ) -> Optional[ComponentManifest]:
        """Create component manifest from registry data."""
        try:
            name = component_data["name"]
            slug = component_data["slug"]
            
            # Get component code from registry
            code_content = await self._get_component_code(slug)
            
            # Extract dependencies
            runtime_deps = self._extract_dependencies(code_content)
            
            # Generate CLI command
            cli_command = f"npx shadcn@latest add {slug}"
            
            return ComponentManifest(
                id=f"shadcn/{slug}",
                provider=Provider.SHADCN,
                name=name,
                slug=slug,
                category=ComponentCategory(component_data.get("category", "other")),
                tags=self._generate_tags(name, slug),
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/shadcn-ui/ui/blob/main/LICENSE.md",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url=f"https://github.com/shadcn-ui/ui/tree/main/apps/www/registry/default/ui",
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    next=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V3,  # shadcn/ui primarily uses v3
                    plugin_deps=["tailwindcss-animate"],
                    required_classes=self._extract_tailwind_classes(code_content)
                ),
                runtime_deps=runtime_deps,
                peer_deps=["@radix-ui/react-icons"] if self._uses_radix_icons(code_content) else [],
                install=InstallPlan(
                    npm=runtime_deps,
                    steps=[
                        {
                            "type": "cli",
                            "command": cli_command,
                            "description": f"Install {name} component via shadcn CLI"
                        }
                    ]
                ),
                code=ComponentCode(
                    tsx=code_content if code_content else None
                ),
                access=ComponentAccess(
                    copy_paste=True,
                    cli=cli_command,
                    pro=False
                ),
                description=f"A {name.lower()} component built with Radix UI and Tailwind CSS.",
                documentation_url=f"https://ui.shadcn.com/docs/components/{slug}",
                demo_url=f"https://ui.shadcn.com/docs/components/{slug}",
                keywords=[slug, "radix", "tailwind", "react", "component"]
            )
            
        except Exception as e:
            print(f"Error creating manifest for {component_data}: {e}")
            return None
    
    async def _get_component_code(self, slug: str) -> str:
        """Get component code from registry."""
        try:
            # Try to get the component file
            file_path = f"apps/www/registry/default/ui/{slug}.tsx"
            return await self.get_file_content(file_path)
        except:
            return ""
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract dependencies from component code."""
        deps = []
        
        # Common Radix UI packages
        radix_patterns = [
            r'from ["\'](@radix-ui/react-[^"\']+)',
            r'import.*from ["\'](@radix-ui/react-[^"\']+)'
        ]
        
        for pattern in radix_patterns:
            matches = re.findall(pattern, code)
            deps.extend(matches)
        
        # Other common dependencies
        if "class-variance-authority" in code:
            deps.append("class-variance-authority")
        
        if "clsx" in code:
            deps.append("clsx")
        
        if "tailwind-merge" in code:
            deps.append("tailwind-merge")
        
        if "lucide-react" in code:
            deps.append("lucide-react")
        
        if "date-fns" in code:
            deps.append("date-fns")
        
        return list(set(deps))
    
    def _uses_radix_icons(self, code: str) -> bool:
        """Check if component uses Radix UI icons."""
        return "@radix-ui/react-icons" in code
    
    def _extract_tailwind_classes(self, code: str) -> List[str]:
        """Extract Tailwind classes from component code."""
        classes = []
        
        # Look for className attributes and cn() calls
        patterns = [
            r'className=["\']([^"\']+)["\']',
            r'cn\(["\']([^"\']+)["\']',
            r'cn\(\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                classes.extend(match.split())
        
        # Filter for likely Tailwind classes
        tailwind_classes = [cls for cls in classes if self._is_tailwind_class(cls)]
        return list(set(tailwind_classes))
    
    def _is_tailwind_class(self, cls: str) -> bool:
        """Check if a class looks like a Tailwind class."""
        tailwind_patterns = [
            r'^(bg|text|border|p|m|w|h|flex|grid|rounded|shadow)-',
            r'^(hover|focus|active|disabled|group-hover):',
            r'^(sm|md|lg|xl|2xl):',
            r'^(data-\[state=.*\]):',
            r'^(absolute|relative|fixed|sticky)$',
            r'^(flex|block|inline|hidden)$'
        ]
        
        for pattern in tailwind_patterns:
            if re.match(pattern, cls):
                return True
        
        return False
    
    def _generate_tags(self, name: str, slug: str) -> List[str]:
        """Generate tags for component."""
        tags = [slug, "radix", "tailwind", "accessible"]
        
        name_lower = name.lower()
        if "form" in name_lower or "input" in name_lower:
            tags.append("form")
        if "button" in name_lower:
            tags.append("interactive")
        if "dialog" in name_lower or "modal" in name_lower:
            tags.append("overlay")
        if "nav" in name_lower or "menu" in name_lower:
            tags.append("navigation")
        
        return tags
    
    async def _get_fallback_components(self) -> List[ComponentManifest]:
        """Get fallback components when registry parsing fails."""
        fallback_components = [
            {
                "name": "Button",
                "slug": "button",
                "category": "inputs",
                "description": "Displays a button element with various styles and states.",
                "runtime_deps": ["class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Input",
                "slug": "input", 
                "category": "inputs",
                "description": "Displays a form input field with validation support.",
                "runtime_deps": ["clsx", "tailwind-merge"]
            },
            {
                "name": "Card",
                "slug": "card",
                "category": "cards",
                "description": "Displays a card with header, content, and footer sections.",
                "runtime_deps": ["clsx", "tailwind-merge"]
            },
            {
                "name": "Dialog",
                "slug": "dialog",
                "category": "overlays",
                "description": "A window overlaid on either the primary window or another dialog window.",
                "runtime_deps": ["@radix-ui/react-dialog", "class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Alert",
                "slug": "alert",
                "category": "feedback",
                "description": "Displays a callout for user attention with various severity levels.",
                "runtime_deps": ["class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Badge",
                "slug": "badge",
                "category": "data_display",
                "description": "Displays a badge or a component that looks like a badge.",
                "runtime_deps": ["class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Avatar",
                "slug": "avatar",
                "category": "data_display",
                "description": "An image element with a fallback for representing the user.",
                "runtime_deps": ["@radix-ui/react-avatar", "clsx", "tailwind-merge"]
            },
            {
                "name": "Accordion",
                "slug": "accordion",
                "category": "disclosure",
                "description": "A vertically stacked set of interactive headings.",
                "runtime_deps": ["@radix-ui/react-accordion", "clsx", "tailwind-merge"]
            },
            {
                "name": "Checkbox",
                "slug": "checkbox",
                "category": "inputs",
                "description": "A control that allows the user to toggle between checked and not checked.",
                "runtime_deps": ["@radix-ui/react-checkbox", "clsx", "tailwind-merge"]
            },
            {
                "name": "Select",
                "slug": "select",
                "category": "inputs",
                "description": "Displays a list of options for the user to pick from.",
                "runtime_deps": ["@radix-ui/react-select", "clsx", "tailwind-merge"]
            },
            {
                "name": "Switch",
                "slug": "switch",
                "category": "inputs",
                "description": "A control that allows the user to toggle between on and off.",
                "runtime_deps": ["@radix-ui/react-switch", "clsx", "tailwind-merge"]
            },
            {
                "name": "Textarea",
                "slug": "textarea",
                "category": "inputs",
                "description": "Displays a form textarea for longer text input.",
                "runtime_deps": ["clsx", "tailwind-merge"]
            },
            {
                "name": "Label",
                "slug": "label",
                "category": "inputs",
                "description": "Renders an accessible label associated with controls.",
                "runtime_deps": ["@radix-ui/react-label", "class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Tabs",
                "slug": "tabs",
                "category": "navigation",
                "description": "A set of layered sections of content known as tab panels.",
                "runtime_deps": ["@radix-ui/react-tabs", "clsx", "tailwind-merge"]
            },
            {
                "name": "Progress",
                "slug": "progress",
                "category": "feedback",
                "description": "Displays an indicator showing the completion progress of a task.",
                "runtime_deps": ["@radix-ui/react-progress", "clsx", "tailwind-merge"]
            },
            {
                "name": "Slider",
                "slug": "slider",
                "category": "inputs",
                "description": "An input where the user selects a value from within a given range.",
                "runtime_deps": ["@radix-ui/react-slider", "clsx", "tailwind-merge"]
            },
            {
                "name": "Toast",
                "slug": "toast",
                "category": "feedback",
                "description": "A succinct message that is displayed temporarily.",
                "runtime_deps": ["@radix-ui/react-toast", "class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Tooltip",
                "slug": "tooltip",
                "category": "overlays",
                "description": "A popup that displays information related to an element.",
                "runtime_deps": ["@radix-ui/react-tooltip", "clsx", "tailwind-merge"]
            },
            {
                "name": "Popover",
                "slug": "popover",
                "category": "overlays",
                "description": "Displays rich content in a portal, triggered by a button.",
                "runtime_deps": ["@radix-ui/react-popover", "clsx", "tailwind-merge"]
            },
            {
                "name": "Sheet",
                "slug": "sheet",
                "category": "overlays",
                "description": "Extends the Dialog component to display content that complements the main content.",
                "runtime_deps": ["@radix-ui/react-dialog", "class-variance-authority", "clsx", "tailwind-merge"]
            },
            {
                "name": "Separator",
                "slug": "separator",
                "category": "layout",
                "description": "Visually or semantically separates content.",
                "runtime_deps": ["@radix-ui/react-separator", "clsx", "tailwind-merge"]
            },
            {
                "name": "Skeleton",
                "slug": "skeleton",
                "category": "feedback",
                "description": "Use to show a placeholder while content is loading.",
                "runtime_deps": ["clsx", "tailwind-merge"]
            },
            {
                "name": "Table",
                "slug": "table",
                "category": "tables",
                "description": "A responsive table component for displaying tabular data.",
                "runtime_deps": ["clsx", "tailwind-merge"]
            },
            {
                "name": "Form",
                "slug": "form",
                "category": "inputs",
                "description": "Building forms with validation and error handling.",
                "runtime_deps": ["@hookform/resolvers", "react-hook-form", "zod", "clsx", "tailwind-merge"]
            },
            {
                "name": "Command",
                "slug": "command",
                "category": "inputs",
                "description": "Fast, composable, unstyled command menu for React.",
                "runtime_deps": ["cmdk", "clsx", "tailwind-merge"]
            },
            {
                "name": "Calendar",
                "slug": "calendar",
                "category": "inputs",
                "description": "A date field component that allows users to enter and edit date.",
                "runtime_deps": ["react-day-picker", "date-fns", "clsx", "tailwind-merge"]
            },
            {
                "name": "Context Menu",
                "slug": "context-menu",
                "category": "overlays",
                "description": "Displays a menu to the user triggered by right-clicking or long-pressing.",
                "runtime_deps": ["@radix-ui/react-context-menu", "clsx", "tailwind-merge"]
            },
            {
                "name": "Dropdown Menu",
                "slug": "dropdown-menu",
                "category": "overlays",
                "description": "Displays a menu to the user triggered by a button.",
                "runtime_deps": ["@radix-ui/react-dropdown-menu", "clsx", "tailwind-merge"]
            },
            {
                "name": "Menubar",
                "slug": "menubar",
                "category": "navigation",
                "description": "A visually persistent menu common in desktop applications.",
                "runtime_deps": ["@radix-ui/react-menubar", "clsx", "tailwind-merge"]
            },
            {
                "name": "Navigation Menu",
                "slug": "navigation-menu",
                "category": "navigation",
                "description": "A collection of links for navigating websites.",
                "runtime_deps": ["@radix-ui/react-navigation-menu", "class-variance-authority", "clsx", "tailwind-merge"]
            }
        ]
        
        components = []
        for comp_data in fallback_components:
            manifest = ComponentManifest(
                id=f"shadcn/{comp_data['slug']}",
                provider=Provider.SHADCN,
                name=comp_data["name"],
                slug=comp_data["slug"],
                category=ComponentCategory(comp_data["category"]),
                tags=self._generate_tags(comp_data["name"], comp_data["slug"]),
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/shadcn-ui/ui/blob/main/LICENSE.md",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url="https://github.com/shadcn-ui/ui",
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    next=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V3,
                    plugin_deps=["tailwindcss-animate"]
                ),
                runtime_deps=comp_data["runtime_deps"],
                install=InstallPlan(
                    npm=comp_data["runtime_deps"],
                    steps=[
                        {
                            "type": "cli",
                            "command": f"npx shadcn@latest add {comp_data['slug']}",
                            "description": f"Install {comp_data['name']} component via shadcn CLI"
                        }
                    ]
                ),
                code=ComponentCode(),
                access=ComponentAccess(
                    copy_paste=True,
                    cli=f"npx shadcn@latest add {comp_data['slug']}",
                    pro=False
                ),
                description=comp_data["description"],
                documentation_url=f"https://ui.shadcn.com/docs/components/{comp_data['slug']}",
                demo_url=f"https://ui.shadcn.com/docs/components/{comp_data['slug']}",
                keywords=[comp_data["slug"], "radix", "tailwind", "react", "component"]
            )
            components.append(manifest)
        
        return components