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
from ..tools.backend_tools import BackendTools


class LeaMCPServer:
    """MCP Server for Lea UI Components system."""
    
    def __init__(self):
        self.server = Server("lea-ui-components")
        self.providers = {}
        self.backend_tools = BackendTools()
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
                                "enum": ["magicui", "shadcn", "daisyui", "reactbits", "aceternity", "alignui", "twentyfirst", "bentogrids", "nextjsdesign", "hyperui", "tailwindcomponents"]
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
                                "enum": ["magicui", "shadcn", "daisyui", "reactbits", "aceternity", "alignui", "twentyfirst", "bentogrids", "nextjsdesign", "hyperui", "tailwindcomponents"]
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
                ),
                # Backend Generation Tools
                Tool(
                    name="project_init",
                    description="Initialize a new FastAPI project with comprehensive scaffolding",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Project name"
                            },
                            "target_dir": {
                                "type": "string",
                                "description": "Target directory (defaults to current directory)"
                            },
                            "stack": {
                                "type": "string",
                                "description": "Tech stack",
                                "enum": ["fastapi+uvicorn"],
                                "default": "fastapi+uvicorn"
                            },
                            "db": {
                                "type": "string",
                                "description": "Database type",
                                "enum": ["postgres", "sqlite"],
                                "default": "postgres"
                            },
                            "orm": {
                                "type": "string",
                                "description": "ORM type",
                                "enum": ["sqlalchemy+alembic"],
                                "default": "sqlalchemy+alembic"
                            },
                            "queue": {
                                "type": "string",
                                "description": "Queue system",
                                "enum": ["rq", "redis", "none"],
                                "default": "rq"
                            },
                            "docker": {
                                "type": "boolean",
                                "description": "Enable Docker support",
                                "default": True
                            },
                            "ci": {
                                "type": "string",
                                "description": "CI/CD system",
                                "enum": ["github", "gitlab", "none"],
                                "default": "github"
                            },
                            "telemetry": {
                                "type": "boolean",
                                "description": "Enable OpenTelemetry",
                                "default": True
                            },
                            "auth": {
                                "type": "boolean",
                                "description": "Enable JWT authentication",
                                "default": True
                            },
                            "preset": {
                                "type": "string",
                                "description": "Preset configuration",
                                "enum": ["api", "microservice", "full-stack"]
                            }
                        },
                        "required": ["name"]
                    }
                ),
                Tool(
                    name="db_schema_design",
                    description="Generate database models and schemas",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to the project"
                            },
                            "models": {
                                "type": "array",
                                "items": {"type": "object"},
                                "description": "List of model definitions"
                            }
                        },
                        "required": ["project_path", "models"]
                    }
                ),
                Tool(
                    name="api_crud_generate",
                    description="Generate CRUD API endpoints for an entity",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to the project"
                            },
                            "entity": {
                                "type": "string",
                                "description": "Entity name"
                            },
                            "fields": {
                                "type": "array",
                                "items": {"type": "object"},
                                "description": "Entity fields definition"
                            }
                        },
                        "required": ["project_path", "entity", "fields"]
                    }
                ),
                Tool(
                    name="auth_enable",
                    description="Enable authentication in the project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to the project"
                            },
                            "provider": {
                                "type": "string",
                                "description": "Auth provider",
                                "enum": ["jwt", "oauth2", "basic"],
                                "default": "jwt"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="deploy_preset",
                    description="Configure deployment presets",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to the project"
                            },
                            "target": {
                                "type": "string",
                                "description": "Deployment target",
                                "enum": ["railway", "vercel", "docker", "kubernetes"],
                                "default": "railway"
                            }
                        },
                        "required": ["project_path"]
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
                # Backend Generation Tools
                elif name == "project_init":
                    return await self._handle_project_init(arguments)
                elif name == "db_schema_design":
                    return await self._handle_db_schema_design(arguments)
                elif name == "api_crud_generate":
                    return await self._handle_api_crud_generate(arguments)
                elif name == "auth_enable":
                    return await self._handle_auth_enable(arguments)
                elif name == "deploy_preset":
                    return await self._handle_deploy_preset(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def _handle_list_components(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle list_components tool call."""
        provider_filter = args.get("provider")
        category_filter = args.get("category") 
        framework_filter = args.get("framework")
        limit = args.get("limit", 20)
        offset = args.get("offset", 0)
        
        all_components = []
        
        # Get components from providers
        for provider_name, provider in self.providers.items():
            if provider_filter and provider_name != provider_filter:
                continue
            
            try:
                components = await provider.list_components(limit=1000)  # Get all for filtering
                all_components.extend(components)
            except Exception as e:
                continue
        
        # Apply filters
        filtered_components = all_components
        
        if category_filter:
            filtered_components = [c for c in filtered_components if c.category.value == category_filter]
        
        if framework_filter:
            filtered_components = [c for c in filtered_components 
                                 if getattr(c.framework, framework_filter, False)]
        
        # Apply pagination
        paginated = filtered_components[offset:offset + limit]
        
        # Format response
        result = {
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "provider": comp.provider.value,
                    "category": comp.category.value,
                    "description": comp.description,
                    "tags": comp.tags,
                    "framework_support": {
                        "react": comp.framework.react,
                        "vue": comp.framework.vue,
                        "svelte": comp.framework.svelte,
                        "next": comp.framework.next
                    },
                    "license": comp.license.type.value,
                    "free": comp.access.free,
                    "documentation_url": str(comp.documentation_url) if comp.documentation_url else None
                }
                for comp in paginated
            ],
            "total": len(filtered_components),
            "offset": offset,
            "limit": limit
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _handle_search_components(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle search_components tool call."""
        query = args["query"].lower()
        provider_filter = args.get("provider")
        category_filter = args.get("category")
        framework_filter = args.get("framework")
        free_only = args.get("free_only", False)
        limit = args.get("limit", 10)
        
        all_components = []
        
        # Get components from providers
        for provider_name, provider in self.providers.items():
            if provider_filter and provider_name != provider_filter:
                continue
            
            try:
                components = await provider.list_components(limit=1000)
                all_components.extend(components)
            except Exception:
                continue
        
        # Simple search implementation (can be enhanced with BM25/vector search later)
        scored_components = []
        for comp in all_components:
            score = 0
            
            # Name matching (highest weight)
            if query in comp.name.lower():
                score += 10
            
            # Description matching
            if comp.description and query in comp.description.lower():
                score += 5
            
            # Tag matching
            for tag in comp.tags:
                if query in tag.lower():
                    score += 3
            
            # Category matching
            if query in comp.category.value.lower():
                score += 2
            
            if score > 0:
                scored_components.append((score, comp))
        
        # Sort by score and apply filters
        scored_components.sort(key=lambda x: x[0], reverse=True)
        
        filtered_components = []
        for score, comp in scored_components:
            if category_filter and comp.category.value != category_filter:
                continue
            if framework_filter and not getattr(comp.framework, framework_filter, False):
                continue
            if free_only and not comp.access.free:
                continue
            
            filtered_components.append(comp)
        
        # Apply limit
        results = filtered_components[:limit]
        
        # Format response
        result = {
            "query": args["query"],
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "provider": comp.provider.value,
                    "category": comp.category.value,
                    "description": comp.description,
                    "tags": comp.tags,
                    "documentation_url": str(comp.documentation_url) if comp.documentation_url else None,
                    "demo_url": str(comp.demo_url) if comp.demo_url else None
                }
                for comp in results
            ],
            "total_found": len(filtered_components)
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _handle_get_component_code(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle get_component_code tool call."""
        component_id = args["component_id"]
        format_pref = args.get("format", "auto")
        
        # Parse component ID
        if "/" not in component_id:
            return [TextContent(type="text", text="Error: Component ID must be in format 'provider/component'")]
        
        provider_name, comp_slug = component_id.split("/", 1)
        
        if provider_name not in self.providers:
            return [TextContent(type="text", text=f"Error: Provider '{provider_name}' not found")]
        
        provider = self.providers[provider_name]
        
        try:
            component = await provider.get_component(comp_slug)
        except Exception as e:
            return [TextContent(type="text", text=f"Error: Component not found - {str(e)}")]
        
        # Get code in preferred format
        code_content = None
        actual_format = None
        
        if format_pref == "auto" or format_pref == "tsx":
            if component.code.tsx:
                code_content = component.code.tsx
                actual_format = "tsx"
        
        if not code_content and (format_pref == "auto" or format_pref == "jsx"):
            if component.code.jsx:
                code_content = component.code.jsx
                actual_format = "jsx"
        
        if not code_content and (format_pref == "auto" or format_pref == "vue"):
            if component.code.vue:
                code_content = component.code.vue
                actual_format = "vue"
        
        if not code_content and (format_pref == "auto" or format_pref == "html"):
            if component.code.html:
                code_content = component.code.html
                actual_format = "html"
        
        if not code_content:
            # Generate sample code
            code_content = self._generate_sample_code(component, format_pref)
            actual_format = format_pref if format_pref != "auto" else "tsx"
        
        result = {
            "component_id": component_id,
            "name": component.name,
            "format": actual_format,
            "code": code_content,
            "runtime_deps": component.runtime_deps,
            "peer_deps": component.peer_deps,
            "install_commands": component.install.npm if component.install.npm else [],
            "documentation_url": str(component.documentation_url) if component.documentation_url else None
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _handle_get_component_docs(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle get_component_docs tool call."""
        component_id = args["component_id"]
        
        if "/" not in component_id:
            return [TextContent(type="text", text="Error: Component ID must be in format 'provider/component'")]
        
        provider_name, comp_slug = component_id.split("/", 1)
        
        if provider_name not in self.providers:
            return [TextContent(type="text", text=f"Error: Provider '{provider_name}' not found")]
        
        provider = self.providers[provider_name]
        
        try:
            component = await provider.get_component(comp_slug)
        except Exception as e:
            return [TextContent(type="text", text=f"Error: Component not found - {str(e)}")]
        
        result = {
            "component_id": component_id,
            "name": component.name,
            "description": component.description,
            "category": component.category.value,
            "tags": component.tags,
            "framework_support": {
                "react": component.framework.react,
                "vue": component.framework.vue,
                "svelte": component.framework.svelte,
                "angular": component.framework.angular,
                "next": component.framework.next
            },
            "license": {
                "type": component.license.type.value,
                "url": str(component.license.url) if component.license.url else None,
                "commercial": component.license.commercial,
                "redistribute": component.license.redistribute
            },
            "access": {
                "free": component.access.free,
                "pro": component.access.pro,
                "copy_paste": component.access.copy_paste,
                "cli": component.access.cli
            },
            "documentation_url": str(component.documentation_url) if component.documentation_url else None,
            "demo_url": str(component.demo_url) if component.demo_url else None,
            "playground_url": str(component.playground_url) if component.playground_url else None
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _handle_get_block(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle get_block tool call."""
        block_type = args["block_type"]
        target = args.get("target", "nextjs")
        style = args.get("style", "tailwind")
        
        # Generate UI block based on type
        block_data = self._generate_ui_block(block_type, target, style)
        
        return [TextContent(type="text", text=json.dumps(block_data, indent=2))]

    async def _handle_install_plan(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle install_plan tool call."""
        component_ids = args["component_ids"]
        target = args.get("target", "nextjs")
        package_manager = args.get("package_manager", "npm")
        
        all_deps = set()
        all_peer_deps = set()
        commands = []
        
        for component_id in component_ids:
            if "/" not in component_id:
                continue
            
            provider_name, comp_slug = component_id.split("/", 1)
            
            if provider_name not in self.providers:
                continue
            
            provider = self.providers[provider_name]
            
            try:
                component = await provider.get_component(comp_slug)
                all_deps.update(component.runtime_deps)
                all_peer_deps.update(component.peer_deps)
                
                # Add CLI command if available
                if component.access.cli:
                    commands.append({
                        "type": "cli",
                        "command": component.access.cli,
                        "description": f"Install {component.name}"
                    })
                    
            except Exception:
                continue
        
        # Generate install commands
        if all_deps or all_peer_deps:
            deps_to_install = list(all_deps | all_peer_deps)
            
            if package_manager == "npm":
                cmd = f"npm install {' '.join(deps_to_install)}"
            elif package_manager == "yarn":
                cmd = f"yarn add {' '.join(deps_to_install)}"
            elif package_manager == "pnpm":
                cmd = f"pnpm add {' '.join(deps_to_install)}"
            elif package_manager == "bun":
                cmd = f"bun add {' '.join(deps_to_install)}"
            else:
                cmd = f"npm install {' '.join(deps_to_install)}"
            
            commands.insert(0, {
                "type": "install",
                "command": cmd,
                "description": "Install dependencies"
            })
        
        result = {
            "component_ids": component_ids,
            "target": target,
            "package_manager": package_manager,
            "runtime_dependencies": list(all_deps),
            "peer_dependencies": list(all_peer_deps),
            "commands": commands
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _handle_verify(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle verify tool call."""
        code = args["code"]
        framework = args["framework"]
        check_imports = args.get("check_imports", True)
        check_syntax = args.get("check_syntax", True)
        
        issues = []
        
        if check_syntax:
            # Basic syntax checks (can be enhanced with AST parsing)
            if framework in ["react", "nextjs"]:
                if "import" in code and not code.strip().startswith("import"):
                    issues.append({
                        "type": "syntax",
                        "severity": "warning", 
                        "message": "Imports should be at the top of the file"
                    })
                
                if "export default" not in code and "export {" not in code:
                    issues.append({
                        "type": "syntax",
                        "severity": "error",
                        "message": "Component must have a default export"
                    })
        
        if check_imports:
            # Check for common import issues
            import_lines = [line.strip() for line in code.split("\n") if line.strip().startswith("import")]
            
            for line in import_lines:
                if "from ''" in line or 'from ""' in line:
                    issues.append({
                        "type": "import",
                        "severity": "error",
                        "message": f"Empty import path: {line}"
                    })
        
        result = {
            "code_length": len(code),
            "framework": framework,
            "issues": issues,
            "is_valid": len([i for i in issues if i["severity"] == "error"]) == 0,
            "suggestions": [
                "Consider adding TypeScript types for better development experience",
                "Add proper error boundaries for production use"
            ] if not issues else []
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    def _generate_sample_code(self, component: ComponentManifest, format_pref: str) -> str:
        """Generate sample code for component."""
        name = component.name.replace(" ", "")
        
        if format_pref in ["tsx", "jsx", "auto"]:
            return f'''import React from 'react';

interface {name}Props {{
  className?: string;
  children?: React.ReactNode;
}}

export default function {name}({{ className, children }}: {name}Props) {{
  return (
    <div className={{className}}>
      {{{component.description or f"{name} component"}}}
      {{children}}
    </div>
  );
}}'''
        elif format_pref == "vue":
            return f'''<template>
  <div :class="className">
    {component.description or f"{name} component"}
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {{
  className?: string;
}}

defineProps<Props>();
</script>'''
        else:
            return f'''<div class="component">
  {component.description or f"{name} component"}
</div>'''

    def _generate_ui_block(self, block_type: str, target: str, style: str) -> Dict[str, Any]:
        """Generate UI block data."""
        blocks = {
            "auth": {
                "name": "Authentication Form",
                "description": "Login/signup form with validation",
                "files": [
                    {
                        "path": "components/auth/LoginForm.tsx",
                        "content": self._get_auth_form_code(target, style)
                    }
                ],
                "dependencies": ["react-hook-form", "zod", "@hookform/resolvers"],
                "commands": [
                    f"npm install react-hook-form zod @hookform/resolvers"
                ]
            },
            "navbar": {
                "name": "Navigation Bar",
                "description": "Responsive navigation with mobile menu",
                "files": [
                    {
                        "path": "components/layout/Navbar.tsx", 
                        "content": self._get_navbar_code(target, style)
                    }
                ],
                "dependencies": ["@headlessui/react"],
                "commands": [
                    f"npm install @headlessui/react"
                ]
            },
            "hero": {
                "name": "Hero Section",
                "description": "Landing page hero with CTA",
                "files": [
                    {
                        "path": "components/sections/Hero.tsx",
                        "content": self._get_hero_code(target, style)
                    }
                ],
                "dependencies": [],
                "commands": []
            },
            "pricing": {
                "name": "Pricing Table",
                "description": "Pricing plans with feature comparison",
                "files": [
                    {
                        "path": "components/pricing/PricingTable.tsx",
                        "content": self._get_pricing_code(target, style)
                    }
                ],
                "dependencies": [],
                "commands": []
            }
        }
        
        return blocks.get(block_type, {
            "name": f"{block_type.title()} Block",
            "description": f"UI block for {block_type}",
            "files": [],
            "dependencies": [],
            "commands": []
        })

    def _get_auth_form_code(self, target: str, style: str) -> str:
        """Generate auth form code."""
        return '''import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginFormData) => {
    console.log('Login data:', data);
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-center mb-6">Sign In</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            {...register('email')}
            type="email"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
          )}
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            {...register('password')}
            type="password"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>
        
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Sign In
        </button>
      </form>
    </div>
  );
}'''

    def _get_navbar_code(self, target: str, style: str) -> str:
        """Generate navbar code."""
        return '''import React, { useState } from 'react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-gray-800">Lea</h1>
            </div>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                Home
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                Components
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                Docs
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                About
              </a>
            </div>
          </div>
          
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-blue-600 focus:outline-none focus:text-blue-600"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t">
            <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
              Home
            </a>
            <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
              Components  
            </a>
            <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
              Docs
            </a>
            <a href="#" className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium">
              About
            </a>
          </div>
        </div>
      )}
    </nav>
  );
}'''

    def _get_hero_code(self, target: str, style: str) -> str:
        """Generate hero section code."""
        return '''import React from 'react';

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-blue-600 to-purple-700 overflow-hidden">
      <div className="max-w-7xl mx-auto">
        <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div className="sm:text-center lg:text-left">
              <h1 className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
                <span className="block xl:inline">UI Components</span>{' '}
                <span className="block text-yellow-400 xl:inline">Made Simple</span>
              </h1>
              <p className="mt-3 text-base text-gray-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                Access thousands of beautiful, ready-to-use UI components from the best design systems.
                Copy, paste, and customize in seconds.
              </p>
              <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div className="rounded-md shadow">
                  <a
                    href="#"
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
                  >
                    Get Started
                  </a>
                </div>
                <div className="mt-3 sm:mt-0 sm:ml-3">
                  <a
                    href="#"
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 md:py-4 md:text-lg md:px-10"
                  >
                    Browse Components
                  </a>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}'''

    def _get_pricing_code(self, target: str, style: str) -> str:
        """Generate pricing table code."""
        return '''import React from 'react';

const plans = [
  {
    name: 'Free',
    price: '$0',
    description: 'Perfect for getting started',
    features: [
      'Access to basic components',
      'Copy & paste code',
      'Community support',
      'MIT licensed components'
    ],
    cta: 'Get Started',
    popular: false
  },
  {
    name: 'Pro',
    price: '$29',
    description: 'For professional developers',
    features: [
      'Access to all components',
      'Premium blocks & templates',
      'Priority support',
      'Commercial license',
      'Advanced customization'
    ],
    cta: 'Start Free Trial',
    popular: true
  },
  {
    name: 'Team',
    price: '$99',
    description: 'For growing teams',
    features: [
      'Everything in Pro',
      'Team collaboration',
      'Private component library',
      'Design system tools',
      'SSO integration'
    ],
    cta: 'Contact Sales',
    popular: false
  }
];

export default function PricingTable() {
  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mt-4 text-xl text-gray-600">
            Choose the plan that works for you
          </p>
        </div>
        
        <div className="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-3 sm:gap-6 lg:max-w-4xl lg:mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative p-8 bg-white border rounded-lg shadow-sm ${
                plan.popular ? 'border-blue-500 ring-2 ring-blue-500' : 'border-gray-200'
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 right-6 transform -translate-y-1/2">
                  <span className="inline-flex px-4 py-1 text-sm font-semibold text-white bg-blue-500 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="text-center">
                <h3 className="text-2xl font-semibold text-gray-900">{plan.name}</h3>
                <p className="mt-2 text-gray-500">{plan.description}</p>
                <div className="mt-4">
                  <span className="text-4xl font-extrabold text-gray-900">{plan.price}</span>
                  <span className="text-base font-medium text-gray-500">/month</span>
                </div>
              </div>
              
              <ul className="mt-8 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg className="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <p className="ml-3 text-base text-gray-700">{feature}</p>
                  </li>
                ))}
              </ul>
              
              <div className="mt-8">
                <button
                  className={`w-full py-3 px-6 border border-transparent rounded-md text-center font-medium ${
                    plan.popular
                      ? 'text-white bg-blue-600 hover:bg-blue-700'
                      : 'text-blue-600 bg-blue-50 hover:bg-blue-100'
                  }`}
                >
                  {plan.cta}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}'''

    # Backend Generation Tool Handlers
    async def _handle_project_init(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle project_init tool call."""
        result = self.backend_tools.project_init(**args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def _handle_db_schema_design(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle db_schema_design tool call."""
        result = self.backend_tools.db_schema_design(**args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def _handle_api_crud_generate(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle api_crud_generate tool call."""
        result = self.backend_tools.api_crud_generate(**args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def _handle_auth_enable(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle auth_enable tool call."""
        result = self.backend_tools.auth_enable(**args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def _handle_deploy_preset(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle deploy_preset tool call."""
        result = self.backend_tools.deploy_preset(**args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def run(self):
        """Run the MCP server."""
        await self.initialize()
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, InitializeResult(
                protocolVersion="2024-11-05",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability()
                ),
                serverInfo={
                    "name": "Lea UI Components + Backend Generator",
                    "version": "2.0.0"
                }
            ))


# Entry point for MCP server
async def main():
    """Main entry point for MCP server."""
    server = LeaMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())