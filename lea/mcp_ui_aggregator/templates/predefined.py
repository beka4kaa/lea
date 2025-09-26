"""Predefined page templates for common use cases."""

from typing import Dict, List
from . import (
    PageTemplate, PageSection, TemplateComponent, TemplateType, Framework
)


def create_landing_page_template(framework: Framework = Framework.REACT) -> PageTemplate:
    """Create a modern landing page template."""
    
    # Hero section
    hero_section = PageSection(
        name="hero",
        description="Main hero section with call-to-action",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "hero-container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h1", "className": "hero-title"},
                        content="Welcome to Our Amazing Product"
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h4", "className": "hero-subtitle"},
                        content="Transform your business with our innovative solution"
                    ),
                    TemplateComponent(
                        name="Button",
                        namespace="material",
                        props={"variant": "contained", "size": "large", "color": "primary"},
                        content="Get Started"
                    ),
                    TemplateComponent(
                        name="Button",
                        namespace="material",
                        props={"variant": "outlined", "size": "large"},
                        content="Learn More"
                    )
                ]
            )
        ],
        css_classes=["hero-section", "py-20", "text-center"]
    )
    
    # Features section
    features_section = PageSection(
        name="features",
        description="Product features showcase",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h2", "className": "section-title"},
                        content="Why Choose Us"
                    ),
                    TemplateComponent(
                        name="div",
                        namespace="html",
                        props={"className": "features-grid"},
                        children=[
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "feature-card"},
                                children=[
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h5"},
                                        content="🚀 Fast & Reliable"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body1"},
                                        content="Lightning-fast performance with 99.9% uptime guarantee."
                                    )
                                ]
                            ),
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "feature-card"},
                                children=[
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h5"},
                                        content="🔒 Secure & Private"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body1"},
                                        content="Enterprise-grade security with end-to-end encryption."
                                    )
                                ]
                            ),
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "feature-card"},
                                children=[
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h5"},
                                        content="📈 Scalable"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body1"},
                                        content="Grows with your business from startup to enterprise."
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["features-section", "py-16"]
    )
    
    # CTA section
    cta_section = PageSection(
        name="cta",
        description="Final call-to-action",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "cta-container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h3"},
                        content="Ready to Get Started?"
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "body1"},
                        content="Join thousands of satisfied customers today."
                    ),
                    TemplateComponent(
                        name="Button",
                        namespace="material",
                        props={"variant": "contained", "size": "large", "color": "primary"},
                        content="Start Free Trial"
                    )
                ]
            )
        ],
        css_classes=["cta-section", "py-16", "text-center", "bg-primary"]
    )
    
    return PageTemplate(
        name="LandingPage",
        type=TemplateType.LANDING,
        framework=framework,
        description="Modern landing page with hero, features, and CTA sections",
        sections=[hero_section, features_section, cta_section],
        global_styles={
            ".hero-section": "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;",
            ".features-grid": "display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;",
            ".feature-card": "padding: 2rem; height: 100%;",
            ".cta-section": "background: #1976d2; color: white;",
            ".section-title": "text-align: center; margin-bottom: 3rem;"
        },
        dependencies=["@mui/material", "@mui/icons-material"],
        meta_tags={
            "description": "Modern landing page template",
            "keywords": "landing, template, react, material-ui"
        }
    )


def create_dashboard_template(framework: Framework = Framework.REACT) -> PageTemplate:
    """Create a comprehensive dashboard template."""
    
    # Header section
    header_section = PageSection(
        name="header",
        description="Dashboard header with navigation",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "dashboard-header"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h4"},
                        content="Dashboard"
                    ),
                    TemplateComponent(
                        name="Button",
                        namespace="material",
                        props={"variant": "contained", "color": "primary"},
                        content="New Item"
                    )
                ]
            )
        ],
        css_classes=["header-section"]
    )
    
    # Stats section
    stats_section = PageSection(
        name="stats",
        description="Key metrics and statistics",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "stats-grid"},
                children=[
                    TemplateComponent(
                        name="Card",
                        namespace="material",
                        props={"className": "stat-card"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h6", "color": "textSecondary"},
                                content="Total Users"
                            ),
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h3", "color": "primary"},
                                content="12,543"
                            )
                        ]
                    ),
                    TemplateComponent(
                        name="Card",
                        namespace="material",
                        props={"className": "stat-card"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h6", "color": "textSecondary"},
                                content="Revenue"
                            ),
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h3", "color": "primary"},
                                content="$45,231"
                            )
                        ]
                    ),
                    TemplateComponent(
                        name="Card",
                        namespace="material",
                        props={"className": "stat-card"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h6", "color": "textSecondary"},
                                content="Growth"
                            ),
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h3", "color": "success.main"},
                                content="+23.5%"
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["stats-section"]
    )
    
    # Main content section
    content_section = PageSection(
        name="content",
        description="Main dashboard content area",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "dashboard-content"},
                children=[
                    TemplateComponent(
                        name="Card",
                        namespace="material",
                        props={"className": "chart-card"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h6"},
                                content="Analytics Overview"
                            ),
                            TemplateComponent(
                                name="div",
                                namespace="html",
                                props={"className": "chart-placeholder"},
                                content="Chart will be rendered here"
                            )
                        ]
                    ),
                    TemplateComponent(
                        name="Card",
                        namespace="material",
                        props={"className": "table-card"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h6"},
                                content="Recent Activity"
                            ),
                            TemplateComponent(
                                name="div",
                                namespace="html",
                                props={"className": "table-placeholder"},
                                content="Data table will be rendered here"
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["content-section"]
    )
    
    return PageTemplate(
        name="Dashboard",
        type=TemplateType.DASHBOARD,
        framework=framework,
        description="Comprehensive dashboard with stats, charts, and data tables",
        sections=[header_section, stats_section, content_section],
        global_styles={
            ".dashboard-header": "display: flex; justify-content: space-between; align-items: center; padding: 2rem; border-bottom: 1px solid #e0e0e0;",
            ".stats-grid": "display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; padding: 2rem;",
            ".stat-card": "padding: 2rem; text-align: center;",
            ".dashboard-content": "display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; padding: 2rem;",
            ".chart-card, .table-card": "padding: 2rem;",
            ".chart-placeholder, .table-placeholder": "height: 300px; background: #f5f5f5; display: flex; align-items: center; justify-content: center; margin-top: 1rem;"
        },
        dependencies=["@mui/material", "@mui/x-charts", "@mui/x-data-grid"]
    )


def create_ecommerce_template(framework: Framework = Framework.REACT) -> PageTemplate:
    """Create an e-commerce product page template."""
    
    # Product showcase section
    product_section = PageSection(
        name="product",
        description="Product details and images",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "product-container"},
                children=[
                    TemplateComponent(
                        name="div",
                        namespace="html",
                        props={"className": "product-images"},
                        children=[
                            TemplateComponent(
                                name="img",
                                namespace="html",
                                props={"src": "/api/placeholder/400/400", "alt": "Product image", "className": "main-image"}
                            )
                        ]
                    ),
                    TemplateComponent(
                        name="div",
                        namespace="html",
                        props={"className": "product-details"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h4"},
                                content="Premium Wireless Headphones"
                            ),
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "h5", "color": "primary"},
                                content="$299.99"
                            ),
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "body1"},
                                content="Experience superior sound quality with our premium wireless headphones. Features active noise cancellation, 30-hour battery life, and premium materials."
                            ),
                            TemplateComponent(
                                name="Button",
                                namespace="material",
                                props={"variant": "contained", "size": "large", "fullWidth": True},
                                content="Add to Cart"
                            ),
                            TemplateComponent(
                                name="Button",
                                namespace="material",
                                props={"variant": "outlined", "size": "large", "fullWidth": True},
                                content="Add to Wishlist"
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["product-section"]
    )
    
    # Related products section
    related_section = PageSection(
        name="related",
        description="Related product recommendations",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "related-container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h5"},
                        content="You Might Also Like"
                    ),
                    TemplateComponent(
                        name="div",
                        namespace="html",
                        props={"className": "related-grid"},
                        children=[
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "product-card"},
                                children=[
                                    TemplateComponent(
                                        name="img",
                                        namespace="html",
                                        props={"src": "/api/placeholder/200/200", "alt": "Related product"}
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h6"},
                                        content="Wireless Earbuds"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body2", "color": "primary"},
                                        content="$199.99"
                                    )
                                ]
                            ),
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "product-card"},
                                children=[
                                    TemplateComponent(
                                        name="img",
                                        namespace="html",
                                        props={"src": "/api/placeholder/200/200", "alt": "Related product"}
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h6"},
                                        content="Bluetooth Speaker"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body2", "color": "primary"},
                                        content="$149.99"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["related-section"]
    )
    
    return PageTemplate(
        name="EcommercePage",
        type=TemplateType.ECOMMERCE,
        framework=framework,
        description="E-commerce product page with details and recommendations",
        sections=[product_section, related_section],
        global_styles={
            ".product-container": "display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; padding: 2rem; max-width: 1200px; margin: 0 auto;",
            ".product-images .main-image": "width: 100%; border-radius: 8px;",
            ".product-details": "display: flex; flex-direction: column; gap: 1rem;",
            ".related-container": "padding: 2rem; max-width: 1200px; margin: 0 auto;",
            ".related-grid": "display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 2rem;",
            ".product-card": "padding: 1rem; text-align: center;",
            ".product-card img": "width: 100%; border-radius: 8px; margin-bottom: 1rem;"
        },
        dependencies=["@mui/material"]
    )


def create_blog_template(framework: Framework = Framework.REACT) -> PageTemplate:
    """Create a blog layout template."""
    
    # Article section
    article_section = PageSection(
        name="article",
        description="Main blog article content",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "article-container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h3", "component": "h1"},
                        content="The Future of Web Development"
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "subtitle1", "color": "textSecondary"},
                        content="Published on December 15, 2023 by John Doe"
                    ),
                    TemplateComponent(
                        name="img",
                        namespace="html",
                        props={"src": "/api/placeholder/800/400", "alt": "Article header", "className": "article-image"}
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "body1", "paragraph": True},
                        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h5"},
                        content="Key Trends to Watch"
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "body1", "paragraph": True},
                        content="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt."
                    )
                ]
            )
        ],
        css_classes=["article-section"]
    )
    
    # Comments section
    comments_section = PageSection(
        name="comments",
        description="Reader comments and discussion",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "comments-container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h5"},
                        content="Comments"
                    ),
                    TemplateComponent(
                        name="Card",
                        namespace="material",
                        props={"className": "comment-card"},
                        children=[
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "subtitle2"},
                                content="Jane Smith"
                            ),
                            TemplateComponent(
                                name="Typography",
                                namespace="material",
                                props={"variant": "body2"},
                                content="Great article! Very insightful perspective on the future of web development."
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["comments-section"]
    )
    
    return PageTemplate(
        name="BlogPage",
        type=TemplateType.BLOG,
        framework=framework,
        description="Blog article page with content and comments",
        sections=[article_section, comments_section],
        global_styles={
            ".article-container": "max-width: 800px; margin: 0 auto; padding: 2rem;",
            ".article-image": "width: 100%; border-radius: 8px; margin: 2rem 0;",
            ".comments-container": "max-width: 800px; margin: 0 auto; padding: 2rem;",
            ".comment-card": "padding: 1rem; margin: 1rem 0;"
        },
        dependencies=["@mui/material"]
    )


def create_portfolio_template(framework: Framework = Framework.REACT) -> PageTemplate:
    """Create a portfolio showcase template."""
    
    # Hero section
    hero_section = PageSection(
        name="hero",
        description="Portfolio introduction",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "portfolio-hero"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h2"},
                        content="John Doe"
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h5", "color": "textSecondary"},
                        content="Full Stack Developer & Designer"
                    ),
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "body1"},
                        content="Creating beautiful and functional digital experiences for the web."
                    )
                ]
            )
        ],
        css_classes=["hero-section"]
    )
    
    # Projects section
    projects_section = PageSection(
        name="projects",
        description="Portfolio project showcase",
        components=[
            TemplateComponent(
                name="div",
                namespace="html",
                props={"className": "projects-container"},
                children=[
                    TemplateComponent(
                        name="Typography",
                        namespace="material",
                        props={"variant": "h4"},
                        content="Featured Projects"
                    ),
                    TemplateComponent(
                        name="div",
                        namespace="html",
                        props={"className": "projects-grid"},
                        children=[
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "project-card"},
                                children=[
                                    TemplateComponent(
                                        name="img",
                                        namespace="html",
                                        props={"src": "/api/placeholder/400/300", "alt": "Project screenshot"}
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h6"},
                                        content="E-commerce Platform"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body2"},
                                        content="A modern e-commerce solution built with React and Node.js"
                                    ),
                                    TemplateComponent(
                                        name="Button",
                                        namespace="material",
                                        props={"variant": "text"},
                                        content="View Project"
                                    )
                                ]
                            ),
                            TemplateComponent(
                                name="Card",
                                namespace="material",
                                props={"className": "project-card"},
                                children=[
                                    TemplateComponent(
                                        name="img",
                                        namespace="html",
                                        props={"src": "/api/placeholder/400/300", "alt": "Project screenshot"}
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "h6"},
                                        content="Task Management App"
                                    ),
                                    TemplateComponent(
                                        name="Typography",
                                        namespace="material",
                                        props={"variant": "body2"},
                                        content="A collaborative task management tool with real-time updates"
                                    ),
                                    TemplateComponent(
                                        name="Button",
                                        namespace="material",
                                        props={"variant": "text"},
                                        content="View Project"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        css_classes=["projects-section"]
    )
    
    return PageTemplate(
        name="PortfolioPage",
        type=TemplateType.PORTFOLIO,
        framework=framework,
        description="Personal portfolio with project showcase",
        sections=[hero_section, projects_section],
        global_styles={
            ".portfolio-hero": "text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);",
            ".projects-container": "padding: 4rem 2rem; max-width: 1200px; margin: 0 auto;",
            ".projects-grid": "display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem;",
            ".project-card": "padding: 1rem;",
            ".project-card img": "width: 100%; border-radius: 8px; margin-bottom: 1rem;"
        },
        dependencies=["@mui/material"]
    )


# Template registry
TEMPLATE_REGISTRY: Dict[str, PageTemplate] = {
    "landing_react": create_landing_page_template(Framework.REACT),
    "landing_vue": create_landing_page_template(Framework.VUE),
    "landing_html": create_landing_page_template(Framework.HTML),
    "dashboard_react": create_dashboard_template(Framework.REACT),
    "dashboard_vue": create_dashboard_template(Framework.VUE),
    "dashboard_html": create_dashboard_template(Framework.HTML),
    "ecommerce_react": create_ecommerce_template(Framework.REACT),
    "ecommerce_vue": create_ecommerce_template(Framework.VUE),
    "ecommerce_html": create_ecommerce_template(Framework.HTML),
    "blog_react": create_blog_template(Framework.REACT),
    "blog_vue": create_blog_template(Framework.VUE),
    "blog_html": create_blog_template(Framework.HTML),
    "portfolio_react": create_portfolio_template(Framework.REACT),
    "portfolio_vue": create_portfolio_template(Framework.VUE),
    "portfolio_html": create_portfolio_template(Framework.HTML),
}


def get_template(template_id: str) -> PageTemplate:
    """Get a template by ID."""
    return TEMPLATE_REGISTRY.get(template_id)


def list_templates() -> List[Dict[str, str]]:
    """Get list of available templates."""
    templates = []
    for template_id, template in TEMPLATE_REGISTRY.items():
        templates.append({
            "id": template_id,
            "name": template.name,
            "type": template.type.value,
            "framework": template.framework.value,
            "description": template.description
        })
    return templates