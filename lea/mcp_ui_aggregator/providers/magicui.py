"""Magic UI provider implementation with enhanced code templates."""

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

# Enhanced code templates for Magic UI components
MAGICUI_CODE_TEMPLATES = {
    "magic-button": {
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
        "description": "A magical button with animated gradient border and hover effects."
    },
    
    "rainbow-button": {
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
        "description": "A button with rainbow gradient hover effect and smooth animations."
    },
    
    "marquee": {
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
        "description": "A marquee component for scrolling content horizontally or vertically."
    },
    
    "sparkles": {
        "tsx": '''import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SparklesProps {
  children: React.ReactNode;
  className?: string;
  color?: string;
  size?: number;
}

export default function Sparkles({
  children,
  className,
  color = "rgba(255, 255, 255, 0.8)",
  size = 16,
}: SparklesProps) {
  const sparkles = Array.from({ length: 3 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    scale: Math.random() * 0.5 + 0.5,
  }));

  return (
    <span className={cn("relative inline-block", className)}>
      {sparkles.map((sparkle) => (
        <motion.div
          key={sparkle.id}
          className="pointer-events-none absolute"
          style={{
            left: `${sparkle.x}%`,
            top: `${sparkle.y}%`,
            transform: "translate(-50%, -50%)",
          }}
          animate={{
            scale: [0, sparkle.scale, 0],
            rotate: [0, 360],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            delay: sparkle.id * 0.5,
          }}
        >
          <div
            style={{
              width: size,
              height: size,
              backgroundColor: color,
            }}
            className="rounded-full"
          />
        </motion.div>
      ))}
      {children}
    </span>
  );
}''',
        "dependencies": ["framer-motion", "clsx", "tailwind-merge"],
        "description": "Add magical sparkle effects to any component."
    }
}


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
        """Create component manifest from registry data with enhanced code templates."""
        try:
            name = component_data.get("name", "")
            slug = component_data.get("slug", name.lower().replace(" ", "-"))
            
            # Check if we have a template for this component
            template = MAGICUI_CODE_TEMPLATES.get(slug)
            code_content = ""
            runtime_deps = []
            
            if template:
                # Use our enhanced template
                code_content = template.get("tsx", "")
                runtime_deps = template.get("dependencies", [])
            else:
                # Try to get code from registry
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
                
                # Extract dependencies from code if no template
                if not runtime_deps:
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
                code=ComponentCode(
                    tsx=MAGICUI_CODE_TEMPLATES.get(comp_data['slug'], {}).get('tsx')
                ),
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