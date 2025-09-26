"""HyperUI provider implementation - Free Tailwind CSS components."""

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
class HyperUIProvider(BaseProvider):
    """HyperUI component provider - Free Tailwind CSS components."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.HYPERUI
    
    @property
    def base_url(self) -> str:
        return "https://www.hyperui.dev"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List HyperUI components."""
        components = await self._get_hyperui_components()
        
        # Apply pagination
        start = offset
        end = offset + limit
        return components[start:end]
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific HyperUI component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in HyperUI")
    
    async def _get_hyperui_components(self) -> List[ComponentManifest]:
        """Get HyperUI components organized by categories."""
        components_data = [
            # Application UI
            {
                "name": "Header Navigation",
                "slug": "header-navigation",
                "description": "Responsive header navigation with dropdown menus and mobile toggle.",
                "category": "navigation",
                "tags": ["header", "navigation", "menu", "responsive"],
                "section": "Application UI"
            },
            {
                "name": "Sidebar Navigation",
                "slug": "sidebar-navigation",
                "description": "Collapsible sidebar navigation for admin dashboards.",
                "category": "navigation",
                "tags": ["sidebar", "navigation", "admin", "dashboard"],
                "section": "Application UI"
            },
            {
                "name": "Breadcrumb",
                "slug": "breadcrumb",
                "description": "Simple breadcrumb navigation component.",
                "category": "navigation",
                "tags": ["breadcrumb", "navigation", "path"],
                "section": "Application UI"
            },
            {
                "name": "Pagination",
                "slug": "pagination",
                "description": "Numbered pagination component with previous/next controls.",
                "category": "navigation",
                "tags": ["pagination", "navigation", "pages"],
                "section": "Application UI"
            },
            {
                "name": "Stats Cards",
                "slug": "stats-cards",
                "description": "Dashboard statistics cards with icons and numbers.",
                "category": "data_display",
                "tags": ["stats", "cards", "dashboard", "metrics"],
                "section": "Application UI"
            },
            {
                "name": "Data Table",
                "slug": "data-table",
                "description": "Responsive data table with sorting and actions.",
                "category": "tables",
                "tags": ["table", "data", "sorting", "responsive"],
                "section": "Application UI"
            },
            
            # Marketing Components
            {
                "name": "Hero Section",
                "slug": "hero-section",
                "description": "Landing page hero section with call-to-action.",
                "category": "templates",
                "tags": ["hero", "landing", "cta", "marketing"],
                "section": "Marketing"
            },
            {
                "name": "Feature Grid",
                "slug": "feature-grid",
                "description": "Grid layout showcasing product features with icons.",
                "category": "layouts",
                "tags": ["features", "grid", "icons", "showcase"],
                "section": "Marketing"
            },
            {
                "name": "Testimonials",
                "slug": "testimonials",
                "description": "Customer testimonials with photos and quotes.",
                "category": "data_display",
                "tags": ["testimonials", "reviews", "customers"],
                "section": "Marketing"
            },
            {
                "name": "Pricing Cards",
                "slug": "pricing-cards",
                "description": "Pricing plans with feature lists and CTAs.",
                "category": "cards",
                "tags": ["pricing", "plans", "subscription", "cta"],
                "section": "Marketing"
            },
            {
                "name": "Team Grid",
                "slug": "team-grid",
                "description": "Team member cards with photos and social links.",
                "category": "data_display",
                "tags": ["team", "members", "staff", "about"],
                "section": "Marketing"
            },
            {
                "name": "FAQ Section",
                "slug": "faq-section",
                "description": "Frequently asked questions with collapsible answers.",
                "category": "disclosure",
                "tags": ["faq", "questions", "help", "accordion"],
                "section": "Marketing"
            },
            
            # E-commerce
            {
                "name": "Product Card",
                "slug": "product-card",
                "description": "E-commerce product card with image, price, and actions.",
                "category": "cards",
                "tags": ["product", "ecommerce", "shop", "card"],
                "section": "E-commerce"
            },
            {
                "name": "Shopping Cart",
                "slug": "shopping-cart",
                "description": "Shopping cart dropdown with items and totals.",
                "category": "overlays",
                "tags": ["cart", "shopping", "ecommerce", "dropdown"],
                "section": "E-commerce"
            },
            {
                "name": "Product Gallery",
                "slug": "product-gallery",
                "description": "Product image gallery with thumbnail navigation.",
                "category": "data_display",
                "tags": ["gallery", "images", "product", "thumbnails"],
                "section": "E-commerce"
            },
            {
                "name": "Filter Sidebar",
                "slug": "filter-sidebar",
                "description": "Product filter sidebar with categories and price range.",
                "category": "inputs",
                "tags": ["filter", "sidebar", "search", "categories"],
                "section": "E-commerce"
            },
            
            # Form Components
            {
                "name": "Contact Form",
                "slug": "contact-form",
                "description": "Simple contact form with validation styling.",
                "category": "forms",
                "tags": ["contact", "form", "validation", "input"],
                "section": "Forms"
            },
            {
                "name": "Newsletter Signup",
                "slug": "newsletter-signup",
                "description": "Email newsletter signup form with inline button.",
                "category": "forms",
                "tags": ["newsletter", "email", "signup", "subscription"],
                "section": "Forms"
            },
            {
                "name": "Login Form",
                "slug": "login-form",
                "description": "User login form with remember me checkbox.",
                "category": "forms",
                "tags": ["login", "auth", "form", "user"],
                "section": "Forms"
            },
            {
                "name": "Search Bar",
                "slug": "search-bar",
                "description": "Search input with icon and autocomplete styling.",
                "category": "inputs",
                "tags": ["search", "input", "icon", "autocomplete"],
                "section": "Forms"
            },
            
            # Components
            {
                "name": "Alert Banner",
                "slug": "alert-banner",
                "description": "Dismissible alert banner with multiple variants.",
                "category": "feedback",
                "tags": ["alert", "banner", "notification", "dismissible"],
                "section": "Components"
            },
            {
                "name": "Modal Dialog",
                "slug": "modal-dialog",
                "description": "Centered modal dialog with backdrop overlay.",
                "category": "overlays",
                "tags": ["modal", "dialog", "overlay", "popup"],
                "section": "Components"
            },
            {
                "name": "Loading Spinner",
                "slug": "loading-spinner",
                "description": "Animated loading spinners in various styles.",
                "category": "feedback",
                "tags": ["loading", "spinner", "animation", "progress"],
                "section": "Components"
            },
            {
                "name": "Badge",
                "slug": "badge",
                "description": "Small status badges in different colors and sizes.",
                "category": "data_display",
                "tags": ["badge", "status", "label", "tag"],
                "section": "Components"
            },
            {
                "name": "Button Group",
                "slug": "button-group",
                "description": "Grouped buttons with various states and styles.",
                "category": "buttons",
                "tags": ["button", "group", "actions", "toolbar"],
                "section": "Components"
            },
            {
                "name": "Progress Bar",
                "slug": "progress-bar",
                "description": "Progress indicators with percentage and animations.",
                "category": "feedback",
                "tags": ["progress", "bar", "percentage", "loading"],
                "section": "Components"
            },
            {
                "name": "Tabs",
                "slug": "tabs",
                "description": "Horizontal and vertical tab navigation.",
                "category": "navigation",
                "tags": ["tabs", "navigation", "content", "switch"],
                "section": "Components"
            },
            {
                "name": "Dropdown Menu",
                "slug": "dropdown-menu",
                "description": "Dropdown menu with links and dividers.",
                "category": "overlays",
                "tags": ["dropdown", "menu", "navigation", "actions"],
                "section": "Components"
            },
            {
                "name": "Tooltip",
                "slug": "tooltip",
                "description": "Hover tooltips with multiple positions.",
                "category": "overlays",
                "tags": ["tooltip", "hover", "help", "info"],
                "section": "Components"
            },
            {
                "name": "Card",
                "slug": "card",
                "description": "Flexible content cards with headers and actions.",
                "category": "cards",
                "tags": ["card", "content", "container", "layout"],
                "section": "Components"
            }
        ]
        
        components = []
        for comp_data in components_data:
            manifest = ComponentManifest(
                id=f"hyperui/{comp_data['slug']}",
                provider=Provider.HYPERUI,
                name=comp_data["name"],
                slug=comp_data["slug"],
                category=ComponentCategory(comp_data["category"]),
                tags=comp_data["tags"],
                license=License(
                    type=LicenseType.MIT,
                    url="https://github.com/markmead/hyperui/blob/main/LICENSE",
                    redistribute=True,
                    commercial=True
                ),
                source=Source(
                    url="https://github.com/markmead/hyperui",
                    branch="main"
                ),
                framework=Framework(
                    react=True,
                    vue=True,
                    svelte=True,
                    solid=True,
                    angular=True,
                    html=True
                ),
                tailwind=TailwindConfig(
                    version=TailwindVersion.V3,
                    plugin_deps=[],
                    required_classes=[]
                ),
                runtime_deps=[],
                install=InstallPlan(
                    steps=[
                        {
                            "type": "copy",
                            "description": f"Copy {comp_data['name']} HTML/CSS from HyperUI website"
                        }
                    ]
                ),
                code=ComponentCode(
                    html=self._generate_sample_html(comp_data)
                ),
                access=ComponentAccess(
                    copy_paste=True,
                    free=True,
                    pro=False
                ),
                description=comp_data["description"],
                documentation_url=f"https://www.hyperui.dev/components/{comp_data['section'].lower().replace(' ', '-')}/{comp_data['slug']}",
                demo_url=f"https://www.hyperui.dev/components/{comp_data['section'].lower().replace(' ', '-')}/{comp_data['slug']}",
                keywords=[comp_data["slug"], "tailwind", "html", "css", "free"] + comp_data["tags"]
            )
            components.append(manifest)
        
        return components
    
    def _generate_sample_html(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample HTML for the component."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        
        if "button" in slug.lower():
            return f"""<button class="inline-block rounded bg-indigo-600 px-8 py-3 text-sm font-medium text-white transition hover:bg-indigo-700 focus:outline-none focus:ring focus:ring-yellow-400">
  {name}
</button>"""
        elif "card" in slug.lower():
            return f"""<div class="overflow-hidden rounded-lg bg-white shadow">
  <div class="px-4 py-5 sm:p-6">
    <h3 class="text-lg font-medium text-gray-900">{name}</h3>
    <p class="mt-1 text-sm text-gray-500">Sample card content goes here.</p>
  </div>
</div>"""
        elif "form" in slug.lower():
            return f"""<form class="space-y-4">
  <div>
    <label class="block text-sm font-medium text-gray-700">{name}</label>
    <input type="text" class="mt-1 w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" />
  </div>
  <button type="submit" class="w-full rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700">
    Submit
  </button>
</form>"""
        else:
            return f"""<div class="rounded-lg border border-gray-200 p-4">
  <h3 class="font-medium text-gray-900">{name}</h3>
  <p class="text-sm text-gray-500">{comp_data['description']}</p>
</div>"""