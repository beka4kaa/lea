"""21st.dev provider implementation - Component Directory."""

import json
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import HTTPProvider, ComponentNotFoundError
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
class TwentyFirstProvider(HTTPProvider):
    """21st.dev component directory provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.TWENTY_FIRST
    
    @property
    def base_url(self) -> str:
        return "https://21st.dev"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List 21st.dev components."""
        try:
            components = await self._get_all_components()
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            print(f"Error listing 21st.dev components: {e}")
            return []
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific 21st.dev component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in 21st.dev")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all 21st.dev directory components."""
        # 21st.dev curated component directory
        components_data = [
            {
                "name": "Animated Counter",
                "slug": "animated-counter",
                "category": "animated",
                "description": "Smooth animated number counter with customizable easing",
                "tags": ["counter", "animation", "number", "statistics"],
                "external_url": "https://21st.dev/components/animated-counter",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Auto-Resize Textarea",
                "slug": "auto-resize-textarea",
                "category": "forms",
                "description": "Textarea that automatically resizes based on content",
                "tags": ["textarea", "auto-resize", "form", "input"],
                "external_url": "https://21st.dev/components/auto-resize-textarea",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Breadcrumb Navigation",
                "slug": "breadcrumb-navigation",
                "category": "navigation",
                "description": "Accessible breadcrumb navigation component",
                "tags": ["breadcrumb", "navigation", "path", "hierarchy"],
                "external_url": "https://21st.dev/components/breadcrumb",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Collapsible Section",
                "slug": "collapsible-section",
                "category": "layouts",
                "description": "Smooth collapsible content section",
                "tags": ["collapsible", "accordion", "expand", "section"],
                "external_url": "https://21st.dev/components/collapsible",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Command Menu",
                "slug": "command-menu",
                "category": "navigation",
                "description": "Keyboard-accessible command menu interface",
                "tags": ["command", "menu", "keyboard", "search"],
                "external_url": "https://21st.dev/components/command-menu",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Copy to Clipboard",
                "slug": "copy-to-clipboard",
                "category": "other",
                "description": "One-click copy to clipboard functionality",
                "tags": ["copy", "clipboard", "utility", "button"],
                "external_url": "https://21st.dev/components/copy-to-clipboard",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Dark Mode Toggle",
                "slug": "dark-mode-toggle",
                "category": "other",
                "description": "Smooth dark/light mode toggle switch",
                "tags": ["dark-mode", "theme", "toggle", "switch"],
                "external_url": "https://21st.dev/components/dark-mode-toggle",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Date Picker",
                "slug": "date-picker",
                "category": "forms",
                "description": "Accessible date picker with calendar view",
                "tags": ["date", "picker", "calendar", "form"],
                "external_url": "https://21st.dev/components/date-picker",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Drag and Drop List",
                "slug": "drag-drop-list",
                "category": "layouts",
                "description": "Sortable list with drag and drop functionality",
                "tags": ["drag", "drop", "sort", "list"],
                "external_url": "https://21st.dev/components/drag-drop-list",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "File Upload Zone",
                "slug": "file-upload-zone",
                "category": "forms",
                "description": "Drag & drop file upload with progress",
                "tags": ["file", "upload", "drag-drop", "progress"],
                "external_url": "https://21st.dev/components/file-upload",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Floating Action Button",
                "slug": "floating-action-button",
                "category": "buttons",
                "description": "Material Design floating action button",
                "tags": ["fab", "floating", "action", "button"],
                "external_url": "https://21st.dev/components/fab",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Image Gallery",
                "slug": "image-gallery",
                "category": "data_display",
                "description": "Responsive image gallery with lightbox",
                "tags": ["gallery", "images", "lightbox", "responsive"],
                "external_url": "https://21st.dev/components/image-gallery",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Infinite Scroll",
                "slug": "infinite-scroll",
                "category": "other",
                "description": "Infinite scroll implementation with loading states",
                "tags": ["infinite", "scroll", "loading", "pagination"],
                "external_url": "https://21st.dev/components/infinite-scroll",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Loading Spinner",
                "slug": "loading-spinner",
                "category": "feedback",
                "description": "Customizable loading spinner component",
                "tags": ["loading", "spinner", "progress", "indicator"],
                "external_url": "https://21st.dev/components/loading-spinner",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Multi-Select",
                "slug": "multi-select",
                "category": "forms",
                "description": "Multi-selection dropdown with search",
                "tags": ["select", "multi", "dropdown", "search"],
                "external_url": "https://21st.dev/components/multi-select",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Notification Banner",
                "slug": "notification-banner",
                "category": "feedback",
                "description": "Dismissible notification banner",
                "tags": ["notification", "banner", "alert", "dismissible"],
                "external_url": "https://21st.dev/components/notification-banner",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Pagination",
                "slug": "pagination",
                "category": "navigation",
                "description": "Accessible pagination component",
                "tags": ["pagination", "navigation", "pages", "numbers"],
                "external_url": "https://21st.dev/components/pagination",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Rating Component",
                "slug": "rating-component",
                "category": "forms",
                "description": "Interactive star rating component",
                "tags": ["rating", "stars", "review", "feedback"],
                "external_url": "https://21st.dev/components/rating",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Search Box",
                "slug": "search-box",
                "category": "forms",
                "description": "Search input with autocomplete suggestions",
                "tags": ["search", "input", "autocomplete", "suggestions"],
                "external_url": "https://21st.dev/components/search-box",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Slide Over Panel",
                "slug": "slide-over-panel",
                "category": "overlays",
                "description": "Slide-over panel for additional content",
                "tags": ["slide-over", "panel", "sidebar", "overlay"],
                "external_url": "https://21st.dev/components/slide-over",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Step Progress",
                "slug": "step-progress",
                "category": "feedback",
                "description": "Multi-step progress indicator",
                "tags": ["steps", "progress", "wizard", "indicator"],
                "external_url": "https://21st.dev/components/step-progress",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Tag Input",
                "slug": "tag-input",
                "category": "forms",
                "description": "Input field for adding/removing tags",
                "tags": ["tags", "input", "chips", "tokens"],
                "external_url": "https://21st.dev/components/tag-input",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Time Picker",
                "slug": "time-picker",
                "category": "forms",
                "description": "Time selection component",
                "tags": ["time", "picker", "clock", "form"],
                "external_url": "https://21st.dev/components/time-picker",
                "framework": "react",
                "license": "MIT"
            },
            {
                "name": "Virtual List",
                "slug": "virtual-list",
                "category": "data_display",
                "description": "Performance-optimized virtual scrolling list",
                "tags": ["virtual", "list", "performance", "scroll"],
                "external_url": "https://21st.dev/components/virtual-list",
                "framework": "react",
                "license": "MIT"
            }
        ]
        
        components = []
        for comp_data in components_data:
            manifest = self._create_manifest_from_data(comp_data)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any]) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        return ComponentManifest(
            id=f"21st/{slug}",
            provider=Provider.TWENTY_FIRST,
            name=name,
            slug=slug,
            category=ComponentCategory(category),
            tags=comp_data["tags"],
            license=License(
                type=LicenseType.MIT,
                url="https://21st.dev/license",
                notes="Components from 21st.dev directory - check individual licenses",
                redistribute=True,
                commercial=True
            ),
            source=Source(
                url=comp_data["external_url"],
                branch=None
            ),
            framework=Framework(
                react=True,
                next=True,
                vue=comp_data.get("framework") == "vue",
                svelte=comp_data.get("framework") == "svelte",
                angular=comp_data.get("framework") == "angular"
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,
                plugin_deps=[],
                required_classes=[]
            ),
            runtime_deps=[],
            install=InstallPlan(
                npm=[],
                steps=[
                    {
                        "type": "info",
                        "description": f"Visit {comp_data['external_url']} for implementation details"
                    },
                    {
                        "type": "action",
                        "description": "Copy component code from 21st.dev"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=None  # Directory provider - links to external sources
            ),
            access=ComponentAccess(
                copy_paste=False,  # External link required
                pro=False
            ),
            description=comp_data["description"],
            documentation_url=comp_data["external_url"],
            demo_url=comp_data["external_url"],
            keywords=comp_data["tags"] + ["21st-dev", "directory", "curated"]
        )