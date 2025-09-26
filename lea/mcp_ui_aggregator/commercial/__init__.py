"""Commercial features for MCP UI Aggregator.

This module contains features that support the commercial aspects of the MCP UI Aggregator
as outlined in the business plan.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

from pydantic import BaseModel, Field


class SubscriptionTier(str, Enum):
    """Subscription tier enumeration."""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class UsageMetrics(BaseModel):
    """Usage metrics for tracking and billing."""
    user_id: Optional[str] = None
    api_calls: int = Field(default=0, description="Number of API calls made")
    components_accessed: int = Field(default=0, description="Number of components accessed")
    search_queries: int = Field(default=0, description="Number of search queries made")
    code_generations: int = Field(default=0, description="Number of code generations")
    libraries_used: List[str] = Field(default_factory=list, description="UI libraries accessed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SubscriptionLimits(BaseModel):
    """Subscription limits for different tiers."""
    tier: SubscriptionTier
    daily_api_calls: int = Field(description="Daily API call limit")
    monthly_components: int = Field(description="Monthly component access limit")
    libraries_access: List[str] = Field(description="Available UI libraries")
    vector_search: bool = Field(default=False, description="Vector search enabled")
    premium_templates: bool = Field(default=False, description="Access to premium templates")
    priority_support: bool = Field(default=False, description="Priority support")
    custom_themes: bool = Field(default=False, description="Custom theme generation")
    team_collaboration: bool = Field(default=False, description="Team collaboration features")


# Predefined subscription tiers
SUBSCRIPTION_TIERS = {
    SubscriptionTier.FREE: SubscriptionLimits(
        tier=SubscriptionTier.FREE,
        daily_api_calls=100,
        monthly_components=50,
        libraries_access=["material", "shadcn"],
        vector_search=False,
        premium_templates=False,
        priority_support=False,
        custom_themes=False,
        team_collaboration=False
    ),
    SubscriptionTier.BASIC: SubscriptionLimits(
        tier=SubscriptionTier.BASIC,
        daily_api_calls=1000,
        monthly_components=500,
        libraries_access=["material", "shadcn", "chakra"],
        vector_search=True,
        premium_templates=False,
        priority_support=False,
        custom_themes=False,
        team_collaboration=False
    ),
    SubscriptionTier.PRO: SubscriptionLimits(
        tier=SubscriptionTier.PRO,
        daily_api_calls=10000,
        monthly_components=5000,
        libraries_access=["material", "shadcn", "chakra", "antd", "mantine"],
        vector_search=True,
        premium_templates=True,
        priority_support=True,
        custom_themes=True,
        team_collaboration=True
    ),
    SubscriptionTier.ENTERPRISE: SubscriptionLimits(
        tier=SubscriptionTier.ENTERPRISE,
        daily_api_calls=-1,  # Unlimited
        monthly_components=-1,  # Unlimited
        libraries_access=["material", "shadcn", "chakra", "antd", "mantine"],
        vector_search=True,
        premium_templates=True,
        priority_support=True,
        custom_themes=True,
        team_collaboration=True
    )
}


class CommercialValidator:
    """Validates commercial usage and enforces limits."""
    
    def __init__(self):
        self.usage_cache: Dict[str, UsageMetrics] = {}
    
    def check_usage_limits(self, user_id: str, subscription_tier: SubscriptionTier) -> Dict[str, Any]:
        """Check if user has exceeded usage limits."""
        limits = SUBSCRIPTION_TIERS.get(subscription_tier)
        if not limits:
            return {"allowed": False, "reason": "Invalid subscription tier"}
        
        # Get current usage
        usage = self.usage_cache.get(user_id, UsageMetrics(user_id=user_id))
        
        # Check daily API limits
        if limits.daily_api_calls > 0 and usage.api_calls >= limits.daily_api_calls:
            return {
                "allowed": False,
                "reason": f"Daily API limit exceeded ({limits.daily_api_calls})",
                "upgrade_required": True
            }
        
        # Check monthly component limits
        if limits.monthly_components > 0 and usage.components_accessed >= limits.monthly_components:
            return {
                "allowed": False,
                "reason": f"Monthly component limit exceeded ({limits.monthly_components})",
                "upgrade_required": True
            }
        
        return {"allowed": True}
    
    def check_library_access(self, namespace: str, subscription_tier: SubscriptionTier) -> bool:
        """Check if user has access to a specific UI library."""
        limits = SUBSCRIPTION_TIERS.get(subscription_tier)
        if not limits:
            return False
        
        return namespace in limits.libraries_access
    
    def track_usage(self, user_id: str, action: str, **kwargs):
        """Track user usage for billing and analytics."""
        if user_id not in self.usage_cache:
            self.usage_cache[user_id] = UsageMetrics(user_id=user_id)
        
        usage = self.usage_cache[user_id]
        
        if action == "api_call":
            usage.api_calls += 1
        elif action == "component_access":
            usage.components_accessed += 1
            if "namespace" in kwargs:
                if kwargs["namespace"] not in usage.libraries_used:
                    usage.libraries_used.append(kwargs["namespace"])
        elif action == "search_query":
            usage.search_queries += 1
        elif action == "code_generation":
            usage.code_generations += 1
        
        usage.timestamp = datetime.utcnow()
    
    def get_usage_stats(self, user_id: str) -> Optional[UsageMetrics]:
        """Get usage statistics for a user."""
        return self.usage_cache.get(user_id)


class PremiumFeatures:
    """Premium features available to paid subscribers."""
    
    @staticmethod
    def generate_custom_theme(base_library: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a custom theme configuration (Pro/Enterprise feature)."""
        # This would integrate with theme generation systems
        theme_config = {
            "library": base_library,
            "primary_color": preferences.get("primary_color", "#007bff"),
            "secondary_color": preferences.get("secondary_color", "#6c757d"),
            "font_family": preferences.get("font_family", "Inter, sans-serif"),
            "border_radius": preferences.get("border_radius", "8px"),
            "spacing_scale": preferences.get("spacing_scale", "1.2"),
        }
        
        if base_library == "material":
            theme_config["theme_type"] = "mui"
            theme_config["config"] = {
                "palette": {
                    "primary": {"main": theme_config["primary_color"]},
                    "secondary": {"main": theme_config["secondary_color"]}
                },
                "typography": {"fontFamily": theme_config["font_family"]},
                "shape": {"borderRadius": int(theme_config["border_radius"].replace("px", ""))}
            }
        elif base_library == "chakra":
            theme_config["theme_type"] = "chakra"
            theme_config["config"] = {
                "colors": {
                    "brand": theme_config["primary_color"],
                    "gray": theme_config["secondary_color"]
                },
                "fonts": {"body": theme_config["font_family"]},
                "radii": {"base": theme_config["border_radius"]}
            }
        
        return theme_config
    
    @staticmethod
    def get_premium_templates() -> List[Dict[str, Any]]:
        """Get premium page/component templates (Pro/Enterprise feature)."""
        return [
            {
                "name": "SaaS Landing Page",
                "description": "Modern SaaS landing page with hero section, features, pricing, and testimonials",
                "category": "landing",
                "libraries": ["material", "chakra", "antd"],
                "components": ["hero", "features", "pricing", "testimonials", "cta"],
                "premium": True
            },
            {
                "name": "E-commerce Dashboard",
                "description": "Complete e-commerce admin dashboard with analytics, orders, and inventory",
                "category": "dashboard",
                "libraries": ["material", "antd", "mantine"],
                "components": ["sidebar", "charts", "tables", "cards", "forms"],
                "premium": True
            },
            {
                "name": "Blog Platform",
                "description": "Full-featured blog platform with posts, comments, and user management",
                "category": "content",
                "libraries": ["shadcn", "chakra"],
                "components": ["header", "article", "sidebar", "comments", "pagination"],
                "premium": True
            },
            {
                "name": "Team Collaboration Tool",
                "description": "Modern team collaboration interface with chat, files, and project management",
                "category": "productivity",
                "libraries": ["material", "mantine"],
                "components": ["chat", "file-browser", "kanban", "calendar", "notifications"],
                "premium": True
            }
        ]
    
    @staticmethod
    def analyze_component_usage(components: List[str]) -> Dict[str, Any]:
        """Analyze component usage patterns for optimization suggestions (Enterprise feature)."""
        return {
            "total_components": len(components),
            "most_used_libraries": ["material", "chakra", "antd"],
            "component_categories": {
                "buttons": len([c for c in components if "button" in c.lower()]),
                "forms": len([c for c in components if any(word in c.lower() for word in ["input", "form", "select"])]),
                "layout": len([c for c in components if any(word in c.lower() for word in ["grid", "layout", "container"])]),
                "navigation": len([c for c in components if any(word in c.lower() for word in ["nav", "menu", "breadcrumb"])])
            },
            "optimization_suggestions": [
                "Consider using a consistent design system across all components",
                "Reduce bundle size by tree-shaking unused components",
                "Implement component lazy loading for better performance",
                "Consider using a theme provider for consistent styling"
            ],
            "bundle_analysis": {
                "estimated_size": f"{len(components) * 15}KB",
                "tree_shaking_potential": "30-40% size reduction possible",
                "recommended_imports": "Use named imports to reduce bundle size"
            }
        }


# Global commercial validator instance
commercial_validator = CommercialValidator()