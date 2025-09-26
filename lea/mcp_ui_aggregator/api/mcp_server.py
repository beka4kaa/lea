"""MCP Server implementation for Lea UI Components."""

import json
import asyncio
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest, 
    ListToolsResult,
    Tool,
    TextContent,
    JSONRPCMessage,
    InitializeRequest,
    InitializeResult,
    ServerCapabilities,
    ToolsCapability
)

from ..providers.registry import get_all_providers
from ..models.component_manifest import ComponentManifest, Provider, ComponentCategory


class LeaMCPServer:
    """MCP Server for Lea UI Components system."""
    
    def __init__(self):
        self.server = Server("lea-ui-components")
        self.providers = {}
        self._setup_handlers()
    
    async def initialize(self):
        """Initialize providers."""
        providers = get_all_providers()
        for provider in providers:
            self.providers[provider.provider_name.value] = provider
    
    def _setup_handlers(self):
        """Setup MCP request handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available MCP tools."""
            return [
                Tool(
                    name="list_components",
                    description="List all available UI components with optional filtering",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "provider": {
                                "type": "string",
                                "description": "Filter by provider (magicui, shadcn, daisyui, etc.)",
                                "enum": list(self.providers.keys())
                            },
                            "category": {
                                "type": "string", 
                                "description": "Filter by category (animated, forms, navigation, etc.)"
                            },
                            "framework": {
                                "type": "string",
                                "description": "Filter by framework (react, vue, svelte, etc.)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of components to return",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 20
                            },
                            "offset": {
                                "type": "integer", 
                                "description": "Number of components to skip",
                                "minimum": 0,
                                "default": 0
                            }
                        }
                    }
                ),
                Tool(
                    name="search_components",
                    description="Search UI components by query with semantic matching",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (e.g., 'button', 'navigation menu', 'form input')"
                            },
                            "provider": {
                                "type": "string",
                                "description": "Filter by provider",
                                "enum": list(self.providers.keys())
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter by category"
                            },
                            "framework": {
                                "type": "string", 
                                "description": "Target framework for compatibility"
                            },
                            "free_only": {
                                "type": "boolean",
                                "description": "Only return free components",
                                "default": False
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results to return",
                                "minimum": 1,
                                "maximum": 50,
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_component_code",
                    description="Get the complete source code for a specific component",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_id": {
                                "type": "string",
                                "description": "Component ID (e.g., 'shadcn/button', 'magicui/animated-beam')"
                            },
                            "format": {
                                "type": "string", 
                                "description": "Code format preference",
                                "enum": ["tsx", "jsx", "vue", "svelte", "html", "auto"],
                                "default": "auto"
                            }
                        },
                        "required": ["component_id"]
                    }
                ),
                Tool(
                    name="get_component_docs",
                    description="Get documentation and usage examples for a component",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_id": {
                                "type": "string",
                                "description": "Component ID"
                            }
                        },
                        "required": ["component_id"]
                    }
                ),
                Tool(
                    name="get_block",
                    description="Get a ready-to-use UI block with multiple components (auth, pricing, navbar, hero)",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "block_type": {
                                "type": "string",
                                "description": "Type of UI block",
                                "enum": ["auth", "pricing", "navbar", "hero", "footer", "dashboard", "landing"]
                            },
                            "target": {
                                "type": "string",
                                "description": "Target framework",
                                "enum": ["nextjs", "react", "vue", "svelte"],
                                "default": "nextjs"
                            },
                            "style": {
                                "type": "string",
                                "description": "Styling approach", 
                                "enum": ["tailwind", "css-modules", "styled-components"],
                                "default": "tailwind"
                            }
                        },
                        "required": ["block_type"]
                    }
                ),
                Tool(
                    name="install_plan",
                    description="Get installation plan and dependencies for components or blocks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of component IDs to install"
                            },
                            "target": {
                                "type": "string",
                                "description": "Target framework",
                                "enum": ["nextjs", "react", "vue", "svelte"],
                                "default": "nextjs"  
                            },
                            "package_manager": {
                                "type": "string",
                                "description": "Package manager preference",
                                "enum": ["npm", "yarn", "pnpm", "bun"],
                                "default": "npm"
                            }
                        },
                        "required": ["component_ids"]
                    }
                ),
                Tool(
                    name="verify",
                    description="Verify component code and dependencies for correctness",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Component code to verify"
                            },
                            "framework": {
                                "type": "string",
                                "description": "Target framework for verification",
                                "enum": ["react", "vue", "svelte", "nextjs"]
                            },
                            "check_imports": {
                                "type": "boolean",
                                "description": "Check import statements",
                                "default": True
                            },
                            "check_syntax": {
                                "type": "boolean", 
                                "description": "Check syntax validity",
                                "default": True
                            }
                        },
                        "required": ["code", "framework"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "list_components":
                    return await self._handle_list_components(arguments)
                elif name == "search_components":
                    return await self._handle_search_components(arguments)
                elif name == "get_component_code":
                    return await self._handle_get_component_code(arguments)
                elif name == "get_component_docs":
                    return await self._handle_get_component_docs(arguments)
                elif name == "get_block":
                    return await self._handle_get_block(arguments)
                elif name == "install_plan":
                    return await self._handle_install_plan(arguments)
                elif name == "verify":
                    return await self._handle_verify(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool()
async def list_components_tool(
    namespace: Optional[str] = None,
    component_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """List UI components with optional filtering.
    
    Args:
        namespace: Filter by namespace (material, shadcn)
        component_type: Filter by component type
        limit: Maximum number of components to return
        offset: Number of components to skip
    """
    return await list_components(namespace, component_type, limit, offset)


@mcp.tool()
async def search_component_tool(
    query: str,
    namespace: Optional[str] = None,
    component_type: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """Search for UI components by name, title, description, or tags.
    
    Args:
        query: Search query string
        namespace: Filter by namespace
        component_type: Filter by component type
        limit: Maximum number of results
    """
    return await search_component(query, namespace, component_type, limit)


@mcp.tool()
async def get_component_code_tool(
    component_id: Optional[int] = None,
    component_name: Optional[str] = None,
    namespace: Optional[str] = None,
    include_examples: bool = True
) -> Dict[str, Any]:
    """Get code examples for a UI component.
    
    Args:
        component_id: Component ID
        component_name: Component name (requires namespace if provided)
        namespace: Component namespace
        include_examples: Whether to include code examples
    """
    return await get_component_code(component_id, component_name, namespace, include_examples)


@mcp.tool()
async def get_component_docs_tool(
    component_id: Optional[int] = None,
    component_name: Optional[str] = None,
    namespace: Optional[str] = None,
    section_type: Optional[str] = None
) -> Dict[str, Any]:
    """Get documentation for a UI component.
    
    Args:
        component_id: Component ID
        component_name: Component name (requires namespace if provided)
        namespace: Component namespace
        section_type: Filter by documentation section type
    """
    return await get_component_docs(component_id, component_name, namespace, section_type)


@mcp.tool()
async def install_component_tool(
    namespace: str,
    component_name: str,
    package_manager: str = "npm"
) -> Dict[str, Any]:
    """Get installation instructions for a component.
    
    Args:
        namespace: Component namespace (material, shadcn)
        component_name: Name of the component to install
        package_manager: Package manager to use (npm, yarn, pnpm)
    """
    return await install_component(namespace, component_name, package_manager)


# Template Tools

@mcp.tool()
async def list_templates_tool() -> Dict[str, Any]:
    """List all available page templates grouped by type."""
    return await list_templates()


@mcp.tool()
async def get_template_info_tool(template_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific template.
    
    Args:
        template_id: ID of the template to retrieve (e.g., 'react_landing_modern')
    """
    return await get_template_info(template_id)


@mcp.tool()
async def get_predefined_templates_tool() -> Dict[str, Any]:
    """Get all predefined page templates."""
    return await list_templates()


# AI-Enhanced Tools

@mcp.tool()
async def ai_search_components_tool(
    query: str,
    limit: int = 10,
    namespace: Optional[str] = None,
    include_suggestions: bool = True
) -> Dict[str, Any]:
    """AI-powered semantic search for components with intelligent suggestions.
    
    Args:
        query: Natural language search query (e.g., "button for forms", "navigation components")
        limit: Maximum number of results
        namespace: Filter by specific framework namespace
        include_suggestions: Whether to include AI-powered recommendations
    """
    return await ai_search_components(query, limit, namespace, include_suggestions)


@mcp.tool()
async def suggest_component_combinations_tool(
    selected_components: List[str],
    project_type: Optional[str] = None,
    limit: int = 8
) -> Dict[str, Any]:
    """Get AI suggestions for components that work well together.
    
    Args:
        selected_components: List of component names or IDs already selected
        project_type: Type of project (landing, dashboard, ecommerce, blog, portfolio)
        limit: Maximum number of suggestions
    """
    return await suggest_component_combinations(selected_components, project_type, limit)


@mcp.tool()
async def ai_suggest_templates_tool(
    query: str,
    framework: Optional[str] = None,
    project_context: Optional[Dict[str, Any]] = None,
    limit: int = 6
) -> Dict[str, Any]:
    """Get AI-powered template suggestions based on natural language description.
    
    Args:
        query: Natural language description of what you want to build
        framework: Preferred framework (react, vue, html)
        project_context: Additional context like {"industry": "tech", "timeline": "quick", "experience_level": "beginner"}
        limit: Maximum number of suggestions
    """
    return await ai_suggest_templates(query, framework, project_context, limit)


@mcp.tool()
async def analyze_generated_code_tool(
    code: str,
    framework: str,
    component_type: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze generated code for quality and improvements."""
    return await analyze_generated_code(code, framework, component_type)


@mcp.tool()
async def list_available_themes_tool(
    project_type: Optional[str] = None,
    industry: Optional[str] = None,
    include_preview: bool = True
) -> Dict[str, Any]:
    """List all available themes with suggestions."""
    return await list_available_themes_tool(project_type, industry, include_preview)


@mcp.tool()
async def apply_theme_to_template_tool(
    template_id: str,
    theme_id: str,
    framework: str,
    customizations: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Apply a theme to a template."""
    return await apply_theme_to_template_tool(template_id, theme_id, framework, customizations)


@mcp.tool()
async def generate_custom_theme_tool(
    name: str,
    primary_color: str,
    style: str,
    secondary_color: Optional[str] = None,
    mood: Optional[str] = None,
    industry: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a custom theme based on preferences."""
    return await generate_custom_theme_tool(name, primary_color, style, secondary_color, mood, industry)


@mcp.tool()
async def preview_theme_combinations_tool(
    component_types: List[str],
    framework: str,
    theme_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Preview theme combinations with components."""
    return await preview_theme_combinations_tool(component_types, framework, theme_ids)


# Resources


@mcp.resource("components://material")
async def material_components() -> str:
    """Material UI components resource."""
    result = await list_components(namespace="material", limit=100)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("components://shadcn")
async def shadcn_components() -> str:
    """shadcn/ui components resource."""
    result = await list_components(namespace="shadcn", limit=100)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("components://chakra")
async def chakra_components() -> str:
    """Chakra UI components resource."""
    result = await list_components(namespace="chakra", limit=100)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("components://antd")
async def antd_components() -> str:
    """Ant Design components resource."""
    result = await list_components(namespace="antd", limit=100)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("components://mantine")
async def mantine_components() -> str:
    """Mantine components resource."""
    result = await list_components(namespace="mantine", limit=100)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("components://search")
async def search_interface() -> str:
    """Search interface metadata."""
    result = {
        "search_interface": {
            "description": "Search for UI components across all namespaces",
            "endpoints": {
                "search": "Use search_component_tool with query parameter",
                "list": "Use list_components_tool with optional filters"
            },
            "supported_namespaces": ["material", "shadcn", "chakra", "antd", "mantine"],
            "search_fields": ["name", "title", "description", "tags"]
        }
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("templates://all")
async def templates_interface() -> str:
    """Templates interface metadata."""
    result = {
        "templates_interface": {
            "description": "Access to pre-built page templates for rapid development",
            "endpoints": {
                "list": "Use list_templates_tool to see all available templates",
                "info": "Use get_template_info_tool with template_id",
                "generate": "Use generate_template_code_tool with template_id and customizations",
                "customize": "Use customize_template_tool with template_id and customizations"
            },
            "supported_frameworks": ["react", "vue", "html"],
            "template_types": ["landing", "dashboard", "ecommerce", "blog", "portfolio"],
            "customization_options": {
                "texts": "Update text content throughout the template",
                "styles": "Apply custom CSS styles",
                "components": "Modify component properties and configurations"
            }
        }
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.resource("ai://enhanced")
async def ai_interface() -> str:
    """AI-enhanced tools interface metadata."""
    result = {
        "ai_interface": {
            "description": "AI-powered enhancements for intelligent component and template suggestions",
            "endpoints": {
                "semantic_search": "Use ai_search_components_tool for natural language component search",
                "component_suggestions": "Use suggest_component_combinations_tool for complementary components",
                "template_suggestions": "Use ai_suggest_templates_tool for intelligent template recommendations",
                "code_analysis": "Use analyze_generated_code_tool for quality analysis and improvements"
            },
            "ai_capabilities": {
                "semantic_search": "Understands natural language queries and finds relevant components",
                "component_relationships": "Knows which components work well together",
                "template_matching": "Matches user intent to appropriate templates",
                "code_quality": "Analyzes code quality and suggests improvements",
                "contextual_recommendations": "Considers project type and user experience level"
            },
            "supported_contexts": {
                "project_types": ["landing", "dashboard", "ecommerce", "blog", "portfolio", "webapp"],
                "industries": ["tech", "ecommerce", "media", "finance", "healthcare", "education"],
                "experience_levels": ["beginner", "intermediate", "advanced"],
                "frameworks": ["react", "vue", "html"]
            }
        }
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


async def init_mcp_server() -> None:
    """Initialize MCP server."""
    # Create database tables
    await create_tables()
    
    print(f"MCP Server '{settings.mcp_server_name}' initialized")
    print(f"Database: {settings.database_url}")
    print(f"Component tools: list_components_tool, search_component_tool, get_component_code_tool, get_component_docs_tool, install_component_tool")
    print(f"Template tools: list_templates_tool, get_template_info_tool, generate_template_code_tool, customize_template_tool")
    print(f"AI-enhanced tools: ai_search_components_tool, suggest_component_combinations_tool, ai_suggest_templates_tool, analyze_generated_code_tool")
    print(f"Resources: components://material, components://shadcn, components://chakra, components://antd, components://mantine, components://search, templates://all, ai://enhanced")


# Export the mcp server instance
__all__ = ["mcp", "init_mcp_server"]