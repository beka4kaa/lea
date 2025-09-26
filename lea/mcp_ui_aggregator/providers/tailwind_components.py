"""Tailwind Components Gallery provider - Curated Tailwind CSS components."""

import json
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import BaseProvider, ComponentNotFoundError
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
class TailwindComponentsProvider(BaseProvider):
    """Tailwind Components Gallery provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.TAILWIND_COMPONENTS
    
    @property
    def base_url(self) -> str:
        return "https://tailwindcomponents.com"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List Tailwind Components Gallery components."""
        components = await self._get_tailwind_components()
        
        # Apply pagination
        start = offset
        end = offset + limit
        return components[start:end]
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific Tailwind Components Gallery component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in Tailwind Components Gallery")
    
    async def _get_tailwind_components(self) -> List[ComponentManifest]:
        """Get curated Tailwind Components Gallery components."""
        components_data = [
            # Navigation Components
            {
                "name": "Responsive Navbar",
                "slug": "responsive-navbar",
                "description": "Fully responsive navigation bar with mobile hamburger menu.",
                "category": "navigation",
                "tags": ["navbar", "responsive", "mobile", "hamburger"],
                "complexity": "intermediate"
            },
            {
                "name": "Sidebar Menu",
                "slug": "sidebar-menu",
                "description": "Collapsible sidebar menu with icons and nested items.",
                "category": "navigation",
                "tags": ["sidebar", "menu", "collapsible", "icons"],
                "complexity": "advanced"
            },
            {
                "name": "Breadcrumb Trail",
                "slug": "breadcrumb-trail",
                "description": "Breadcrumb navigation with separators and hover effects.",
                "category": "navigation",
                "tags": ["breadcrumb", "trail", "navigation", "path"],
                "complexity": "basic"
            },
            {
                "name": "Tab Navigation",
                "slug": "tab-navigation",
                "description": "Horizontal tab navigation with active states.",
                "category": "navigation",
                "tags": ["tabs", "navigation", "active", "horizontal"],
                "complexity": "intermediate"
            },
            
            # Form Components
            {
                "name": "Contact Form",
                "slug": "contact-form",
                "description": "Professional contact form with validation states.",
                "category": "forms",
                "tags": ["contact", "form", "validation", "professional"],
                "complexity": "intermediate"
            },
            {
                "name": "Login Form",
                "slug": "login-form",
                "description": "Modern login form with social media options.",
                "category": "forms",
                "tags": ["login", "auth", "social", "modern"],
                "complexity": "intermediate"
            },
            {
                "name": "Multi-step Form",
                "slug": "multi-step-form",
                "description": "Multi-step form wizard with progress indicator.",
                "category": "forms",
                "tags": ["multi-step", "wizard", "progress", "form"],
                "complexity": "advanced"
            },
            {
                "name": "File Upload",
                "slug": "file-upload",
                "description": "Drag and drop file upload with preview.",
                "category": "inputs",
                "tags": ["upload", "file", "drag-drop", "preview"],
                "complexity": "advanced"
            },
            
            # Cards & Content
            {
                "name": "Product Card",
                "slug": "product-card",
                "description": "E-commerce product card with image overlay and actions.",
                "category": "cards",
                "tags": ["product", "ecommerce", "overlay", "actions"],
                "complexity": "intermediate"
            },
            {
                "name": "Profile Card",
                "slug": "profile-card",
                "description": "User profile card with avatar and social stats.",
                "category": "cards",
                "tags": ["profile", "user", "avatar", "stats"],
                "complexity": "basic"
            },
            {
                "name": "Blog Post Card",
                "slug": "blog-post-card",
                "description": "Blog post preview card with meta information.",
                "category": "cards",
                "tags": ["blog", "post", "preview", "meta"],
                "complexity": "basic"
            },
            {
                "name": "Testimonial Card",
                "slug": "testimonial-card",
                "description": "Customer testimonial card with rating stars.",
                "category": "cards",
                "tags": ["testimonial", "review", "rating", "stars"],
                "complexity": "intermediate"
            },
            
            # Layout Components
            {
                "name": "Hero Section",
                "slug": "hero-section",
                "description": "Landing page hero with background image and CTA.",
                "category": "templates",
                "tags": ["hero", "landing", "background", "cta"],
                "complexity": "intermediate"
            },
            {
                "name": "Feature Grid",
                "slug": "feature-grid",
                "description": "Responsive feature grid with icons and descriptions.",
                "category": "layouts",
                "tags": ["features", "grid", "responsive", "icons"],
                "complexity": "basic"
            },
            {
                "name": "Pricing Table",
                "slug": "pricing-table",
                "description": "Comparison pricing table with highlighted plan.",
                "category": "tables",
                "tags": ["pricing", "table", "comparison", "plans"],
                "complexity": "intermediate"
            },
            {
                "name": "Timeline",
                "slug": "timeline",
                "description": "Vertical timeline with alternating content.",
                "category": "data_display",
                "tags": ["timeline", "vertical", "chronology", "history"],
                "complexity": "advanced"
            },
            
            # Interactive Components
            {
                "name": "Modal Dialog",
                "slug": "modal-dialog",
                "description": "Accessible modal dialog with backdrop and animations.",
                "category": "overlays",
                "tags": ["modal", "dialog", "accessible", "animations"],
                "complexity": "advanced"
            },
            {
                "name": "Dropdown Menu",
                "slug": "dropdown-menu",
                "description": "Animated dropdown menu with keyboard navigation.",
                "category": "overlays",
                "tags": ["dropdown", "menu", "animated", "keyboard"],
                "complexity": "advanced"
            },
            {
                "name": "Tooltip",
                "slug": "tooltip",
                "description": "Positioned tooltip with multiple trigger options.",
                "category": "overlays",
                "tags": ["tooltip", "positioned", "trigger", "help"],
                "complexity": "intermediate"
            },
            {
                "name": "Carousel",
                "slug": "carousel",
                "description": "Image carousel with navigation dots and arrows.",
                "category": "data_display",
                "tags": ["carousel", "slider", "images", "navigation"],
                "complexity": "advanced"
            },
            
            # Feedback Components
            {
                "name": "Alert Box",
                "slug": "alert-box",
                "description": "Dismissible alert with different severity levels.",
                "category": "feedback",
                "tags": ["alert", "dismissible", "severity", "notification"],
                "complexity": "basic"
            },
            {
                "name": "Progress Bar",
                "slug": "progress-bar",
                "description": "Animated progress bar with percentage display.",
                "category": "feedback",
                "tags": ["progress", "animated", "percentage", "loading"],
                "complexity": "intermediate"
            },
            {
                "name": "Loading Spinner",
                "slug": "loading-spinner",
                "description": "CSS-only loading spinners in various styles.",
                "category": "feedback",
                "tags": ["loading", "spinner", "css", "animation"],
                "complexity": "basic"
            },
            {
                "name": "Toast Notification",
                "slug": "toast-notification",
                "description": "Slide-in toast notification with auto-dismiss.",
                "category": "feedback",
                "tags": ["toast", "notification", "slide", "auto-dismiss"],
                "complexity": "advanced"
            },
            
            # Utility Components
            {
                "name": "Badge",
                "slug": "badge",
                "description": "Status badges with various colors and sizes.",
                "category": "data_display",
                "tags": ["badge", "status", "colors", "sizes"],
                "complexity": "basic"
            },
            {
                "name": "Avatar",
                "slug": "avatar",
                "description": "User avatar with fallback initials and online indicator.",
                "category": "data_display",
                "tags": ["avatar", "user", "fallback", "indicator"],
                "complexity": "basic"
            },
            {
                "name": "Button Group",
                "slug": "button-group",
                "description": "Segmented button group with active state.",
                "category": "buttons",
                "tags": ["button", "group", "segmented", "active"],
                "complexity": "basic"
            },
            {
                "name": "Search Box",
                "slug": "search-box",
                "description": "Search input with autocomplete suggestions.",
                "category": "inputs",
                "tags": ["search", "autocomplete", "suggestions", "input"],
                "complexity": "advanced"
            },
            {
                "name": "Data Table",
                "slug": "data-table",
                "description": "Sortable data table with row selection.",
                "category": "tables",
                "tags": ["table", "sortable", "selection", "data"],
                "complexity": "advanced"
            },
            {
                "name": "Calendar",
                "slug": "calendar",
                "description": "Monthly calendar view with date selection.",
                "category": "inputs",
                "tags": ["calendar", "date", "selection", "monthly"],
                "complexity": "advanced"
            }
        ]
        
        components = []
        for comp_data in components_data:
            manifest = ComponentManifest(
                id=f"tailwind-components/{comp_data['slug']}",
                provider=Provider.TAILWIND_COMPONENTS,
                name=comp_data["name"],
                slug=comp_data["slug"],
                category=ComponentCategory(comp_data["category"]),
                tags=comp_data["tags"] + [comp_data["complexity"]],
                license=License(
                    type=LicenseType.MIT,
                    url="https://tailwindcomponents.com/license",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url="https://tailwindcomponents.com",
                    branch=None
                ),
                framework=Framework(
                    react=True,
                    vue=True,
                    svelte=True,
                    angular=True,
                    html=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V3,
                    plugin_deps=self._get_plugin_deps(comp_data),
                    required_classes=[]
                ),
                runtime_deps=self._get_runtime_deps(comp_data),
                install=InstallPlan(
                    npm=self._get_runtime_deps(comp_data),
                    steps=[
                        {
                            "type": "copy",
                            "description": f"Copy {comp_data['name']} code from Tailwind Components Gallery"
                        }
                    ]
                ),
                code=ComponentCode(
                    html=self._generate_sample_html(comp_data),
                    css=self._generate_sample_css(comp_data)
                ),
                access=ComponentAccess(
                    copy_paste=True,
                    free=True,
                    pro=False
                ),
                description=comp_data["description"],
                documentation_url=f"https://tailwindcomponents.com/component/{comp_data['slug']}",
                demo_url=f"https://tailwindcomponents.com/component/{comp_data['slug']}",
                keywords=[comp_data["slug"], "tailwind", "components", comp_data["complexity"]] + comp_data["tags"]
            )
            components.append(manifest)
        
        return components
    
    def _get_plugin_deps(self, comp_data: Dict[str, Any]) -> List[str]:
        """Get Tailwind plugin dependencies based on component type."""
        deps = []
        
        if comp_data["complexity"] == "advanced" or "animation" in comp_data["tags"]:
            deps.append("@tailwindcss/forms")
        
        if "form" in comp_data["category"] or "input" in comp_data["tags"]:
            deps.append("@tailwindcss/forms")
        
        return deps
    
    def _get_runtime_deps(self, comp_data: Dict[str, Any]) -> List[str]:
        """Get runtime dependencies based on component functionality."""
        deps = []
        
        if comp_data["complexity"] == "advanced":
            if "modal" in comp_data["slug"] or "dropdown" in comp_data["slug"]:
                deps.extend(["@headlessui/react", "framer-motion"])
            elif "carousel" in comp_data["slug"]:
                deps.append("swiper")
            elif "calendar" in comp_data["slug"]:
                deps.append("date-fns")
        
        return deps
    
    def _generate_sample_html(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample HTML for the component."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        
        if "navbar" in slug:
            return f"""<nav class="bg-white shadow-lg">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex justify-between h-16">
      <div class="flex items-center">
        <span class="text-xl font-semibold">{name}</span>
      </div>
      <div class="hidden md:flex items-center space-x-8">
        <a href="#" class="text-gray-700 hover:text-blue-600">Home</a>
        <a href="#" class="text-gray-700 hover:text-blue-600">About</a>
        <a href="#" class="text-gray-700 hover:text-blue-600">Contact</a>
      </div>
    </div>
  </div>
</nav>"""
        elif "card" in slug:
            return f"""<div class="max-w-sm rounded overflow-hidden shadow-lg bg-white">
  <img class="w-full h-48 object-cover" src="https://via.placeholder.com/400x200" alt="{name}">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">{name}</div>
    <p class="text-gray-700 text-base">{comp_data['description']}</p>
  </div>
  <div class="px-6 pt-4 pb-2">
    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
      #tailwind
    </span>
  </div>
</div>"""
        elif "form" in slug:
            return f"""<form class="max-w-md mx-auto bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
  <div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
      {name}
    </label>
    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username">
  </div>
  <div class="flex items-center justify-between">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
      Submit
    </button>
  </div>
</form>"""
        else:
            return f"""<div class="bg-white p-6 rounded-lg shadow-md">
  <h3 class="text-lg font-semibold text-gray-900 mb-2">{name}</h3>
  <p class="text-gray-600">{comp_data['description']}</p>
</div>"""
    
    def _generate_sample_css(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample CSS for advanced components."""
        if comp_data["complexity"] == "advanced":
            return """/* Custom animations and transitions */
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.slide-in {
  animation: slideIn 0.3s ease-out;
}

/* Focus states and accessibility */
.focus-visible:focus {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}"""
        return ""