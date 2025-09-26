"""BentoGrids provider implementation - Specialized Bento Grid Collection."""

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
class BentoGridsProvider(HTTPProvider):
    """BentoGrids specialized collection provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.BENTOGRIDS
    
    @property
    def base_url(self) -> str:
        return "https://bentogrids.com"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List BentoGrids components."""
        try:
            components = await self._get_all_components()
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            print(f"Error listing BentoGrids components: {e}")
            return []
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific BentoGrids component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in BentoGrids")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all BentoGrids components."""
        # BentoGrids specialized bento grid layouts
        bento_components = [
            {
                "name": "Classic Bento Grid",
                "slug": "classic-bento-grid",
                "category": "layouts",
                "description": "Traditional bento grid layout with responsive cells",
                "tags": ["bento", "grid", "classic", "responsive"],
                "features": ["responsive", "auto-fit", "gap-control"],
                "css_grid": True
            },
            {
                "name": "Masonry Bento",
                "slug": "masonry-bento",
                "category": "layouts", 
                "description": "Masonry-style bento grid with dynamic heights",
                "tags": ["bento", "masonry", "dynamic", "heights"],
                "features": ["masonry", "dynamic-height", "pinterest-style"],
                "css_grid": True
            },
            {
                "name": "Feature Showcase Bento",
                "slug": "feature-showcase-bento",
                "category": "layouts",
                "description": "Bento grid optimized for showcasing features",
                "tags": ["bento", "features", "showcase", "highlight"],
                "features": ["feature-cards", "highlight", "call-to-action"],
                "css_grid": True
            },
            {
                "name": "Portfolio Bento Grid",
                "slug": "portfolio-bento-grid",
                "category": "layouts",
                "description": "Creative portfolio layout using bento grid",
                "tags": ["bento", "portfolio", "creative", "gallery"],
                "features": ["portfolio", "image-focus", "hover-effects"],
                "css_grid": True
            },
            {
                "name": "Dashboard Bento",
                "slug": "dashboard-bento",
                "category": "layouts",
                "description": "Dashboard layout with bento grid arrangement",
                "tags": ["bento", "dashboard", "metrics", "widgets"],
                "features": ["dashboard", "widgets", "data-display"],
                "css_grid": True
            },
            {
                "name": "Blog Bento Layout",
                "slug": "blog-bento-layout",
                "category": "layouts",
                "description": "Blog post layout using bento grid system",
                "tags": ["bento", "blog", "articles", "content"],
                "features": ["blog", "content", "reading-focused"],
                "css_grid": True
            },
            {
                "name": "Product Grid Bento",
                "slug": "product-grid-bento",
                "category": "layouts",
                "description": "E-commerce product grid with bento styling",
                "tags": ["bento", "product", "ecommerce", "catalog"],
                "features": ["ecommerce", "product-cards", "pricing"],
                "css_grid": True
            },
            {
                "name": "Team Bento Grid",
                "slug": "team-bento-grid",
                "category": "layouts",
                "description": "Team member showcase using bento layout",
                "tags": ["bento", "team", "members", "profiles"],
                "features": ["team", "profiles", "social-links"],
                "css_grid": True
            },
            {
                "name": "Service Bento Layout",
                "slug": "service-bento-layout",
                "category": "layouts",
                "description": "Service offerings displayed in bento grid",
                "tags": ["bento", "services", "offerings", "business"],
                "features": ["services", "business", "pricing-tiers"],
                "css_grid": True
            },
            {
                "name": "Stats Bento Grid",
                "slug": "stats-bento-grid",
                "category": "data_display",
                "description": "Statistics and metrics in bento arrangement",
                "tags": ["bento", "stats", "metrics", "analytics"],
                "features": ["statistics", "metrics", "counters"],
                "css_grid": True
            },
            {
                "name": "Timeline Bento",
                "slug": "timeline-bento",
                "category": "layouts",
                "description": "Timeline layout using bento grid structure",
                "tags": ["bento", "timeline", "chronological", "events"],
                "features": ["timeline", "events", "chronological"],
                "css_grid": True
            },
            {
                "name": "Gallery Bento Grid",
                "slug": "gallery-bento-grid",
                "category": "data_display",
                "description": "Image gallery with bento grid arrangement",
                "tags": ["bento", "gallery", "images", "photography"],
                "features": ["gallery", "lightbox", "image-optimization"],
                "css_grid": True
            },
            {
                "name": "Testimonial Bento",
                "slug": "testimonial-bento",
                "category": "layouts",
                "description": "Customer testimonials in bento layout",
                "tags": ["bento", "testimonials", "reviews", "social-proof"],
                "features": ["testimonials", "reviews", "social-proof"],
                "css_grid": True
            },
            {
                "name": "CTA Bento Grid",
                "slug": "cta-bento-grid",
                "category": "layouts",
                "description": "Call-to-action sections in bento arrangement",
                "tags": ["bento", "cta", "call-to-action", "conversion"],
                "features": ["cta", "conversion", "buttons"],
                "css_grid": True
            },
            {
                "name": "Animated Bento Grid",
                "slug": "animated-bento-grid",
                "category": "animated",
                "description": "Bento grid with smooth animations",
                "tags": ["bento", "animated", "transitions", "interactive"],
                "features": ["animations", "hover-effects", "transitions"],
                "css_grid": True
            },
            {
                "name": "Responsive Bento System",
                "slug": "responsive-bento-system",
                "category": "layouts",
                "description": "Complete responsive bento grid system",
                "tags": ["bento", "responsive", "system", "adaptive"],
                "features": ["responsive", "mobile-first", "breakpoints"],
                "css_grid": True
            }
        ]
        
        components = []
        for comp_data in bento_components:
            manifest = self._create_manifest_from_data(comp_data)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any]) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        # Generate sample code for bento grids
        sample_code = self._generate_bento_code(comp_data)
        
        return ComponentManifest(
            id=f"bentogrids/{slug}",
            provider=Provider.BENTOGRIDS,
            name=name,
            slug=slug,
            category=ComponentCategory(category) if isinstance(category, str) else category,
            tags=comp_data["tags"],
            license=License(
                type=LicenseType.MIT,
                url="https://bentogrids.com/license",
                notes="BentoGrids components under MIT license",
                redistribute=True,
                commercial=True
            ),
            source=Source(
                url=f"https://bentogrids.com/grids/{slug}",
                branch=None
            ),
            framework=Framework(
                react=True,
                next=True,
                vue=True,  # CSS Grid works with all frameworks
                svelte=True,
                angular=True
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,
                plugin_deps=[],
                required_classes=["grid", "grid-cols-*", "gap-*", "col-span-*", "row-span-*"]
            ),
            runtime_deps=[],
            install=InstallPlan(
                npm=[],
                steps=[
                    {
                        "type": "info",
                        "description": "BentoGrids uses CSS Grid - no additional dependencies required"
                    },
                    {
                        "type": "action",
                        "description": "Copy the CSS Grid classes and adjust content to your needs"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=sample_code,
                css=self._generate_css_code(comp_data)
            ),
            access=ComponentAccess(
                copy_paste=True,
                pro=False
            ),
            description=comp_data["description"],
            documentation_url=f"https://bentogrids.com/grids/{slug}",
            demo_url=f"https://bentogrids.com/demo/{slug}",
            keywords=comp_data["tags"] + ["bentogrids", "css-grid", "layout"]
        )
    
    def _generate_bento_code(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample bento grid code."""
        slug = comp_data["slug"]
        name = comp_data["name"]
        
        if "classic" in slug:
            return '''export function ClassicBentoGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-6 gap-4 p-4">
      {/* Large feature card */}
      <div className="col-span-1 md:col-span-2 lg:col-span-3 row-span-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-6 text-white">
        <h2 className="text-2xl font-bold mb-2">Featured Content</h2>
        <p className="text-blue-100">Main highlight goes here</p>
      </div>
      
      {/* Small cards */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold mb-2">Quick Stats</h3>
        <p className="text-3xl font-bold text-blue-600">42K</p>
      </div>
      
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold mb-2">Growth</h3>
        <p className="text-3xl font-bold text-green-600">+12%</p>
      </div>
      
      {/* Wide card */}
      <div className="col-span-1 md:col-span-2 bg-gray-50 rounded-xl p-4">
        <h3 className="font-semibold mb-2">Recent Activity</h3>
        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm">User signed up</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span className="text-sm">Order completed</span>
          </div>
        </div>
      </div>
      
      {/* Additional cards */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold mb-2">Revenue</h3>
        <p className="text-2xl font-bold text-purple-600">$24.5K</p>
      </div>
      
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold mb-2">Users</h3>
        <p className="text-2xl font-bold text-orange-600">1.2K</p>
      </div>
    </div>
  );
}'''
        
        elif "masonry" in slug:
            return '''export function MasonryBento() {
  return (
    <div className="columns-1 md:columns-2 lg:columns-3 xl:columns-4 gap-4 p-4">
      <div className="break-inside-avoid mb-4 bg-white rounded-xl p-6 shadow-sm border">
        <h3 className="font-semibold mb-3">Short Content</h3>
        <p className="text-gray-600">Brief description here.</p>
      </div>
      
      <div className="break-inside-avoid mb-4 bg-gradient-to-br from-pink-500 to-rose-600 rounded-xl p-6 text-white">
        <h3 className="font-semibold mb-3">Featured Item</h3>
        <p className="text-pink-100 mb-4">
          Longer content that takes up more vertical space. This creates the 
          natural masonry effect where items have different heights.
        </p>
        <button className="bg-white text-pink-600 px-4 py-2 rounded-lg font-medium">
          Learn More
        </button>
      </div>
      
      <div className="break-inside-avoid mb-4 bg-white rounded-xl p-6 shadow-sm border">
        <h3 className="font-semibold mb-3">Statistics</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-2xl font-bold text-blue-600">150+</p>
            <p className="text-sm text-gray-500">Projects</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-green-600">98%</p>
            <p className="text-sm text-gray-500">Success</p>
          </div>
        </div>
      </div>
      
      <div className="break-inside-avoid mb-4 bg-white rounded-xl p-6 shadow-sm border">
        <h3 className="font-semibold mb-3">Gallery</h3>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-gray-200 rounded-lg aspect-square"></div>
          <div className="bg-gray-200 rounded-lg aspect-square"></div>
          <div className="bg-gray-200 rounded-lg aspect-square col-span-2"></div>
        </div>
      </div>
    </div>
  );
}'''
        
        elif "dashboard" in slug:
            return '''export function DashboardBento() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-6 p-6">
      {/* Main chart area */}
      <div className="col-span-1 md:col-span-2 lg:col-span-4 xl:col-span-4 row-span-2 bg-white rounded-2xl p-6 shadow-sm border">
        <h2 className="text-xl font-semibold mb-4">Analytics Overview</h2>
        <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <span className="text-gray-500">Chart Component</span>
        </div>
      </div>
      
      {/* KPI Cards */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Total Revenue</h3>
        <p className="text-2xl font-bold text-green-600">$45.2K</p>
        <p className="text-sm text-green-500 mt-1">↗ +12.5%</p>
      </div>
      
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="text-sm font-medium text-gray-500 mb-1">New Users</h3>
        <p className="text-2xl font-bold text-blue-600">2.4K</p>
        <p className="text-sm text-blue-500 mt-1">↗ +8.2%</p>
      </div>
      
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Conversion</h3>
        <p className="text-2xl font-bold text-purple-600">3.2%</p>
        <p className="text-sm text-red-500 mt-1">↘ -2.1%</p>
      </div>
      
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Orders</h3>
        <p className="text-2xl font-bold text-orange-600">892</p>
        <p className="text-sm text-orange-500 mt-1">↗ +15.3%</p>
      </div>
      
      {/* Recent activity */}
      <div className="col-span-1 md:col-span-2 bg-white rounded-xl p-6 shadow-sm border">
        <h3 className="font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm">New order from John Doe</span>
            <span className="text-xs text-gray-500 ml-auto">2m ago</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span className="text-sm">User registered</span>
            <span className="text-xs text-gray-500 ml-auto">5m ago</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <span className="text-sm">Payment processed</span>
            <span className="text-xs text-gray-500 ml-auto">8m ago</span>
          </div>
        </div>
      </div>
    </div>
  );
}'''
        
        else:
            # Generic bento grid template
            component_name = name.replace(" ", "")
            return f'''export function {component_name}() {{
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
      {{/* Main feature */}}
      <div className="col-span-1 md:col-span-2 row-span-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-6 text-white">
        <h2 className="text-xl font-bold mb-2">{name}</h2>
        <p className="text-indigo-100">Featured content area</p>
      </div>
      
      {{/* Secondary items */}}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-medium mb-2">Item 1</h3>
        <p className="text-sm text-gray-600">Content here</p>
      </div>
      
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-medium mb-2">Item 2</h3>
        <p className="text-sm text-gray-600">Content here</p>
      </div>
      
      <div className="col-span-1 md:col-span-2 bg-gray-50 rounded-xl p-4">
        <h3 className="font-medium mb-2">Wide Item</h3>
        <p className="text-sm text-gray-600">Spans multiple columns</p>
      </div>
    </div>
  );
}}'''
    
    def _generate_css_code(self, comp_data: Dict[str, Any]) -> str:
        """Generate accompanying CSS for bento grids."""
        return '''/* BentoGrid CSS */
.bento-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.bento-item {
  border-radius: 0.75rem;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.bento-feature {
  grid-column: span 2;
  grid-row: span 2;
}

@media (max-width: 768px) {
  .bento-feature {
    grid-column: span 1;
    grid-row: span 1;
  }
}'''