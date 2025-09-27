"""Enhanced shadcn/ui provider with proper code templates."""

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

# Шаблоны кода для Shadcn компонентов
SHADCN_CODE_TEMPLATES = {
    "button": {
        "tsx": '''import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }''',
        "dependencies": ["@radix-ui/react-slot", "class-variance-authority", "clsx", "tailwind-merge"],
        "description": "A button component with multiple variants and sizes."
    },
    
    "input": {
        "tsx": '''import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
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

export { Input }''',
        "dependencies": ["clsx", "tailwind-merge"],
        "description": "A styled input component."
    },
    
    "card": {
        "tsx": '''import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRight<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }''',
        "dependencies": ["clsx", "tailwind-merge"],
        "description": "A card component with header, content, and footer."
    },
    
    "badge": {
        "tsx": '''import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }''',
        "dependencies": ["class-variance-authority", "clsx", "tailwind-merge"],
        "description": "A badge component for status indicators."
    },
    
    "avatar": {
        "tsx": '''import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"
import { cn } from "@/lib/utils"

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn(
      "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full",
      className
    )}
    {...props}
  />
))
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props}
  />
))
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-muted",
      className
    )}
    {...props}
  />
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }''',
        "dependencies": ["@radix-ui/react-avatar", "clsx", "tailwind-merge"],
        "description": "An avatar component for user profile pictures."
    }
}


@register_provider  
class EnhancedShadcnUIProvider(GitHubProvider):
    """Enhanced shadcn/ui component provider with proper code templates."""
    
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
        """List shadcn/ui components with enhanced code support."""
        components = []
        
        # Generate components from our templates
        for slug, template in SHADCN_CODE_TEMPLATES.items():
            component_data = {
                "name": slug.replace("-", " ").title(),
                "slug": slug,
                "category": self._infer_category_from_name(slug)
            }
            manifest = await self._create_enhanced_manifest(component_data, template)
            if manifest:
                components.append(manifest)
        
        # Add additional components from registry if available
        try:
            registry_components = await self._get_registry_components()
            for comp_data in registry_components:
                if comp_data["slug"] not in SHADCN_CODE_TEMPLATES:
                    manifest = await self._create_basic_manifest(comp_data)
                    if manifest:
                        components.append(manifest)
        except Exception:
            pass  # Fallback gracefully
        
        # Apply pagination
        start = offset
        end = offset + limit
        return components[start:end]

    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific shadcn/ui component with enhanced code."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        # Check if we have a template for this component
        if component_id in SHADCN_CODE_TEMPLATES:
            template = SHADCN_CODE_TEMPLATES[component_id]
            component_data = {
                "name": component_id.replace("-", " ").title(),
                "slug": component_id,
                "category": self._infer_category_from_name(component_id)
            }
            return await self._create_enhanced_manifest(component_data, template)
        
        # Fallback to existing implementation
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in shadcn/ui")

    async def _create_enhanced_manifest(
        self, 
        component_data: Dict[str, Any], 
        template: Dict[str, Any]
    ) -> ComponentManifest:
        """Create enhanced manifest with proper code template."""
        slug = component_data.get("slug", "")
        
        return ComponentManifest(
            id=f"shadcn/{slug}",
            provider=self.provider_name,
            name=component_data.get("name", slug.replace("-", " ").title()),
            slug=slug,
            category=ComponentCategory(component_data.get("category", "other")),
            tags=["shadcn", "react", "tailwind", "radix", "typescript"],
            license=License(
                type=LicenseType.MIT,
                url="https://github.com/shadcn-ui/ui/blob/main/LICENSE.md",
                redistribute=True,
                commercial=True
            ),
            source=Source(
                url="https://github.com/shadcn-ui/ui",
                commit=None,
                branch="main"
            ),
            framework=Framework(
                react=True,
                vue=False,
                angular=False,
                svelte=False,
                solid=False,
                next=True,
                nuxt=False,
                html=False
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,
                plugin_deps=["tailwindcss-animate"],
                required_classes=[],
                custom_css=None
            ),
            runtime_deps=template.get("dependencies", []),
            peer_deps=["react", "react-dom"],
            dev_deps=["typescript", "@types/react", "@types/react-dom"],
            install=InstallPlan(
                npm=template.get("dependencies", []),
                yarn=[],
                pnpm=[],
                bun=[],
                steps=[
                    {
                        "type": "cli",
                        "command": f"npx shadcn@latest add {slug}",
                        "description": f"Install {component_data.get('name', slug)} component via shadcn CLI"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=template.get("tsx"),
                jsx=template.get("tsx"),  # Use TSX for JSX as well
                vue=None,
                svelte=None,
                angular=None,
                html=None,
                css=None,
                js=None,
                ts=None
            ),
            access=ComponentAccess(
                copy_paste=True,
                cli=f"npx shadcn@latest add {slug}",
                npm=None,
                cdn=None,
                free=True,
                pro=False
            ),
            description=template.get("description", f"A {slug} component from shadcn/ui."),
            documentation_url=f"https://ui.shadcn.com/docs/components/{slug}",
            demo_url=f"https://ui.shadcn.com/docs/components/{slug}",
            playground_url=None,
            keywords=["shadcn", slug, "react", "component", "tailwind"],
            author="shadcn",
            version="latest",
            created_at=None,
            updated_at=datetime.now(),
            downloads=None,
            stars=None,
            forks=None,
            popularity_score=10.0  # High popularity for shadcn components
        )

    async def _create_basic_manifest(self, component_data: Dict[str, Any]) -> ComponentManifest:
        """Create basic manifest for components without templates."""
        slug = component_data.get("slug", "")
        
        return ComponentManifest(
            id=f"shadcn/{slug}",
            provider=self.provider_name,
            name=component_data.get("name", slug.replace("-", " ").title()),
            slug=slug,
            category=ComponentCategory(component_data.get("category", "other")),
            tags=["shadcn", "react", "tailwind"],
            license=License(
                type=LicenseType.MIT,
                url="https://github.com/shadcn-ui/ui/blob/main/LICENSE.md",
                redistribute=True,
                commercial=True
            ),
            source=Source(
                url="https://github.com/shadcn-ui/ui",
                commit=None,
                branch="main"
            ),
            framework=Framework(
                react=True,
                vue=False,
                angular=False,
                svelte=False,
                solid=False,
                next=True,
                nuxt=False,
                html=False
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,
                plugin_deps=["tailwindcss-animate"],
                required_classes=[],
                custom_css=None
            ),
            runtime_deps=["clsx", "tailwind-merge"],
            peer_deps=["react", "react-dom"],
            dev_deps=[],
            install=InstallPlan(
                npm=["clsx", "tailwind-merge"],
                yarn=[],
                pnpm=[],
                bun=[],
                steps=[
                    {
                        "type": "cli", 
                        "command": f"npx shadcn@latest add {slug}",
                        "description": f"Install {component_data.get('name', slug)} component via shadcn CLI"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=None,  # No template available
                jsx=None,
                vue=None,
                svelte=None,
                angular=None,
                html=None,
                css=None,
                js=None,
                ts=None
            ),
            access=ComponentAccess(
                copy_paste=True,
                cli=f"npx shadcn@latest add {slug}",
                npm=None,
                cdn=None,
                free=True,
                pro=False
            ),
            description=f"A {slug} component from shadcn/ui.",
            documentation_url=f"https://ui.shadcn.com/docs/components/{slug}",
            demo_url=f"https://ui.shadcn.com/docs/components/{slug}",
            playground_url=None,
            keywords=["shadcn", slug, "react", "component"],
            author="shadcn",
            version="latest",
            created_at=None,
            updated_at=datetime.now(),
            downloads=None,
            stars=None,
            forks=None,
            popularity_score=8.0
        )

    def _infer_category_from_name(self, name: str) -> str:
        """Infer component category from name."""
        name_lower = name.lower()
        
        if any(word in name_lower for word in ["button", "btn"]):
            return "buttons"
        elif any(word in name_lower for word in ["input", "form", "field", "select", "textarea"]):
            return "forms"
        elif any(word in name_lower for word in ["card", "dialog", "modal", "sheet", "popover"]):
            return "overlays"
        elif any(word in name_lower for word in ["nav", "menu", "breadcrumb", "tabs"]):
            return "navigation"
        elif any(word in name_lower for word in ["table", "badge", "avatar", "progress"]):
            return "data_display"
        elif any(word in name_lower for word in ["alert", "toast", "notification"]):
            return "feedback"
        else:
            return "other"

    async def _get_registry_components(self) -> List[Dict[str, Any]]:
        """Get additional components from registry (fallback)."""
        # This would normally fetch from the actual registry
        # For now, return empty list to avoid errors
        return []