"""React Bits provider implementation."""

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


@register_provider
class ReactBitsProvider(GitHubProvider):
    """React Bits component provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.REACTBITS
    
    @property
    def base_url(self) -> str:
        return "https://react-bits.dev"
    
    @property
    def github_repo(self) -> str:
        return "DavidHDev/react-bits"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List React Bits components."""
        try:
            # Get components from hardcoded list since it's a curated collection
            components = await self._get_all_components()
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            print(f"Error listing React Bits components: {e}")
            return []
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific React Bits component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in React Bits")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all React Bits components."""
        # React Bits curated components
        react_bits_components = [
            # Animations
            {
                "name": "Typewriter Effect",
                "slug": "typewriter-effect",
                "category": "animated",
                "description": "A smooth typewriter effect component with customizable speed and cursor",
                "tags": ["animation", "typewriter", "text", "effect"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Fade In",
                "slug": "fade-in",
                "category": "animated",
                "description": "Smooth fade-in animation component with intersection observer",
                "tags": ["animation", "fade", "intersection", "scroll"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Slide In",
                "slug": "slide-in",
                "category": "animated",
                "description": "Slide-in animation from different directions",
                "tags": ["animation", "slide", "direction", "entrance"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Stagger Animation",
                "slug": "stagger-animation",
                "category": "animated",
                "description": "Staggered animations for lists and grids",
                "tags": ["animation", "stagger", "list", "grid"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Morphing Button",
                "slug": "morphing-button",
                "category": "buttons",
                "description": "Button that morphs between different states",
                "tags": ["button", "morph", "state", "transition"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Ripple Effect",
                "slug": "ripple-effect",
                "category": "animated",
                "description": "Material Design ripple effect component",
                "tags": ["ripple", "material", "effect", "click"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            
            # Backgrounds
            {
                "name": "Animated Background",
                "slug": "animated-background",
                "category": "backgrounds",
                "description": "Customizable animated background with particles",
                "tags": ["background", "animated", "particles", "canvas"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Gradient Background",
                "slug": "gradient-background",
                "category": "backgrounds",
                "description": "Animated gradient background with smooth transitions",
                "tags": ["background", "gradient", "animated", "css"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Grid Background",
                "slug": "grid-background",
                "category": "backgrounds",
                "description": "Animated grid background pattern",
                "tags": ["background", "grid", "pattern", "animated"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Floating Shapes",
                "slug": "floating-shapes",
                "category": "backgrounds",
                "description": "Floating geometric shapes background",
                "tags": ["background", "shapes", "floating", "geometric"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            
            # Interactive Components
            {
                "name": "Magnetic Card",
                "slug": "magnetic-card",
                "category": "layouts",
                "description": "Card component with magnetic hover effect",
                "tags": ["card", "magnetic", "hover", "interactive"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Tilt Card",
                "slug": "tilt-card",
                "category": "layouts",
                "description": "3D tilt effect card on mouse move",
                "tags": ["card", "tilt", "3d", "mouse"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Flip Card",
                "slug": "flip-card",
                "category": "layouts",
                "description": "Card that flips to reveal back content",
                "tags": ["card", "flip", "reveal", "3d"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Parallax Card",
                "slug": "parallax-card",
                "category": "layouts",
                "description": "Card with parallax scrolling effect",
                "tags": ["card", "parallax", "scroll", "effect"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            
            # Text Effects
            {
                "name": "Glitch Text",
                "slug": "glitch-text",
                "category": "text",
                "description": "Glitch effect text animation",
                "tags": ["text", "glitch", "effect", "animation"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Neon Text",
                "slug": "neon-text",
                "category": "text",
                "description": "Neon glow text effect with CSS",
                "tags": ["text", "neon", "glow", "css"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Scramble Text",
                "slug": "scramble-text",
                "category": "text",
                "description": "Text that scrambles and reveals letter by letter",
                "tags": ["text", "scramble", "reveal", "animation"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Wave Text",
                "slug": "wave-text",
                "category": "text",
                "description": "Text with wave animation effect",
                "tags": ["text", "wave", "animation", "letters"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            
            # Interactive Elements
            {
                "name": "Cursor Follow",
                "slug": "cursor-follow",
                "category": "other",
                "description": "Element that follows the cursor with smooth animation",
                "tags": ["cursor", "follow", "mouse", "animation"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Magnetic Button",
                "slug": "magnetic-button",
                "category": "buttons",
                "description": "Button with magnetic attraction to cursor",
                "tags": ["button", "magnetic", "cursor", "attraction"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Spotlight Card",
                "slug": "spotlight-card",
                "category": "layouts",
                "description": "Card with spotlight effect following cursor",
                "tags": ["card", "spotlight", "cursor", "effect"],
                "runtime_deps": [],
                "code_type": "tsx"
            },
            {
                "name": "Hover Reveal",
                "slug": "hover-reveal",
                "category": "other",
                "description": "Reveal content on hover with smooth transition",
                "tags": ["hover", "reveal", "transition", "content"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            
            # Navigation
            {
                "name": "Animated Menu",
                "slug": "animated-menu",
                "category": "navigation",
                "description": "Hamburger menu with smooth animations",
                "tags": ["menu", "hamburger", "animated", "navigation"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Tab Switcher",
                "slug": "tab-switcher",
                "category": "navigation",
                "description": "Animated tab switcher with smooth transitions",
                "tags": ["tabs", "switcher", "animated", "navigation"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "Dock Navigation",
                "slug": "dock-navigation",
                "category": "navigation",
                "description": "macOS-style dock navigation with magnification",
                "tags": ["dock", "navigation", "macos", "magnification"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            
            # Form Components
            {
                "name": "Animated Input",
                "slug": "animated-input",
                "category": "forms",
                "description": "Input field with smooth label animations",
                "tags": ["input", "animated", "label", "form"],
                "runtime_deps": ["framer-motion"],
                "code_type": "tsx"
            },
            {
                "name": "OTP Input",
                "slug": "otp-input",
                "category": "forms",
                "description": "One-time password input with auto-focus",
                "tags": ["otp", "input", "password", "verification"],
                "runtime_deps": [],
                "code_type": "tsx"
            }
        ]
        
        components = []
        for comp_data in react_bits_components:
            manifest = self._create_manifest_from_data(comp_data)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any]) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        # Generate sample code
        sample_code = self._generate_sample_code(comp_data)
        
        return ComponentManifest(
            id=f"reactbits/{slug}",
            provider=Provider.REACTBITS,
            name=name,
            slug=slug,
            category=ComponentCategory(category),
            tags=comp_data["tags"],
            license=License(
                type=LicenseType.MIT_COMMONS_CLAUSE,
                url="https://github.com/DavidHDev/react-bits/blob/main/LICENSE",
                notes="MIT + Commons Clause - commercial use allowed but resale prohibited",
                redistribute=True,
                commercial=False  # Commons Clause restriction
            ),
            source=Source(
                url=f"https://github.com/DavidHDev/react-bits",
                branch="main"
            ),
            framework=Framework(
                react=True,
                next=True,
                vue=False,  # React-specific components
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
                        "type": "warning",
                        "description": "React Bits uses MIT + Commons Clause license - commercial use allowed but resale prohibited"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=sample_code if comp_data.get("code_type") == "tsx" else None
            ),
            access=ComponentAccess(
                copy_paste=True,
                pro=False
            ),
            description=comp_data["description"],
            documentation_url=f"https://react-bits.dev/components/{slug}",
            demo_url=f"https://react-bits.dev/components/{slug}",
            keywords=comp_data["tags"] + ["react-bits", "animation", "interactive"]
        )
    
    def _generate_sample_code(self, comp_data: Dict[str, Any]) -> str:
        """Generate sample code for component."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        
        # Component-specific code templates
        if "typewriter" in slug:
            return '''import { useState, useEffect } from 'react';

interface TypewriterProps {
  text: string;
  speed?: number;
}

export function TypewriterEffect({ text, speed = 100 }: TypewriterProps) {
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);

      return () => clearTimeout(timeout);
    }
  }, [currentIndex, text, speed]);

  return (
    <span className="font-mono">
      {displayText}
      <span className="animate-pulse">|</span>
    </span>
  );
}'''
        
        elif "fade-in" in slug:
            return '''import { motion } from 'framer-motion';

interface FadeInProps {
  children: React.ReactNode;
  delay?: number;
}

export function FadeIn({ children, delay = 0 }: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
    >
      {children}
    </motion.div>
  );
}'''
        
        elif "button" in slug:
            return f'''import {{ motion }} from 'framer-motion';

interface {name.replace(" ", "")}Props {{
  children: React.ReactNode;
  onClick?: () => void;
}}

export function {name.replace(" ", "")}({{ children, onClick }}: {name.replace(" ", "")}Props) {{
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="px-6 py-3 bg-blue-500 text-white rounded-lg font-medium"
      onClick={{onClick}}
    >
      {{children}}
    </motion.button>
  );
}}'''
        
        else:
            # Generic template
            component_name = name.replace(" ", "")
            return f'''interface {component_name}Props {{
  children?: React.ReactNode;
  className?: string;
}}

export function {component_name}({{ children, className = "" }}: {component_name}Props) {{
  return (
    <div className={{`{comp_data["tags"][0]} ${{className}}`}}>
      {{children || "{name} Component"}}
    </div>
  );
}}'''