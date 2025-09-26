"""AlignUI provider implementation."""

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
class AlignUIProvider(HTTPProvider):
    """AlignUI component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.ALIGNUI
    
    @property
    def base_url(self) -> str:
        return "https://alignui.com"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List AlignUI components."""
        try:
            components = await self._get_all_components()
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            print(f"Error listing AlignUI components: {e}")
            return []
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific AlignUI component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in AlignUI")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all AlignUI components."""
        # AlignUI component catalog (Base free + Pro)
        alignui_components = {
            # Base (Free) Components
            "base": [
                {
                    "name": "Alert",
                    "slug": "alert",
                    "category": "feedback",
                    "description": "Flexible alert component with multiple variants",
                    "tags": ["alert", "notification", "feedback", "status"],
                    "runtime_deps": ["@radix-ui/react-alert-dialog"],
                    "pro": False
                },
                {
                    "name": "Avatar",
                    "slug": "avatar",
                    "category": "data_display",
                    "description": "User avatar component with fallback support",
                    "tags": ["avatar", "user", "profile", "image"],
                    "runtime_deps": ["@radix-ui/react-avatar"],
                    "pro": False
                },
                {
                    "name": "Badge",
                    "slug": "badge",
                    "category": "data_display",
                    "description": "Small status badge component",
                    "tags": ["badge", "status", "label", "tag"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Button",
                    "slug": "button",
                    "category": "buttons",
                    "description": "Customizable button component with variants",
                    "tags": ["button", "action", "click", "interactive"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Card",
                    "slug": "card",
                    "category": "layouts",
                    "description": "Flexible card container component",
                    "tags": ["card", "container", "layout", "content"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Checkbox",
                    "slug": "checkbox",
                    "category": "forms",
                    "description": "Checkbox input with custom styling",
                    "tags": ["checkbox", "input", "form", "selection"],
                    "runtime_deps": ["@radix-ui/react-checkbox"],
                    "pro": False
                },
                {
                    "name": "Dialog",
                    "slug": "dialog",
                    "category": "overlays",
                    "description": "Modal dialog component",
                    "tags": ["dialog", "modal", "overlay", "popup"],
                    "runtime_deps": ["@radix-ui/react-dialog"],
                    "pro": False
                },
                {
                    "name": "Dropdown Menu",
                    "slug": "dropdown-menu",
                    "category": "overlays",
                    "description": "Customizable dropdown menu component",
                    "tags": ["dropdown", "menu", "navigation", "overlay"],
                    "runtime_deps": ["@radix-ui/react-dropdown-menu"],
                    "pro": False
                },
                {
                    "name": "Input",
                    "slug": "input",
                    "category": "forms",
                    "description": "Styled input field component",
                    "tags": ["input", "form", "field", "text"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Label",
                    "slug": "label",
                    "category": "forms",
                    "description": "Form label component",
                    "tags": ["label", "form", "accessibility", "text"],
                    "runtime_deps": ["@radix-ui/react-label"],
                    "pro": False
                },
                {
                    "name": "Progress",
                    "slug": "progress",
                    "category": "feedback",
                    "description": "Progress indicator component",
                    "tags": ["progress", "loading", "indicator", "status"],
                    "runtime_deps": ["@radix-ui/react-progress"],
                    "pro": False
                },
                {
                    "name": "Radio Group",
                    "slug": "radio-group",
                    "category": "forms",
                    "description": "Radio button group component",
                    "tags": ["radio", "group", "selection", "form"],
                    "runtime_deps": ["@radix-ui/react-radio-group"],
                    "pro": False
                },
                {
                    "name": "Select",
                    "slug": "select",
                    "category": "forms",
                    "description": "Customizable select dropdown",
                    "tags": ["select", "dropdown", "form", "options"],
                    "runtime_deps": ["@radix-ui/react-select"],
                    "pro": False
                },
                {
                    "name": "Separator",
                    "slug": "separator",
                    "category": "layouts",
                    "description": "Visual separator component",
                    "tags": ["separator", "divider", "layout", "visual"],
                    "runtime_deps": ["@radix-ui/react-separator"],
                    "pro": False
                },
                {
                    "name": "Sheet",
                    "slug": "sheet",
                    "category": "overlays",
                    "description": "Side sheet/drawer component",
                    "tags": ["sheet", "drawer", "sidebar", "overlay"],
                    "runtime_deps": ["@radix-ui/react-dialog"],
                    "pro": False
                },
                {
                    "name": "Skeleton",
                    "slug": "skeleton",
                    "category": "feedback",
                    "description": "Loading skeleton placeholder",
                    "tags": ["skeleton", "loading", "placeholder", "shimmer"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Switch",
                    "slug": "switch",
                    "category": "forms",
                    "description": "Toggle switch component",
                    "tags": ["switch", "toggle", "form", "boolean"],
                    "runtime_deps": ["@radix-ui/react-switch"],
                    "pro": False
                },
                {
                    "name": "Table",
                    "slug": "table",
                    "category": "data_display",
                    "description": "Responsive table component",
                    "tags": ["table", "data", "grid", "display"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Tabs",
                    "slug": "tabs",
                    "category": "navigation",
                    "description": "Tab navigation component",
                    "tags": ["tabs", "navigation", "content", "switch"],
                    "runtime_deps": ["@radix-ui/react-tabs"],
                    "pro": False
                },
                {
                    "name": "Textarea",
                    "slug": "textarea",
                    "category": "forms",
                    "description": "Multi-line text input component",
                    "tags": ["textarea", "input", "form", "multiline"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Toast",
                    "slug": "toast",
                    "category": "feedback",
                    "description": "Toast notification component",
                    "tags": ["toast", "notification", "feedback", "message"],
                    "runtime_deps": ["@radix-ui/react-toast"],
                    "pro": False
                },
                {
                    "name": "Toggle",
                    "slug": "toggle",
                    "category": "forms",
                    "description": "Toggle button component",
                    "tags": ["toggle", "button", "state", "selection"],
                    "runtime_deps": ["@radix-ui/react-toggle"],
                    "pro": False
                },
                {
                    "name": "Tooltip",
                    "slug": "tooltip",
                    "category": "overlays",
                    "description": "Tooltip overlay component",
                    "tags": ["tooltip", "overlay", "information", "hint"],
                    "runtime_deps": ["@radix-ui/react-tooltip"],
                    "pro": False
                }
            ],
            
            # Pro Components (metadata only with deep links)
            "pro": [
                {
                    "name": "Advanced Data Table",
                    "slug": "advanced-data-table-pro",
                    "category": "data_display",
                    "description": "Professional data table with sorting, filtering, pagination, and export",
                    "tags": ["table", "data", "advanced", "pro", "sorting", "filtering"],
                    "runtime_deps": ["@tanstack/react-table"],
                    "pro": True
                },
                {
                    "name": "Calendar Pro",
                    "slug": "calendar-pro",
                    "category": "forms",
                    "description": "Full-featured calendar with events, scheduling, and time management",
                    "tags": ["calendar", "events", "schedule", "pro", "date"],
                    "runtime_deps": ["date-fns", "@radix-ui/react-popover"],
                    "pro": True
                },
                {
                    "name": "Chart Suite",
                    "slug": "chart-suite-pro",
                    "category": "data_display",
                    "description": "Professional chart components with animations and interactions",
                    "tags": ["charts", "graphs", "data", "pro", "visualization"],
                    "runtime_deps": ["recharts", "d3"],
                    "pro": True
                },
                {
                    "name": "Command Palette",
                    "slug": "command-palette-pro",
                    "category": "navigation",
                    "description": "Advanced command palette with fuzzy search and keyboard shortcuts",
                    "tags": ["command", "palette", "search", "pro", "keyboard"],
                    "runtime_deps": ["cmdk", "fuse.js"],
                    "pro": True
                },
                {
                    "name": "File Explorer",
                    "slug": "file-explorer-pro",
                    "category": "data_display",
                    "description": "Professional file explorer with tree view and file operations",
                    "tags": ["file", "explorer", "tree", "pro", "navigation"],
                    "runtime_deps": ["react-window"],
                    "pro": True
                },
                {
                    "name": "Form Builder",
                    "slug": "form-builder-pro",
                    "category": "forms",
                    "description": "Dynamic form builder with validation and conditional logic",
                    "tags": ["form", "builder", "dynamic", "pro", "validation"],
                    "runtime_deps": ["react-hook-form", "zod"],
                    "pro": True
                },
                {
                    "name": "Kanban Board",
                    "slug": "kanban-board-pro",
                    "category": "layouts",
                    "description": "Professional kanban board with drag & drop and customization",
                    "tags": ["kanban", "board", "drag", "pro", "project"],
                    "runtime_deps": ["@dnd-kit/core", "@dnd-kit/sortable"],
                    "pro": True
                },
                {
                    "name": "Rich Text Editor",
                    "slug": "rich-text-editor-pro",
                    "category": "forms",
                    "description": "Full-featured rich text editor with plugins and formatting",
                    "tags": ["editor", "rich", "text", "pro", "wysiwyg"],
                    "runtime_deps": ["@tiptap/react", "@tiptap/starter-kit"],
                    "pro": True
                }
            ]
        }
        
        components = []
        
        # Process base (free) components
        for comp_data in alignui_components["base"]:
            manifest = self._create_manifest_from_data(comp_data, is_pro=False)
            components.append(manifest)
        
        # Process pro components (metadata only with deep links)
        for comp_data in alignui_components["pro"]:
            manifest = self._create_manifest_from_data(comp_data, is_pro=True)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any], is_pro: bool = False) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        # Generate sample code only for base components
        sample_code = None if is_pro else self._generate_sample_code(comp_data)
        
        return ComponentManifest(
            id=f"alignui/{slug}",
            provider=Provider.ALIGNUI,
            name=name,
            slug=slug,
            category=ComponentCategory(category),
            tags=comp_data["tags"],
            license=License(
                type=LicenseType.CUSTOM if is_pro else LicenseType.MIT,
                url="https://alignui.com/pricing" if is_pro else "https://alignui.com/license",
                notes="Pro components require AlignUI Pro subscription" if is_pro else "Base components under MIT license",
                redistribute=not is_pro,
                commercial=True
            ),
            source=Source(
                url="https://alignui.com" if not is_pro else f"https://alignui.com/pro/components/{slug}",
                branch=None
            ),
            framework=Framework(
                react=True,
                next=True,
                vue=False,  # React-focused
                svelte=False,
                angular=False
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,
                plugin_deps=[],
                required_classes=[]
            ),
            runtime_deps=comp_data.get("runtime_deps", []),
            install=InstallPlan(
                npm=comp_data.get("runtime_deps", []),
                steps=[
                    {
                        "type": "info" if not is_pro else "warning",
                        "description": f"{'AlignUI Base component - free to use' if not is_pro else 'AlignUI Pro component - requires subscription for full access'}"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=sample_code if sample_code else None
            ),
            access=ComponentAccess(
                copy_paste=not is_pro,
                pro=is_pro
            ),
            description=comp_data["description"],
            documentation_url=f"https://alignui.com/components/{slug}",
            demo_url=f"https://alignui.com/components/{slug}" if not is_pro else f"https://alignui.com/pro/components/{slug}",
            keywords=comp_data["tags"] + ["alignui", "radix", "accessible"]
        )
    
    def _generate_sample_code(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample code for base components."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        
        # Component-specific code templates
        if slug == "button":
            return '''import { cn } from "@/lib/utils"
import { ButtonHTMLAttributes, forwardRef } from "react"

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link"
  size?: "default" | "sm" | "lg" | "icon"
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    return (
      <button
        className={cn(
          "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
          variant === "default" && "bg-primary text-primary-foreground hover:bg-primary/90",
          variant === "outline" && "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
          size === "default" && "h-10 px-4 py-2",
          size === "sm" && "h-9 rounded-md px-3",
          size === "lg" && "h-11 rounded-md px-8",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)

Button.displayName = "Button"

export { Button }'''
        
        elif slug == "card":
            return '''import { cn } from "@/lib/utils"
import { HTMLAttributes, forwardRef } from "react"

const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)}
      {...props}
    />
  )
)

const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)

const CardTitle = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />
  )
)

const CardContent = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)

export { Card, CardHeader, CardTitle, CardContent }'''
        
        elif slug == "input":
            return '''import { cn } from "@/lib/utils"
import { InputHTMLAttributes, forwardRef } from "react"

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)

Input.displayName = "Input"

export { Input }'''
        
        else:
            # Generic template
            component_name = name.replace(" ", "")
            return f'''import {{ cn }} from "@/lib/utils"
import {{ HTMLAttributes, forwardRef }} from "react"

export interface {component_name}Props extends HTMLAttributes<HTMLDivElement> {{}}

const {component_name} = forwardRef<HTMLDivElement, {component_name}Props>(
  ({{ className, ...props }}, ref) => (
    <div
      ref={{ref}}
      className={{cn("alignui-{slug}", className)}}
      {{...props}}
    />
  )
)

{component_name}.displayName = "{component_name}"

export {{ {component_name} }}'''