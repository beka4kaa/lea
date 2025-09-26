"""daisyUI provider implementation."""

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
class DaisyUIProvider(BaseProvider):
    """daisyUI component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.DAISYUI
    
    @property
    def base_url(self) -> str:
        return "https://daisyui.com"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List daisyUI components."""
        # Since daisyUI is a Tailwind plugin with predefined classes,
        # we'll create manifests for the main component classes
        components = await self._get_all_components()
        
        # Apply pagination
        start = offset
        end = offset + limit
        return components[start:end]
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific daisyUI component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in daisyUI")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all daisyUI components."""
        # daisyUI component data
        daisy_components = [
            # Actions
            {
                "name": "Button",
                "slug": "btn",
                "category": "buttons",
                "description": "Button in different sizes and colors",
                "css_classes": ["btn", "btn-primary", "btn-secondary", "btn-accent", "btn-ghost", "btn-link"],
                "modifiers": ["btn-lg", "btn-md", "btn-sm", "btn-xs", "btn-wide", "btn-block", "btn-circle", "btn-square"]
            },
            {
                "name": "Dropdown",
                "slug": "dropdown",
                "category": "navigation", 
                "description": "Dropdown menu with customizable content",
                "css_classes": ["dropdown", "dropdown-content", "dropdown-toggle"],
                "modifiers": ["dropdown-end", "dropdown-top", "dropdown-bottom", "dropdown-left", "dropdown-right"]
            },
            {
                "name": "Modal",
                "slug": "modal",
                "category": "layouts",
                "description": "Modal dialog for displaying content",
                "css_classes": ["modal", "modal-box", "modal-action"],
                "modifiers": ["modal-open", "modal-top", "modal-middle", "modal-bottom"]
            },
            {
                "name": "Swap",
                "slug": "swap",
                "category": "other",
                "description": "Swap allows you to toggle the visibility of two elements",
                "css_classes": ["swap", "swap-on", "swap-off"],
                "modifiers": ["swap-rotate", "swap-flip"]
            },
            
            # Data Display
            {
                "name": "Alert",
                "slug": "alert",
                "category": "feedback",
                "description": "Alert messages in different colors",
                "css_classes": ["alert", "alert-info", "alert-success", "alert-warning", "alert-error"],
                "modifiers": []
            },
            {
                "name": "Avatar",
                "slug": "avatar",
                "category": "data_display",
                "description": "Avatar with placeholder and presence indicator",
                "css_classes": ["avatar", "avatar-group"],
                "modifiers": ["online", "offline"]
            },
            {
                "name": "Badge",
                "slug": "badge",
                "category": "data_display",
                "description": "Badge for status and labels",
                "css_classes": ["badge", "badge-primary", "badge-secondary", "badge-accent", "badge-ghost"],
                "modifiers": ["badge-lg", "badge-md", "badge-sm", "badge-xs"]
            },
            {
                "name": "Card",
                "slug": "card",
                "category": "layouts",
                "description": "Card container with title, content and actions",
                "css_classes": ["card", "card-body", "card-title", "card-actions"],
                "modifiers": ["card-compact", "card-normal", "card-side", "image-full"]
            },
            {
                "name": "Carousel",
                "slug": "carousel",
                "category": "data_display",
                "description": "Carousel for displaying multiple items",
                "css_classes": ["carousel", "carousel-item"],
                "modifiers": ["carousel-center", "carousel-end", "carousel-vertical"]
            },
            {
                "name": "Chat",
                "slug": "chat",
                "category": "data_display",
                "description": "Chat bubble for messaging interfaces",
                "css_classes": ["chat", "chat-start", "chat-end", "chat-image", "chat-header", "chat-bubble", "chat-footer"],
                "modifiers": ["chat-bubble-primary", "chat-bubble-secondary", "chat-bubble-accent"]
            },
            {
                "name": "Collapse",
                "slug": "collapse",
                "category": "layouts",
                "description": "Collapsible content area",
                "css_classes": ["collapse", "collapse-title", "collapse-content"],
                "modifiers": ["collapse-arrow", "collapse-plus", "collapse-open", "collapse-close"]
            },
            {
                "name": "Countdown",
                "slug": "countdown",
                "category": "data_display",
                "description": "Countdown timer component",
                "css_classes": ["countdown"],
                "modifiers": []
            },
            {
                "name": "Diff",
                "slug": "diff",
                "category": "data_display",
                "description": "Show differences between two items",
                "css_classes": ["diff", "diff-item-1", "diff-item-2", "diff-resizer"],
                "modifiers": []
            },
            {
                "name": "Kbd",
                "slug": "kbd",
                "category": "data_display",
                "description": "Keyboard key styling",
                "css_classes": ["kbd"],
                "modifiers": ["kbd-lg", "kbd-md", "kbd-sm", "kbd-xs"]
            },
            {
                "name": "Stat",
                "slug": "stat",
                "category": "data_display",
                "description": "Statistics display component",
                "css_classes": ["stats", "stat", "stat-title", "stat-value", "stat-desc", "stat-figure"],
                "modifiers": ["stats-vertical", "stats-horizontal"]
            },
            {
                "name": "Table",
                "slug": "table",
                "category": "data_display",
                "description": "Table with styling options",
                "css_classes": ["table", "table-zebra", "table-pin-rows", "table-pin-cols"],
                "modifiers": ["table-xs", "table-sm", "table-md", "table-lg"]
            },
            {
                "name": "Timeline",
                "slug": "timeline",
                "category": "data_display",
                "description": "Timeline component for showing chronological content",
                "css_classes": ["timeline", "timeline-start", "timeline-middle", "timeline-end"],
                "modifiers": ["timeline-vertical", "timeline-horizontal", "timeline-compact"]
            },
            
            # Data Input
            {
                "name": "Checkbox",
                "slug": "checkbox",
                "category": "forms",
                "description": "Checkbox input with custom styling",
                "css_classes": ["checkbox", "checkbox-primary", "checkbox-secondary", "checkbox-accent"],
                "modifiers": ["checkbox-lg", "checkbox-md", "checkbox-sm", "checkbox-xs"]
            },
            {
                "name": "File Input",
                "slug": "file-input",
                "category": "forms",
                "description": "File input with custom styling",
                "css_classes": ["file-input", "file-input-bordered", "file-input-ghost"],
                "modifiers": ["file-input-lg", "file-input-md", "file-input-sm", "file-input-xs"]
            },
            {
                "name": "Input",
                "slug": "input",
                "category": "forms",
                "description": "Text input with various styles",
                "css_classes": ["input", "input-bordered", "input-ghost", "input-primary", "input-secondary"],
                "modifiers": ["input-lg", "input-md", "input-sm", "input-xs"]
            },
            {
                "name": "Radio",
                "slug": "radio",
                "category": "forms",
                "description": "Radio button with custom styling",
                "css_classes": ["radio", "radio-primary", "radio-secondary", "radio-accent"],
                "modifiers": ["radio-lg", "radio-md", "radio-sm", "radio-xs"]
            },
            {
                "name": "Range",
                "slug": "range",
                "category": "forms",
                "description": "Range slider input",
                "css_classes": ["range", "range-primary", "range-secondary", "range-accent"],
                "modifiers": ["range-lg", "range-md", "range-sm", "range-xs"]
            },
            {
                "name": "Rating",
                "slug": "rating",
                "category": "forms",
                "description": "Star rating input component",
                "css_classes": ["rating", "rating-half"],
                "modifiers": ["rating-lg", "rating-md", "rating-sm", "rating-xs"]
            },
            {
                "name": "Select",
                "slug": "select",
                "category": "forms",
                "description": "Select dropdown input",
                "css_classes": ["select", "select-bordered", "select-ghost", "select-primary"],
                "modifiers": ["select-lg", "select-md", "select-sm", "select-xs"]
            },
            {
                "name": "Textarea",
                "slug": "textarea",
                "category": "forms",
                "description": "Textarea input with custom styling",
                "css_classes": ["textarea", "textarea-bordered", "textarea-ghost", "textarea-primary"],
                "modifiers": ["textarea-lg", "textarea-md", "textarea-sm", "textarea-xs"]
            },
            {
                "name": "Toggle",
                "slug": "toggle",
                "category": "forms",
                "description": "Toggle switch input",
                "css_classes": ["toggle", "toggle-primary", "toggle-secondary", "toggle-accent"],
                "modifiers": ["toggle-lg", "toggle-md", "toggle-sm", "toggle-xs"]
            },
            
            # Layout
            {
                "name": "Artboard",
                "slug": "artboard",
                "category": "layouts",
                "description": "Container for showcasing content in various screen sizes",
                "css_classes": ["artboard", "artboard-demo"],
                "modifiers": ["phone-1", "phone-2", "phone-3", "phone-4", "phone-5", "phone-6"]
            },
            {
                "name": "Divider",
                "slug": "divider",
                "category": "layouts",
                "description": "Divider line with optional text",
                "css_classes": ["divider"],
                "modifiers": ["divider-horizontal", "divider-vertical"]
            },
            {
                "name": "Drawer",
                "slug": "drawer",
                "category": "layouts",
                "description": "Drawer sidebar layout",
                "css_classes": ["drawer", "drawer-toggle", "drawer-content", "drawer-side", "drawer-overlay"],
                "modifiers": ["drawer-open", "drawer-end"]
            },
            {
                "name": "Footer",
                "slug": "footer",
                "category": "layouts",
                "description": "Footer container with flexible layout",
                "css_classes": ["footer", "footer-title"],
                "modifiers": ["footer-center"]
            },
            {
                "name": "Hero",
                "slug": "hero",
                "category": "layouts",
                "description": "Hero section for landing pages",
                "css_classes": ["hero", "hero-content", "hero-overlay"],
                "modifiers": ["hero-min-h-screen"]
            },
            {
                "name": "Indicator",
                "slug": "indicator",
                "category": "layouts",
                "description": "Indicator for showing badges or status on other elements",
                "css_classes": ["indicator", "indicator-item"],
                "modifiers": ["indicator-top", "indicator-middle", "indicator-bottom", "indicator-start", "indicator-center", "indicator-end"]
            },
            {
                "name": "Join",
                "slug": "join",
                "category": "layouts",
                "description": "Join elements together without border radius",
                "css_classes": ["join", "join-item"],
                "modifiers": ["join-vertical", "join-horizontal"]
            },
            {
                "name": "Mask",
                "slug": "mask",
                "category": "layouts",
                "description": "Mask for cropping content to specific shapes",
                "css_classes": ["mask"],
                "modifiers": ["mask-circle", "mask-triangle", "mask-heart", "mask-hexagon", "mask-decagon", "mask-pentagon", "mask-diamond", "mask-square", "mask-parallelogram"]
            },
            {
                "name": "Stack",
                "slug": "stack",
                "category": "layouts",
                "description": "Stack elements on top of each other",
                "css_classes": ["stack"],
                "modifiers": []
            },
            
            # Navigation
            {
                "name": "Breadcrumbs",
                "slug": "breadcrumbs",
                "category": "navigation",
                "description": "Breadcrumb navigation component",
                "css_classes": ["breadcrumbs"],
                "modifiers": []
            },
            {
                "name": "Bottom Navigation",
                "slug": "btm-nav",
                "category": "navigation",
                "description": "Bottom navigation bar",
                "css_classes": ["btm-nav"],
                "modifiers": ["btm-nav-xs", "btm-nav-sm", "btm-nav-md", "btm-nav-lg"]
            },
            {
                "name": "Link",
                "slug": "link",
                "category": "navigation",
                "description": "Link styling with hover effects",
                "css_classes": ["link", "link-primary", "link-secondary", "link-accent"],
                "modifiers": ["link-hover", "link-neutral"]
            },
            {
                "name": "Menu",
                "slug": "menu",
                "category": "navigation",
                "description": "Vertical menu component",
                "css_classes": ["menu", "menu-title"],
                "modifiers": ["menu-horizontal", "menu-vertical", "menu-lg", "menu-md", "menu-sm", "menu-xs"]
            },
            {
                "name": "Navbar",
                "slug": "navbar",
                "category": "navigation",
                "description": "Navigation bar component",
                "css_classes": ["navbar", "navbar-start", "navbar-center", "navbar-end"],
                "modifiers": []
            },
            {
                "name": "Pagination",
                "slug": "pagination", 
                "category": "navigation",
                "description": "Pagination component for navigating pages",
                "css_classes": ["join", "btn"],
                "modifiers": ["btn-active", "btn-disabled"]
            },
            {
                "name": "Steps",
                "slug": "steps",
                "category": "navigation",
                "description": "Step indicator for multi-step processes",
                "css_classes": ["steps", "step", "step-primary", "step-secondary", "step-accent"],
                "modifiers": ["steps-vertical", "steps-horizontal"]
            },
            {
                "name": "Tab",
                "slug": "tab",
                "category": "navigation",
                "description": "Tab component for content switching",
                "css_classes": ["tabs", "tab", "tab-active"],
                "modifiers": ["tabs-boxed", "tabs-bordered", "tabs-lifted", "tab-lg", "tab-md", "tab-sm", "tab-xs"]
            },
            
            # Feedback
            {
                "name": "Loading",
                "slug": "loading",
                "category": "feedback",
                "description": "Loading spinner component",
                "css_classes": ["loading", "loading-spinner", "loading-dots", "loading-ring", "loading-ball", "loading-bars", "loading-infinity"],
                "modifiers": ["loading-lg", "loading-md", "loading-sm", "loading-xs"]
            },
            {
                "name": "Progress",
                "slug": "progress",
                "category": "feedback",
                "description": "Progress bar component",
                "css_classes": ["progress", "progress-primary", "progress-secondary", "progress-accent"],
                "modifiers": []
            },
            {
                "name": "Radial Progress",
                "slug": "radial-progress",
                "category": "feedback",
                "description": "Circular progress indicator",
                "css_classes": ["radial-progress"],
                "modifiers": []
            },
            {
                "name": "Skeleton",
                "slug": "skeleton",
                "category": "feedback",
                "description": "Skeleton placeholder for loading content",
                "css_classes": ["skeleton"],
                "modifiers": []
            },
            {
                "name": "Toast",
                "slug": "toast",
                "category": "feedback",
                "description": "Toast notification component",
                "css_classes": ["toast", "toast-top", "toast-bottom", "toast-start", "toast-center", "toast-end"],
                "modifiers": []
            },
            {
                "name": "Tooltip",
                "slug": "tooltip",
                "category": "feedback",
                "description": "Tooltip component for additional information",
                "css_classes": ["tooltip", "tooltip-open"],
                "modifiers": ["tooltip-top", "tooltip-bottom", "tooltip-left", "tooltip-right", "tooltip-primary", "tooltip-secondary", "tooltip-accent"]
            },
            
            # Mockup
            {
                "name": "Browser",
                "slug": "mockup-browser",
                "category": "layouts",
                "description": "Browser mockup for showcasing web content",
                "css_classes": ["mockup-browser", "mockup-browser-toolbar"],
                "modifiers": []
            },
            {
                "name": "Code",
                "slug": "mockup-code",
                "category": "layouts",
                "description": "Code editor mockup",
                "css_classes": ["mockup-code"],
                "modifiers": []
            },
            {
                "name": "Phone",
                "slug": "mockup-phone",
                "category": "layouts",
                "description": "Phone mockup for showcasing mobile content",
                "css_classes": ["mockup-phone"],
                "modifiers": []
            },
            {
                "name": "Window",
                "slug": "mockup-window",
                "category": "layouts",
                "description": "Window mockup for showcasing desktop applications",
                "css_classes": ["mockup-window"],
                "modifiers": []
            }
        ]
        
        components = []
        for comp_data in daisy_components:
            manifest = self._create_manifest_from_data(comp_data)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any]) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        # Generate HTML/JSX example
        html_example = self._generate_html_example(comp_data)
        jsx_example = self._generate_jsx_example(comp_data)
        
        return ComponentManifest(
            id=f"daisyui/{slug}",
            provider=Provider.DAISYUI,
            name=name,
            slug=slug,
            category=ComponentCategory(category),
            tags=["daisyui", "tailwind", "css", "component", slug] + comp_data.get("css_classes", []),
            license=License(
                type=LicenseType.MIT,
                url="https://github.com/saadeghi/daisyui/blob/master/LICENSE",
                redistribute=True,
                commercial=True
            ),
            source=Source(
                url="https://github.com/saadeghi/daisyui",
                branch="master"
            ),
            framework=Framework(
                react=True,
                next=True,
                vue=True,
                svelte=True,
                angular=True
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,  # daisyUI supports both v3 and v4
                plugin_deps=["daisyui"],
                required_classes=comp_data.get("css_classes", []) + comp_data.get("modifiers", [])
            ),
            runtime_deps=[],
            install=InstallPlan(
                npm=["daisyui"],
                steps=[
                    {
                        "type": "npm",
                        "command": "npm install -D daisyui",
                        "description": "Install daisyUI plugin"
                    },
                    {
                        "type": "patch",
                        "file_path": "tailwind.config.js",
                        "content": 'plugins: [require("daisyui")]',
                        "description": "Add daisyUI to Tailwind config"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=jsx_example,
                jsx=jsx_example,
                css=None  # daisyUI uses CSS classes, no custom CSS needed
            ),
            access=ComponentAccess(
                copy_paste=True,
                cli=None,
                pro=False
            ),
            description=comp_data["description"],
            documentation_url=f"https://daisyui.com/components/{slug}",
            demo_url=f"https://daisyui.com/components/{slug}",
            keywords=[slug, "daisyui", "tailwind", "css"] + comp_data.get("css_classes", [])
        )
    
    def _generate_html_example(self, comp_data: Dict[str, Any]) -> str:
        """Generate HTML example for component."""
        slug = comp_data["slug"]
        css_classes = comp_data.get("css_classes", [])
        
        if not css_classes:
            return f'<div class="{slug}">Example {comp_data["name"]}</div>'
        
        main_class = css_classes[0]
        
        # Component-specific examples
        if slug == "btn":
            return '<button class="btn">Button</button>'
        elif slug == "input":
            return '<input type="text" placeholder="Type here" class="input input-bordered w-full max-w-xs" />'
        elif slug == "card":
            return '''<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Card title!</h2>
    <p>If a dog chews shoes whose shoes does he choose?</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
    </div>
  </div>
</div>'''
        elif slug == "alert":
            return '<div class="alert alert-info"><span>Info alert</span></div>'
        else:
            return f'<div class="{main_class}">{comp_data["name"]} example</div>'
    
    def _generate_jsx_example(self, comp_data: Dict[str, Any]) -> str:
        """Generate JSX/React example for component."""
        html = self._generate_html_example(comp_data)
        
        # Convert HTML to JSX (basic conversion)
        jsx = html.replace('class=', 'className=')
        jsx = jsx.replace('/>', ' />')
        
        # Wrap in React component
        component_name = comp_data["name"].replace(" ", "")
        
        return f'''export function {component_name}Example() {{
  return (
    {jsx}
  );
}}'''