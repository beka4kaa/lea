"""Magic UI provider implementation."""

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
class MagicUIProvider(GitHubProvider):
    """Magic UI component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.MAGICUI
    
    @property
    def base_url(self) -> str:
        return "https://magicui.design"
    
    @property
    def github_repo(self) -> str:
        return "magicuidesign/magicui"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List Magic UI components from GitHub registry."""
        try:
            # Get registry file
            registry_content = await self.get_file_content("__registry__/registry.json")
            registry_data = json.loads(registry_content)
            
            components = []
            for component_data in registry_data.get("components", []):
                manifest = await self._create_manifest_from_registry(component_data)
                if manifest:
                    components.append(manifest)
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            # Fallback to hardcoded components if registry is not available
            return await self._get_fallback_components()
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific Magic UI component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in Magic UI")
    
    async def _create_manifest_from_registry(
        self,
        component_data: Dict[str, Any]
    ) -> Optional[ComponentManifest]:
        """Create component manifest from registry data."""
        try:
            name = component_data.get("name", "")
            slug = component_data.get("slug", name.lower().replace(" ", "-"))
            
            # Get component code
            code_content = ""
            if "files" in component_data:
                for file_info in component_data["files"]:
                    if file_info.get("type") == "component":
                        file_path = file_info.get("path", "")
                        if file_path:
                            try:
                                code_content = await self.get_file_content(file_path)
                                break
                            except:
                                continue
            
            # Extract dependencies from code
            runtime_deps = self._extract_dependencies(code_content)
            
            # Determine category
            category = self._determine_category(name, component_data.get("category", ""))
            
            return ComponentManifest(
                id=f"magicui/{slug}",
                provider=Provider.MAGICUI,
                name=name,
                slug=slug,
                category=category,
                tags=component_data.get("tags", []),
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/magicuidesign/magicui/blob/main/LICENSE",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url=f"https://github.com/magicuidesign/magicui/tree/main/{component_data.get('path', '')}",
                    commit=None,
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    next=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V4,
                    plugin_deps=[],
                    required_classes=self._extract_tailwind_classes(code_content)
                ),
                runtime_deps=runtime_deps,
                install=InstallPlan(
                    npm=runtime_deps,
                    steps=[]
                ),
                code=ComponentCode(
                    tsx=code_content if code_content else None
                ),
                access=ComponentAccess(
                    copy_paste=True,
                    cli=None,
                    pro=False
                ),
                description=component_data.get("description", ""),
                documentation_url=f"https://magicui.design/docs/components/{slug}",
                demo_url=f"https://magicui.design/docs/components/{slug}",
                keywords=component_data.get("keywords", [])
            )
            
        except Exception as e:
            print(f"Error creating manifest for {component_data}: {e}")
            return None
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract dependencies from component code."""
        deps = []
        
        # Common patterns for Magic UI components
        if "framer-motion" in code:
            deps.append("framer-motion")
        
        if "@radix-ui" in code:
            # Extract specific Radix UI packages
            radix_matches = re.findall(r'from ["\'](@radix-ui/[^"\']+)', code)
            deps.extend(radix_matches)
        
        if "lucide-react" in code:
            deps.append("lucide-react")
        
        if "class-variance-authority" in code:
            deps.append("class-variance-authority")
        
        if "clsx" in code:
            deps.append("clsx")
        
        if "tailwind-merge" in code:
            deps.append("tailwind-merge")
        
        return list(set(deps))  # Remove duplicates
    
    def _extract_tailwind_classes(self, code: str) -> List[str]:
        """Extract Tailwind classes from component code."""
        # This is a simplified extraction - in real implementation,
        # you'd want a more sophisticated parser
        classes = []
        
        # Look for className attributes
        class_matches = re.findall(r'className=["\']([^"\']+)["\']', code)
        for match in class_matches:
            # Split by spaces and filter Tailwind-like classes
            potential_classes = match.split()
            for cls in potential_classes:
                if self._is_tailwind_class(cls):
                    classes.append(cls)
        
        return list(set(classes))
    
    def _is_tailwind_class(self, cls: str) -> bool:
        """Check if a class looks like a Tailwind class."""
        # Simple heuristic - Tailwind classes often have specific patterns
        tailwind_patterns = [
            r'^(bg|text|border|p|m|w|h|flex|grid)-',
            r'^(hover|focus|active|disabled):',
            r'^(sm|md|lg|xl|2xl):',
            r'^animate-',
            r'^transition-'
        ]
        
        for pattern in tailwind_patterns:
            if re.match(pattern, cls):
                return True
        
        return False
    
    def _determine_category(self, name: str, registry_category: str) -> ComponentCategory:
        """Determine component category."""
        name_lower = name.lower()
        registry_lower = registry_category.lower()
        
        # Animation-related components
        if any(word in name_lower for word in ["marquee", "orbit", "particles", "typewriter", "blur"]):
            return ComponentCategory.ANIMATED
        
        # Text components
        if any(word in name_lower for word in ["text", "gradient", "word", "letter"]):
            return ComponentCategory.TEXT
        
        # Background components
        if any(word in name_lower for word in ["background", "grid", "dots", "meteors"]):
            return ComponentCategory.BACKGROUNDS
        
        # Layout components
        if any(word in name_lower for word in ["bento", "grid", "dock", "sidebar"]):
            return ComponentCategory.LAYOUTS
        
        # Form components
        if any(word in name_lower for word in ["input", "button", "form"]):
            return ComponentCategory.FORMS
        
        # Default based on registry category
        category_map = {
            "animation": ComponentCategory.ANIMATED,
            "layout": ComponentCategory.LAYOUTS,
            "form": ComponentCategory.FORMS,
            "text": ComponentCategory.TEXT,
            "background": ComponentCategory.BACKGROUNDS
        }
        
        return category_map.get(registry_lower, ComponentCategory.OTHER)
    
    async def _get_fallback_components(self) -> List[ComponentManifest]:
        """Get fallback components when registry is not available."""
        # Hardcoded popular Magic UI components
        fallback_components = [
            {
                "name": "Marquee",
                "slug": "marquee",
                "description": "An infinite scrolling component that can be used to display text, images, or any other content.",
                "category": "animated",
                "tags": ["animation", "scroll", "text"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Orbit",
                "slug": "orbit",
                "description": "A component that displays content in an orbital animation.",
                "category": "animated", 
                "tags": ["animation", "orbit", "circular"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Particles",
                "slug": "particles",
                "description": "A particle system component for creating dynamic backgrounds.",
                "category": "backgrounds",
                "tags": ["particles", "background", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Gradient Text",
                "slug": "gradient-text",
                "description": "A text component with gradient effects.",
                "category": "text",
                "tags": ["text", "gradient", "styling"],
                "runtime_deps": []
            },
            {
                "name": "Blur Fade",
                "slug": "blur-fade",
                "description": "A component that creates blur and fade animations.",
                "category": "animated",
                "tags": ["animation", "blur", "fade"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Animated Beam",
                "slug": "animated-beam",
                "description": "Animated beam connecting two elements with smooth transitions.",
                "category": "animated",
                "tags": ["animation", "beam", "connector"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Magic Card",
                "slug": "magic-card",
                "description": "Interactive card with magical hover effects and animations.",
                "category": "cards",
                "tags": ["card", "hover", "interactive"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Number Ticker",
                "slug": "number-ticker",
                "description": "Animated number counter with smooth transitions and customizable formatting.",
                "category": "animated",
                "tags": ["counter", "animation", "numbers"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Globe",
                "slug": "globe",
                "description": "Interactive 3D globe component with customizable markers and animations.",
                "category": "data_display",
                "tags": ["3d", "globe", "interactive"],
                "runtime_deps": ["three", "framer-motion"]
            },
            {
                "name": "Sparkles",
                "slug": "sparkles",
                "description": "Magical sparkle animation effect for highlighting content.",
                "category": "animated",
                "tags": ["sparkle", "animation", "magic"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Meteors",
                "slug": "meteors",
                "description": "Animated meteors falling across the screen as background effect.",
                "category": "backgrounds",
                "tags": ["meteors", "animation", "background"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Ripple",
                "slug": "ripple",
                "description": "Ripple effect animation component for interactions.",
                "category": "animated",
                "tags": ["ripple", "animation", "effect"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Dock",
                "slug": "dock",
                "description": "MacOS-style dock navigation component with spring animations.",
                "category": "navigation",
                "tags": ["dock", "navigation", "macos"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Avatar Circles",
                "slug": "avatar-circles",
                "description": "Circular avatar layout component with hover animations.",
                "category": "data_display",
                "tags": ["avatar", "circle", "profile"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Border Beam",
                "slug": "border-beam",
                "description": "Animated border with moving beam effect for highlighting elements.",
                "category": "animated",
                "tags": ["border", "beam", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Typing Animation",
                "slug": "typing-animation",
                "description": "Typewriter effect text animation with customizable speed.",
                "category": "text",
                "tags": ["typing", "text", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Word Rotate",
                "slug": "word-rotate",
                "description": "Rotating word animation component for dynamic text display.",
                "category": "text",
                "tags": ["word", "rotate", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Flickering Grid",
                "slug": "flickering-grid",
                "description": "Grid with flickering light effects for cyberpunk aesthetics.",
                "category": "backgrounds",
                "tags": ["grid", "flicker", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Bento Grid",
                "slug": "bento-grid",
                "description": "Masonry-style bento box grid layout for content organization.",
                "category": "layouts",
                "tags": ["grid", "layout", "bento"],
                "runtime_deps": []
            },
            {
                "name": "Animated Shiny Text",
                "slug": "animated-shiny-text",
                "description": "Text with animated shiny effect and gradient overlay.",
                "category": "text",
                "tags": ["text", "shine", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Magic Button",
                "slug": "magic-button",
                "description": "Button with magical hover animations and particle effects.",
                "category": "inputs",
                "tags": ["button", "magic", "hover"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Shimmer",
                "slug": "shimmer",
                "description": "Shimmer loading effect component for skeleton screens.",
                "category": "feedback",
                "tags": ["shimmer", "loading", "effect"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Rainbow Button",
                "slug": "rainbow-button",
                "description": "Button with rainbow gradient animation and hover effects.",
                "category": "inputs",
                "tags": ["button", "rainbow", "gradient"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Text Reveal",
                "slug": "text-reveal",
                "description": "Text reveal animation triggered on scroll or hover.",
                "category": "text",
                "tags": ["text", "reveal", "scroll"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Animated List",
                "slug": "animated-list",
                "description": "List with staggered item animations and smooth transitions.",
                "category": "data_display",
                "tags": ["list", "stagger", "animation"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Cool Mode",
                "slug": "cool-mode",
                "description": "Cool particle effect triggered on user interactions.",
                "category": "animated",
                "tags": ["cool", "particles", "interaction"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Neon Glow",
                "slug": "neon-glow",
                "description": "Neon glow effect for elements with customizable colors.",
                "category": "animated",
                "tags": ["neon", "glow", "effect"],
                "runtime_deps": []
            },
            {
                "name": "Confetti",
                "slug": "confetti",
                "description": "Celebration confetti animation with physics simulation.",
                "category": "animated",
                "tags": ["confetti", "celebration", "animation"],
                "runtime_deps": ["canvas-confetti", "framer-motion"]
            },
            {
                "name": "Spotlight",
                "slug": "spotlight",
                "description": "Interactive spotlight effect that follows cursor movement.",
                "category": "animated",
                "tags": ["spotlight", "effect", "interactive"],
                "runtime_deps": ["framer-motion"]
            },
            {
                "name": "Liquid Blob",
                "slug": "liquid-blob",
                "description": "Morphing liquid blob animation with smooth transitions.",
                "category": "animated",
                "tags": ["blob", "liquid", "morph"],
                "runtime_deps": ["framer-motion"]
            }
        ]
        
        components = []
        for comp_data in fallback_components:
            manifest = ComponentManifest(
                id=f"magicui/{comp_data['slug']}",
                provider=Provider.MAGICUI,
                name=comp_data["name"],
                slug=comp_data["slug"],
                category=ComponentCategory(comp_data["category"]),
                tags=comp_data["tags"],
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/magicuidesign/magicui/blob/main/LICENSE",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url=f"https://github.com/magicuidesign/magicui",
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    next=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V4,
                    plugin_deps=[]
                ),
                runtime_deps=comp_data["runtime_deps"],
                install=InstallPlan(
                    npm=comp_data["runtime_deps"]
                ),
                code=ComponentCode(),
                access=ComponentAccess(
                    copy_paste=True,
                    pro=False
                ),
                description=comp_data["description"],
                documentation_url=f"https://magicui.design/docs/components/{comp_data['slug']}",
                demo_url=f"https://magicui.design/docs/components/{comp_data['slug']}"
            )
            components.append(manifest)
        
        return components