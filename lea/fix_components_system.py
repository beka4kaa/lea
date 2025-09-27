#!/usr/bin/env python3
"""
Улучшение системы компонентов MCP UI Aggregator
Исправляет проблемы с кодом, документацией и зависимостями
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

# Шаблоны кода для компонентов без кода
COMPONENT_CODE_TEMPLATES = {
    # Shadcn компоненты
    "shadcn/button": {
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
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
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
    
    "shadcn/input": {
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
    
    "shadcn/card": {
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

const CardFooter = React.forwardRef<
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

    # MagicUI компоненты
    "magicui/magic-button": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface MagicButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
}

export default function MagicButton({
  children,
  className,
  ...props
}: MagicButtonProps) {
  return (
    <motion.button
      className={cn(
        "relative inline-flex h-12 overflow-hidden rounded-full p-[1px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50",
        className
      )}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      {...props}
    >
      <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
      <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-950 px-3 py-1 text-sm font-medium text-white backdrop-blur-3xl">
        {children}
      </span>
    </motion.button>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "A magical button with animated gradient border."
    },

    "magicui/rainbow-button": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface RainbowButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
}

export default function RainbowButton({
  children,
  className,
  ...props
}: RainbowButtonProps) {
  return (
    <motion.button
      className={cn(
        "group relative inline-flex h-11 items-center justify-center overflow-hidden rounded-md bg-neutral-950 px-6 font-medium text-neutral-200 transition hover:scale-110",
        className
      )}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      {...props}
    >
      <span className="absolute inset-0 overflow-hidden rounded-md">
        <span className="absolute inset-0 rounded-md bg-gradient-to-r from-red-500 via-purple-500 to-blue-500 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
      </span>
      <span className="relative z-10">{children}</span>
    </motion.button>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "A button with rainbow gradient hover effect."
    },

    "magicui/marquee": {
        "tsx": '''import { cn } from "@/lib/utils";

interface MarqueeProps {
  className?: string;
  reverse?: boolean;
  pauseOnHover?: boolean;
  children?: React.ReactNode;
  vertical?: boolean;
  repeat?: number;
}

export default function Marquee({
  className,
  reverse,
  pauseOnHover = false,
  children,
  vertical = false,
  repeat = 4,
  ...props
}: MarqueeProps) {
  return (
    <div
      {...props}
      className={cn(
        "group flex overflow-hidden p-2 [--duration:20s] [--gap:1rem] [gap:var(--gap)]",
        {
          "flex-row": !vertical,
          "flex-col": vertical,
        },
        className,
      )}
    >
      {Array(repeat)
        .fill(0)
        .map((_, i) => (
          <div
            key={i}
            className={cn("flex shrink-0 justify-around [gap:var(--gap)]", {
              "animate-marquee flex-row": !vertical,
              "animate-marquee-vertical flex-col": vertical,
              "group-hover:[animation-play-state:paused]": pauseOnHover,
              "[animation-direction:reverse]": reverse,
            })}
          >
            {children}
          </div>
        ))}
    </div>
  );
}''',
        "dependencies": ["clsx", "tailwind-merge"],
        "description": "A marquee component for scrolling content."
    }
}

# Улучшенная документация для компонентов
ENHANCED_DOCUMENTATION = {
    "shadcn/button": {
        "installation": [
            "npx shadcn@latest add button",
            "npm install @radix-ui/react-slot class-variance-authority clsx tailwind-merge"
        ],
        "usage": '''import { Button } from "@/components/ui/button"

export default function ButtonDemo() {
  return (
    <div className="flex gap-2">
      <Button>Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  )
}''',
        "examples": [
            "Basic button usage",
            "Button variants",
            "Button sizes",
            "Button with icons",
            "Loading button state"
        ]
    },
    
    "magicui/magic-button": {
        "installation": [
            "npm install framer-motion clsx tailwind-merge"
        ],
        "usage": '''import MagicButton from "@/components/ui/magic-button"

export default function MagicButtonDemo() {
  return (
    <div className="flex gap-4">
      <MagicButton onClick={() => console.log("Magic!")}>
        ✨ Magic Button
      </MagicButton>
    </div>
  )
}''',
        "examples": [
            "Basic magic button",
            "Custom colors",
            "Different sizes",
            "With icons"
        ]
    }
}

def patch_providers_with_code():
    """Патчит провайдеров для добавления кода компонентов"""
    print("🔧 Применяем патчи для улучшения кода компонентов...")
    
    # Патч для Shadcn провайдера
    shadcn_patch = '''
    async def _create_manifest_from_registry(self, component_data: Dict[str, Any]) -> Optional[ComponentManifest]:
        """Enhanced manifest creation with proper code handling."""
        slug = component_data.get("slug", "")
        component_id = f"shadcn/{slug}"
        
        # Check if we have template code for this component
        template_code = None
        dependencies = []
        if component_id in COMPONENT_CODE_TEMPLATES:
            template = COMPONENT_CODE_TEMPLATES[component_id]
            template_code = template.get("tsx")
            dependencies = template.get("dependencies", [])
        
        return ComponentManifest(
            id=component_id,
            provider=self.provider_name,
            name=component_data.get("name", slug.replace("-", " ").title()),
            slug=slug,
            category=ComponentCategory(component_data.get("category", "other")),
            tags=["shadcn", "react", "tailwind", "radix"],
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
            runtime_deps=dependencies,
            peer_deps=[],
            dev_deps=[],
            install=InstallPlan(
                npm=dependencies,
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
                tsx=template_code,
                jsx=template_code,
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
            description=COMPONENT_CODE_TEMPLATES.get(component_id, {}).get("description", f"Displays a {slug} component."),
            documentation_url=f"https://ui.shadcn.com/docs/components/{slug}",
            demo_url=f"https://ui.shadcn.com/docs/components/{slug}",
            playground_url=None,
            keywords=["shadcn", slug, "react", "component"],
            author=None,
            version=None,
            created_at=None,
            updated_at=None,
            downloads=None,
            stars=None,
            forks=None,
            popularity_score=0.0
        )
'''
    
    return {
        "shadcn_patch": shadcn_patch,
        "templates_added": len(COMPONENT_CODE_TEMPLATES),
        "documentation_enhanced": len(ENHANCED_DOCUMENTATION)
    }

async def test_improvements():
    """Тестирует улучшения"""
    print("🧪 Тестируем улучшения...")
    
    import httpx
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Тест компонентов с кодом
        test_components = [
            "shadcn/button",
            "daisyui/btn", 
            "magicui/magic-button",
            "alignui/button"
        ]
        
        results = {}
        for comp_id in test_components:
            provider, component = comp_id.split("/")
            try:
                response = await client.get(f"{base_url}/api/v1/components/{provider}/{component}/code")
                results[comp_id] = {
                    "status": response.status_code,
                    "has_code": response.status_code == 200,
                    "error": response.text if response.status_code != 200 else None
                }
            except Exception as e:
                results[comp_id] = {
                    "status": "error",
                    "has_code": False,
                    "error": str(e)
                }
        
        return results

if __name__ == "__main__":
    print("🚀 Запуск улучшения системы компонентов...")
    
    # Применяем патчи
    patches = patch_providers_with_code()
    print(f"✅ Применено патчей: {patches}")
    
    print("📋 Для полного исправления необходимо:")
    print("1. Обновить код провайдеров с новыми шаблонами")
    print("2. Перезапустить сервер")
    print("3. Протестировать компоненты")
    print("4. Обновить документацию")