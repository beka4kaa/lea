"""Aceternity UI provider implementation."""

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
class AceternityProvider(HTTPProvider):
    """Aceternity UI component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.ACETERNITY
    
    @property
    def base_url(self) -> str:
        return "https://ui.aceternity.com"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List Aceternity UI components."""
        try:
            components = await self._get_all_components()
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            print(f"Error listing Aceternity components: {e}")
            return []
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific Aceternity component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in Aceternity UI")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all Aceternity UI components."""
        # Aceternity UI component catalog (Free + Pro)
        aceternity_components = {
            # Free Components
            "free": [
                {
                    "name": "3D Card Effect",
                    "slug": "3d-card-effect",
                    "category": "layouts",
                    "description": "Interactive 3D card with tilt and hover effects",
                    "tags": ["3d", "card", "interactive", "hover", "tilt"],
                    "runtime_deps": ["framer-motion", "clsx"],
                    "pro": False
                },
                {
                    "name": "Animated Tooltip",
                    "slug": "animated-tooltip",
                    "category": "overlays",
                    "description": "Smooth animated tooltip with multiple positions",
                    "tags": ["tooltip", "animated", "overlay", "position"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Aurora Background",
                    "slug": "aurora-background",
                    "category": "backgrounds",
                    "description": "Beautiful aurora-style animated background",
                    "tags": ["background", "aurora", "animated", "gradient"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Background Beams",
                    "slug": "background-beams",
                    "category": "backgrounds",
                    "description": "Animated light beams background effect",
                    "tags": ["background", "beams", "light", "animated"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Bento Grid",
                    "slug": "bento-grid",
                    "category": "layouts",
                    "description": "Modern bento-style grid layout",
                    "tags": ["bento", "grid", "layout", "responsive"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Border Beam",
                    "slug": "border-beam",
                    "category": "other",
                    "description": "Animated border with beam effect",
                    "tags": ["border", "beam", "animated", "effect"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Card Hover Effect",
                    "slug": "card-hover-effect",
                    "category": "layouts",
                    "description": "Smooth card hover animations and effects",
                    "tags": ["card", "hover", "animation", "effect"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Compare",
                    "slug": "compare",
                    "category": "other",
                    "description": "Before/after image comparison slider",
                    "tags": ["compare", "slider", "before", "after", "image"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Container Scroll Animation",
                    "slug": "container-scroll-animation",
                    "category": "animated",
                    "description": "Scroll-triggered container animations",
                    "tags": ["scroll", "animation", "container", "trigger"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Direction Aware Hover",
                    "slug": "direction-aware-hover",
                    "category": "other",
                    "description": "Hover effect that detects entry direction",
                    "tags": ["hover", "direction", "aware", "effect"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Evervault Card",
                    "slug": "evervault-card",
                    "category": "layouts",
                    "description": "Evervault-inspired encrypted card effect",
                    "tags": ["evervault", "card", "encrypted", "effect"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Focus Cards",
                    "slug": "focus-cards",
                    "category": "layouts",
                    "description": "Cards that focus on hover with blur effect",
                    "tags": ["focus", "cards", "hover", "blur"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Following Pointer",
                    "slug": "following-pointer",
                    "category": "other",
                    "description": "Element that smoothly follows the pointer",
                    "tags": ["pointer", "follow", "cursor", "smooth"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Globe",
                    "slug": "globe",
                    "category": "other",
                    "description": "Interactive 3D globe component",
                    "tags": ["globe", "3d", "interactive", "world"],
                    "runtime_deps": ["three", "@react-three/fiber"],
                    "pro": False
                },
                {
                    "name": "Google Gemini Effect",
                    "slug": "google-gemini-effect",
                    "category": "animated",
                    "description": "Google Gemini-inspired loading effect",
                    "tags": ["google", "gemini", "loading", "effect"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Hero Parallax",
                    "slug": "hero-parallax",
                    "category": "layouts",
                    "description": "Parallax hero section with smooth scrolling",
                    "tags": ["hero", "parallax", "scroll", "section"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Highlight",
                    "slug": "highlight",
                    "category": "text",
                    "description": "Animated text highlighting effect",
                    "tags": ["highlight", "text", "animated", "marker"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Hover Border Gradient",
                    "slug": "hover-border-gradient",
                    "category": "other",
                    "description": "Gradient border that animates on hover",
                    "tags": ["hover", "border", "gradient", "animated"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Infinite Moving Cards",
                    "slug": "infinite-moving-cards",
                    "category": "layouts",
                    "description": "Infinitely scrolling card carousel",
                    "tags": ["infinite", "moving", "cards", "carousel"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Lamp Effect",
                    "slug": "lamp-effect",
                    "category": "other",
                    "description": "Dramatic lamp lighting effect",
                    "tags": ["lamp", "lighting", "effect", "dramatic"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "MacBook Scroll",
                    "slug": "macbook-scroll",
                    "category": "other",
                    "description": "MacBook-style scroll animation",
                    "tags": ["macbook", "scroll", "animation", "apple"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Meteors",
                    "slug": "meteors",
                    "category": "backgrounds",
                    "description": "Animated meteor shower background",
                    "tags": ["meteors", "background", "animated", "space"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Moving Border",
                    "slug": "moving-border",
                    "category": "other",
                    "description": "Animated moving border effect",
                    "tags": ["moving", "border", "animated", "effect"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Multi Step Loader",
                    "slug": "multi-step-loader",
                    "category": "other",
                    "description": "Multi-step loading animation",
                    "tags": ["loader", "multi-step", "loading", "progress"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Parallax Scroll",
                    "slug": "parallax-scroll",
                    "category": "other",
                    "description": "Smooth parallax scrolling effect",
                    "tags": ["parallax", "scroll", "smooth", "effect"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Placeholders and Vanish Input",
                    "slug": "placeholders-and-vanish-input",
                    "category": "forms",
                    "description": "Input with vanishing placeholder effect",
                    "tags": ["input", "placeholder", "vanish", "form"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Sparkles",
                    "slug": "sparkles",
                    "category": "other",
                    "description": "Animated sparkle effects",
                    "tags": ["sparkles", "animated", "effect", "magical"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Sticky Scroll Reveal",
                    "slug": "sticky-scroll-reveal",
                    "category": "other",
                    "description": "Sticky scroll with content reveal",
                    "tags": ["sticky", "scroll", "reveal", "content"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Text Generate Effect",
                    "slug": "text-generate-effect",
                    "category": "text",
                    "description": "AI-style text generation effect",
                    "tags": ["text", "generate", "ai", "typewriter"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Text Reveal Card",
                    "slug": "text-reveal-card",
                    "category": "layouts",
                    "description": "Card with text reveal on hover",
                    "tags": ["text", "reveal", "card", "hover"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Tracing Beam",
                    "slug": "tracing-beam",
                    "category": "other",
                    "description": "Animated tracing beam effect",
                    "tags": ["tracing", "beam", "animated", "line"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                },
                {
                    "name": "Typewriter Effect",
                    "slug": "typewriter-effect",
                    "category": "text",
                    "description": "Classic typewriter text animation",
                    "tags": ["typewriter", "text", "animation", "typing"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Vortex",
                    "slug": "vortex",
                    "category": "backgrounds",
                    "description": "Swirling vortex background effect",
                    "tags": ["vortex", "background", "swirl", "animated"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Wavy Background",
                    "slug": "wavy-background",
                    "category": "backgrounds",
                    "description": "Animated wavy background pattern",
                    "tags": ["wavy", "background", "animated", "wave"],
                    "runtime_deps": [],
                    "pro": False
                },
                {
                    "name": "Wobble Card",
                    "slug": "wobble-card",
                    "category": "layouts",
                    "description": "Card with wobble animation effect",
                    "tags": ["wobble", "card", "animation", "effect"],
                    "runtime_deps": ["framer-motion"],
                    "pro": False
                }
            ],
            
            # Pro Components (metadata only)
            "pro": [
                {
                    "name": "Advanced Data Table",
                    "slug": "advanced-data-table",
                    "category": "layouts",
                    "description": "Feature-rich data table with sorting, filtering, and pagination",
                    "tags": ["table", "data", "advanced", "pro"],
                    "runtime_deps": ["@tanstack/react-table"],
                    "pro": True
                },
                {
                    "name": "File Upload Dropzone",
                    "slug": "file-upload-dropzone",
                    "category": "forms",
                    "description": "Advanced file upload with drag & drop and progress",
                    "tags": ["upload", "file", "dropzone", "pro"],
                    "runtime_deps": ["react-dropzone"],
                    "pro": True
                },
                {
                    "name": "Timeline Component",
                    "slug": "timeline-component",
                    "category": "layouts",
                    "description": "Interactive timeline with animations",
                    "tags": ["timeline", "animation", "interactive", "pro"],
                    "runtime_deps": ["framer-motion"],
                    "pro": True
                },
                {
                    "name": "Chart Components",
                    "slug": "chart-components",
                    "category": "layouts",
                    "description": "Beautiful animated charts and graphs",
                    "tags": ["charts", "graphs", "data", "pro"],
                    "runtime_deps": ["recharts", "framer-motion"],
                    "pro": True
                },
                {
                    "name": "Calendar Component",
                    "slug": "calendar-component",
                    "category": "forms",
                    "description": "Full-featured calendar with events",
                    "tags": ["calendar", "events", "date", "pro"],
                    "runtime_deps": ["date-fns"],
                    "pro": True
                }
            ]
        }
        
        components = []
        
        # Process free components
        for comp_data in aceternity_components["free"]:
            manifest = self._create_manifest_from_data(comp_data, is_pro=False)
            components.append(manifest)
        
        # Process pro components (metadata only)
        for comp_data in aceternity_components["pro"]:
            manifest = self._create_manifest_from_data(comp_data, is_pro=True)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any], is_pro: bool = False) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        # Generate sample code only for free components
        sample_code = None if is_pro else self._generate_sample_code(comp_data)
        
        return ComponentManifest(
            id=f"aceternity/{slug}",
            provider=Provider.ACETERNITY,
            name=name,
            slug=slug,
            category=ComponentCategory(category),
            tags=comp_data["tags"],
            license=License(
                type=LicenseType.CUSTOM if is_pro else LicenseType.MIT,
                url="https://ui.aceternity.com/license" if is_pro else "https://ui.aceternity.com/license",
                notes="Pro components require Aceternity UI Pro license" if is_pro else "Free components under MIT license",
                redistribute=not is_pro,
                commercial=True
            ),
            source=Source(
                url="https://ui.aceternity.com",
                branch=None
            ),
            framework=Framework(
                react=True,
                next=True,
                vue=False,  # React-specific
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
                        "type": "info",
                        "description": f"{'Pro component - requires Aceternity UI Pro license' if is_pro else 'Free Aceternity UI component'}"
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
            documentation_url=f"https://ui.aceternity.com/components/{slug}",
            demo_url=f"https://ui.aceternity.com/components/{slug}",
            keywords=comp_data["tags"] + ["aceternity", "ui", "modern"]
        )
    
    def _generate_sample_code(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample code for free components."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        
        # Component-specific code templates
        if "3d-card" in slug:
            return '''import { CardBody, CardContainer, CardItem } from "./3d-card";

export function ThreeDCardDemo() {
  return (
    <CardContainer className="inter-var">
      <CardBody className="bg-gray-50 relative group/card dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border">
        <CardItem
          translateZ="50"
          className="text-xl font-bold text-neutral-600 dark:text-white"
        >
          Make things float in air
        </CardItem>
        <CardItem
          as="p"
          translateZ="60"
          className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
        >
          Hover over this card to unleash the power of CSS 3D transforms
        </CardItem>
        <CardItem translateZ="100" className="w-full mt-4">
          <img
            src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2560&auto=format&fit=crop&ixlib=rb-4.0.3"
            height="1000"
            width="1000"
            className="h-60 w-full object-cover rounded-xl group-hover/card:shadow-xl"
            alt="thumbnail"
          />
        </CardItem>
      </CardBody>
    </CardContainer>
  );
}'''
        
        elif "aurora" in slug:
            return '''export function AuroraBackground({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative flex flex-col h-[40rem] items-center justify-center bg-white dark:bg-black text-white transition-bg">
      <div className="absolute inset-0 overflow-hidden">
        <div className="aurora-bg absolute inset-0 opacity-50" />
      </div>
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}'''
        
        elif "bento" in slug:
            return '''const items = [
  {
    title: "The Dawn of Innovation",
    description: "Explore the birth of groundbreaking ideas and inventions.",
    header: <Skeleton />,
    className: "md:col-span-2",
    icon: <IconClipboardCopy className="h-4 w-4 text-neutral-500" />,
  },
  // ... more items
];

export function BentoGridDemo() {
  return (
    <BentoGrid className="max-w-4xl mx-auto">
      {items.map((item, i) => (
        <BentoGridItem
          key={i}
          title={item.title}
          description={item.description}
          header={item.header}
          className={item.className}
          icon={item.icon}
        />
      ))}
    </BentoGrid>
  );
}'''
        
        elif "typewriter" in slug:
            return '''import { TypewriterEffect } from "./typewriter-effect";

export function TypewriterEffectDemo() {
  const words = [
    {
      text: "Build",
    },
    {
      text: "awesome",
    },
    {
      text: "apps",
    },
    {
      text: "with",
    },
    {
      text: "Aceternity.",
      className: "text-blue-500 dark:text-blue-500",
    },
  ];
  
  return (
    <div className="flex flex-col items-center justify-center h-[40rem]">
      <p className="text-neutral-600 dark:text-neutral-200 text-xs sm:text-base">
        The road to freedom starts from here
      </p>
      <TypewriterEffect words={words} />
    </div>
  );
}'''
        
        else:
            # Generic template
            component_name = name.replace(" ", "").replace("-", "")
            return f'''interface {component_name}Props {{
  children?: React.ReactNode;
  className?: string;
}}

export function {component_name}({{ children, className = "" }}: {component_name}Props) {{
  return (
    <div className={{`aceternity-component ${{className}}`}}>
      {{children || "{name}"}}
    </div>
  );
}}'''