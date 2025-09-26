"""Theme system for UI components and templates."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ThemeCategory(Enum):
    """Theme categories."""
    CORPORATE = "corporate"
    CREATIVE = "creative"
    MINIMAL = "minimal"
    COLORFUL = "colorful"
    DARK = "dark"
    LIGHT = "light"


@dataclass
class ColorPalette:
    """Color palette for themes."""
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    success: str
    warning: str
    error: str
    info: str


@dataclass
class Typography:
    """Typography settings for themes."""
    font_family_primary: str
    font_family_secondary: str
    font_size_base: str
    font_size_small: str
    font_size_large: str
    font_weight_normal: str
    font_weight_bold: str
    line_height_base: str


@dataclass
class Spacing:
    """Spacing system for themes."""
    xs: str
    sm: str
    md: str
    lg: str
    xl: str
    xxl: str


@dataclass
class BorderRadius:
    """Border radius system for themes."""
    none: str
    sm: str
    md: str
    lg: str
    xl: str
    full: str


@dataclass
class Theme:
    """Complete theme definition."""
    id: str
    name: str
    description: str
    category: ThemeCategory
    colors: ColorPalette
    typography: Typography
    spacing: Spacing
    border_radius: BorderRadius
    shadows: Dict[str, str]
    breakpoints: Dict[str, str]
    custom_properties: Dict[str, Any]


class ThemeRegistry:
    """Registry for managing themes."""
    
    def __init__(self):
        self.themes = {}
        self._initialize_default_themes()
    
    def _initialize_default_themes(self):
        """Initialize default theme collection."""
        
        # Modern Light Theme
        self.themes["modern_light"] = Theme(
            id="modern_light",
            name="Modern Light",
            description="Clean and modern light theme with blue accents",
            category=ThemeCategory.LIGHT,
            colors=ColorPalette(
                primary="#2563eb",
                secondary="#64748b",
                accent="#06b6d4",
                background="#ffffff",
                surface="#f8fafc",
                text_primary="#0f172a",
                text_secondary="#64748b",
                success="#10b981",
                warning="#f59e0b",
                error="#ef4444",
                info="#3b82f6"
            ),
            typography=Typography(
                font_family_primary="'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
                font_family_secondary="'JetBrains Mono', 'Courier New', monospace",
                font_size_base="16px",
                font_size_small="14px",
                font_size_large="18px",
                font_weight_normal="400",
                font_weight_bold="600",
                line_height_base="1.5"
            ),
            spacing=Spacing(
                xs="0.25rem",
                sm="0.5rem",
                md="1rem",
                lg="1.5rem",
                xl="2rem",
                xxl="3rem"
            ),
            border_radius=BorderRadius(
                none="0",
                sm="0.25rem",
                md="0.5rem",
                lg="0.75rem",
                xl="1rem",
                full="9999px"
            ),
            shadows={
                "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
                "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
                "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
            },
            breakpoints={
                "sm": "640px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px",
                "2xl": "1536px"
            },
            custom_properties={}
        )
        
        # Dark Professional Theme
        self.themes["dark_professional"] = Theme(
            id="dark_professional",
            name="Dark Professional",
            description="Professional dark theme with purple accents",
            category=ThemeCategory.DARK,
            colors=ColorPalette(
                primary="#8b5cf6",
                secondary="#6b7280",
                accent="#06b6d4",
                background="#111827",
                surface="#1f2937",
                text_primary="#f9fafb",
                text_secondary="#d1d5db",
                success="#10b981",
                warning="#f59e0b",
                error="#ef4444",
                info="#3b82f6"
            ),
            typography=Typography(
                font_family_primary="'Roboto', -apple-system, BlinkMacSystemFont, sans-serif",
                font_family_secondary="'Source Code Pro', 'Courier New', monospace",
                font_size_base="16px",
                font_size_small="14px",
                font_size_large="18px",
                font_weight_normal="400",
                font_weight_bold="500",
                line_height_base="1.6"
            ),
            spacing=Spacing(
                xs="0.25rem",
                sm="0.5rem",
                md="1rem",
                lg="1.5rem",
                xl="2rem",
                xxl="3rem"
            ),
            border_radius=BorderRadius(
                none="0",
                sm="0.125rem",
                md="0.375rem",
                lg="0.5rem",
                xl="0.75rem",
                full="9999px"
            ),
            shadows={
                "sm": "0 1px 2px 0 rgb(0 0 0 / 0.2)",
                "md": "0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.2)",
                "lg": "0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.2)",
                "xl": "0 20px 25px -5px rgb(0 0 0 / 0.3), 0 8px 10px -6px rgb(0 0 0 / 0.2)"
            },
            breakpoints={
                "sm": "640px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px",
                "2xl": "1536px"
            },
            custom_properties={}
        )
        
        # Minimal Theme
        self.themes["minimal"] = Theme(
            id="minimal",
            name="Minimal",
            description="Ultra-minimal theme with neutral colors",
            category=ThemeCategory.MINIMAL,
            colors=ColorPalette(
                primary="#374151",
                secondary="#9ca3af",
                accent="#6b7280",
                background="#ffffff",
                surface="#f9fafb",
                text_primary="#111827",
                text_secondary="#6b7280",
                success="#059669",
                warning="#d97706",
                error="#dc2626",
                info="#2563eb"
            ),
            typography=Typography(
                font_family_primary="'System UI', -apple-system, BlinkMacSystemFont, sans-serif",
                font_family_secondary="'SF Mono', 'Monaco', monospace",
                font_size_base="16px",
                font_size_small="14px",
                font_size_large="18px",
                font_weight_normal="400",
                font_weight_bold="500",
                line_height_base="1.5"
            ),
            spacing=Spacing(
                xs="0.25rem",
                sm="0.5rem",
                md="1rem",
                lg="1.5rem",
                xl="2rem",
                xxl="3rem"
            ),
            border_radius=BorderRadius(
                none="0",
                sm="0.125rem",
                md="0.25rem",
                lg="0.375rem",
                xl="0.5rem",
                full="9999px"
            ),
            shadows={
                "sm": "0 1px 2px 0 rgb(0 0 0 / 0.04)",
                "md": "0 2px 4px 0 rgb(0 0 0 / 0.06)",
                "lg": "0 4px 8px 0 rgb(0 0 0 / 0.08)",
                "xl": "0 8px 16px 0 rgb(0 0 0 / 0.1)"
            },
            breakpoints={
                "sm": "640px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px",
                "2xl": "1536px"
            },
            custom_properties={}
        )
        
        # Vibrant Creative Theme
        self.themes["vibrant_creative"] = Theme(
            id="vibrant_creative",
            name="Vibrant Creative",
            description="Bold and colorful theme for creative projects",
            category=ThemeCategory.COLORFUL,
            colors=ColorPalette(
                primary="#ec4899",
                secondary="#8b5cf6",
                accent="#06b6d4",
                background="#fefefe",
                surface="#fef7ff",
                text_primary="#1e1b4b",
                text_secondary="#7c3aed",
                success="#10b981",
                warning="#f59e0b",
                error="#ef4444",
                info="#3b82f6"
            ),
            typography=Typography(
                font_family_primary="'Poppins', -apple-system, BlinkMacSystemFont, sans-serif",
                font_family_secondary="'Fira Code', 'Courier New', monospace",
                font_size_base="16px",
                font_size_small="14px",
                font_size_large="18px",
                font_weight_normal="400",
                font_weight_bold="600",
                line_height_base="1.6"
            ),
            spacing=Spacing(
                xs="0.25rem",
                sm="0.5rem",
                md="1rem",
                lg="1.5rem",
                xl="2rem",
                xxl="3rem"
            ),
            border_radius=BorderRadius(
                none="0",
                sm="0.5rem",
                md="0.75rem",
                lg="1rem",
                xl="1.5rem",
                full="9999px"
            ),
            shadows={
                "sm": "0 2px 4px 0 rgb(236 72 153 / 0.1)",
                "md": "0 4px 8px 0 rgb(236 72 153 / 0.15)",
                "lg": "0 8px 16px 0 rgb(236 72 153 / 0.2)",
                "xl": "0 16px 32px 0 rgb(236 72 153 / 0.25)"
            },
            breakpoints={
                "sm": "640px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px",
                "2xl": "1536px"
            },
            custom_properties={}
        )
        
        # Corporate Theme
        self.themes["corporate"] = Theme(
            id="corporate",
            name="Corporate",
            description="Professional corporate theme with navy blue",
            category=ThemeCategory.CORPORATE,
            colors=ColorPalette(
                primary="#1e40af",
                secondary="#475569",
                accent="#0ea5e9",
                background="#ffffff",
                surface="#f1f5f9",
                text_primary="#0f172a",
                text_secondary="#475569",
                success="#16a34a",
                warning="#ca8a04",
                error="#dc2626",
                info="#2563eb"
            ),
            typography=Typography(
                font_family_primary="'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif",
                font_family_secondary="'Consolas', 'Courier New', monospace",
                font_size_base="16px",
                font_size_small="14px",
                font_size_large="18px",
                font_weight_normal="400",
                font_weight_bold="600",
                line_height_base="1.5"
            ),
            spacing=Spacing(
                xs="0.25rem",
                sm="0.5rem",
                md="1rem",
                lg="1.5rem",
                xl="2rem",
                xxl="3rem"
            ),
            border_radius=BorderRadius(
                none="0",
                sm="0.25rem",
                md="0.375rem",
                lg="0.5rem",
                xl="0.75rem",
                full="9999px"
            ),
            shadows={
                "sm": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
                "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
                "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
            },
            breakpoints={
                "sm": "640px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px",
                "2xl": "1536px"
            },
            custom_properties={}
        )
    
    def get_theme(self, theme_id: str) -> Optional[Theme]:
        """Get theme by ID."""
        return self.themes.get(theme_id)
    
    def list_themes(self) -> List[Theme]:
        """Get all available themes."""
        return list(self.themes.values())
    
    def get_themes_by_category(self, category: ThemeCategory) -> List[Theme]:
        """Get themes by category."""
        return [theme for theme in self.themes.values() if theme.category == category]
    
    def register_theme(self, theme: Theme) -> None:
        """Register a new theme."""
        self.themes[theme.id] = theme


# Global theme registry
theme_registry = ThemeRegistry()