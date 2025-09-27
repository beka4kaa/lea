"""MCP Discovery endpoints for agent integration."""

from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime

router = APIRouter()

# Complete MCP Tools specification for AI agents
MCP_TOOLS_SPEC = [
    {
        "name": "list_components",
        "description": "List all available UI components from 11 providers (MagicUI, Shadcn, DaisyUI, etc.) with optional filtering by provider, category, framework, and pagination",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "Filter by provider",
                    "enum": ["magicui", "shadcn", "daisyui", "reactbits", "tremor", "nextui", "chakra", "mantine", "antd", "arco", "semi"]
                },
                "category": {
                    "type": "string", 
                    "description": "Filter by component category",
                    "enum": ["animated", "forms", "navigation", "buttons", "inputs", "layouts", "data_display", "feedback", "overlays", "text", "backgrounds", "cards", "other"]
                },
                "framework": {
                    "type": "string",
                    "description": "Filter by framework compatibility",
                    "enum": ["react", "vue", "svelte", "angular", "next", "nuxt"]
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of components to return (1-100)",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 20
                },
                "offset": {
                    "type": "integer", 
                    "description": "Number of components to skip for pagination",
                    "minimum": 0,
                    "default": 0
                }
            }
        },
        "examples": [
            {"provider": "magicui", "limit": 10},
            {"category": "animated", "framework": "react"},
            {"limit": 5, "offset": 0}
        ]
    },
    {
        "name": "search_component",
        "description": "Search UI components using semantic matching across all 66 components. Use natural language queries like 'beautiful animated button', 'contact form with validation', 'image gallery with lightbox'",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language search query (e.g., 'animated button', 'contact form', 'image gallery', 'loading spinner')"
                },
                "provider": {
                    "type": "string",
                    "description": "Filter by specific provider",
                    "enum": ["magicui", "shadcn", "daisyui", "reactbits", "tremor", "nextui", "chakra", "mantine", "antd", "arco", "semi"]
                },
                "category": {
                    "type": "string",
                    "description": "Filter by category",
                    "enum": ["animated", "forms", "navigation", "buttons", "inputs", "layouts", "data_display", "feedback", "overlays", "text", "backgrounds", "cards", "other"]
                },
                "framework": {
                    "type": "string", 
                    "description": "Target framework for compatibility",
                    "enum": ["react", "vue", "svelte", "angular", "next", "nuxt"]
                },
                "free_only": {
                    "type": "boolean",
                    "description": "Only return free components (excludes paid/pro components)",
                    "default": False
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return (1-50)",
                    "minimum": 1,
                    "maximum": 50,
                    "default": 10
                }
            },
            "required": ["query"]
        },
        "examples": [
            {"query": "animated button with hover effects", "limit": 5},
            {"query": "contact form validation", "provider": "magicui"},
            {"query": "image gallery lightbox", "framework": "react"}
        ]
    },
    {
        "name": "get_component_code",
        "description": "Get complete production-ready source code for any component. Returns TSX/JSX code with TypeScript interfaces, proper imports, styling, and animations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_id": {
                    "type": "string",
                    "description": "Component ID in format 'provider/slug' (e.g., 'shadcn/button', 'magicui/contact-form', 'magicui/calculator')",
                    "pattern": "^[a-z]+/[a-z-]+$"
                },
                "format": {
                    "type": "string", 
                    "description": "Preferred code format",
                    "enum": ["tsx", "jsx", "vue", "svelte", "html", "auto"],
                    "default": "auto"
                }
            },
            "required": ["component_id"]
        },
        "examples": [
            {"component_id": "shadcn/button"},
            {"component_id": "magicui/contact-form", "format": "tsx"},
            {"component_id": "magicui/calculator"}
        ]
    },
    {
        "name": "get_component_docs",
        "description": "Get comprehensive documentation, usage examples, installation instructions, and dependencies for any component",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_id": {
                    "type": "string",
                    "description": "Component ID in format 'provider/slug'",
                    "pattern": "^[a-z]+/[a-z-]+$"
                }
            },
            "required": ["component_id"]
        },
        "examples": [
            {"component_id": "shadcn/button"},
            {"component_id": "magicui/tooltip"}
        ]
    },
    {
        "name": "get_block",
        "description": "Get complete UI blocks (multi-component layouts) like authentication pages, pricing sections, hero sections, navigation bars, footers, and dashboards",
        "inputSchema": {
            "type": "object", 
            "properties": {
                "block_type": {
                    "type": "string",
                    "description": "Type of UI block to generate",
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
        },
        "examples": [
            {"block_type": "pricing", "target": "nextjs"},
            {"block_type": "hero", "style": "tailwind"},
            {"block_type": "auth"}
        ]
    },
    {
        "name": "install_plan",
        "description": "Generate complete installation plan with all dependencies, commands, and setup steps for selected components",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of component IDs to install (e.g., ['shadcn/button', 'magicui/contact-form'])",
                    "minItems": 1
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
        },
        "examples": [
            {"component_ids": ["shadcn/button", "shadcn/input"], "package_manager": "npm"},
            {"component_ids": ["magicui/contact-form"], "target": "nextjs"}
        ]
    },
    {
        "name": "verify",
        "description": "Verify component code for syntax errors, import issues, and framework compatibility",
        "inputSchema": {
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
                    "description": "Check import statements for validity",
                    "default": True
                },
                "check_syntax": {
                    "type": "boolean", 
                    "description": "Check syntax validity",
                    "default": True
                }
            },
            "required": ["code", "framework"]
        },
        "examples": [
            {"code": "import React from 'react'...", "framework": "react"},
            {"code": "export default function Button()...", "framework": "nextjs", "check_imports": True}
        ]
    }
]

@router.get("/mcp-discovery")
async def mcp_discovery():
    """MCP protocol discovery endpoint for AI agents - provides complete server capabilities and usage examples."""
    return {
        "protocol": "MCP 2024-11-05",
        "transport": "JSON-RPC 2.0",
        "endpoint": "/mcp",
        "server_info": {
            "name": "Lea UI Components",
            "version": "1.0.0",
            "description": "Comprehensive UI component aggregator with 66 components from 11 providers including MagicUI, Shadcn, DaisyUI, ReactBits, Tremor, NextUI, Chakra, Mantine, Ant Design, Arco, and Semi Design",
            "components_count": 66,
            "providers_count": 11,
            "enhanced_features": [
                "Enhanced template system with production-ready TSX code",
                "Interactive components (forms, modals, galleries, calculators)",
                "Comprehensive search and filtering",
                "Complete installation plans",
                "Multi-framework support"
            ]
        },
        "capabilities": {
            "tools": [tool["name"] for tool in MCP_TOOLS_SPEC],
            "providers": ["magicui", "shadcn", "daisyui", "reactbits", "tremor", "nextui", "chakra", "mantine", "antd", "arco", "semi"],
            "frameworks": ["react", "vue", "svelte", "angular", "next", "nuxt"],
            "categories": ["animated", "forms", "navigation", "buttons", "inputs", "layouts", "data_display", "feedback", "overlays", "text", "backgrounds", "cards", "other"]
        },
        "tools": MCP_TOOLS_SPEC,
        "example_workflows": {
            "find_button_components": [
                {
                    "step": 1,
                    "description": "Search for button components",
                    "request": {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {
                            "name": "search_component",
                            "arguments": {"query": "animated button hover effects", "limit": 5}
                        }
                    }
                },
                {
                    "step": 2,
                    "description": "Get code for selected button",
                    "request": {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/call",
                        "params": {
                            "name": "get_component_code",
                            "arguments": {"component_id": "magicui/magic-button"}
                        }
                    }
                }
            ],
            "create_contact_form": [
                {
                    "step": 1,
                    "description": "Find contact form component",
                    "request": {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {
                            "name": "search_component",
                            "arguments": {"query": "contact form validation", "provider": "magicui"}
                        }
                    }
                },
                {
                    "step": 2,
                    "description": "Get complete form code",
                    "request": {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/call",
                        "params": {
                            "name": "get_component_code",
                            "arguments": {"component_id": "magicui/contact-form"}
                        }
                    }
                },
                {
                    "step": 3,
                    "description": "Get installation plan",
                    "request": {
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "tools/call",
                        "params": {
                            "name": "install_plan",
                            "arguments": {"component_ids": ["magicui/contact-form"]}
                        }
                    }
                }
            ]
        },
        "quick_start": {
            "initialize": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize", 
                "params": {"protocolVersion": "2024-11-05"}
            },
            "list_tools": {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            },
            "search_components": {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search_component",
                    "arguments": {"query": "your search here", "limit": 10}
                }
            }
        },
        "documentation": "https://github.com/beka4kaa/lea/blob/main/MCP_AGENT_INTEGRATION.md",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/openapi-mcp.json")
async def get_mcp_openapi():
    """OpenAPI schema for MCP protocol endpoints."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Lea MCP Server",
            "version": "1.0.0",
            "description": "JSON-RPC 2.0 MCP Server for UI Components",
            "x-protocol": "MCP JSON-RPC 2.0"
        },
        "servers": [
            {
                "url": "/mcp",
                "description": "MCP JSON-RPC 2.0 endpoint"
            }
        ],
        "paths": {
            "/mcp": {
                "post": {
                    "summary": "MCP JSON-RPC 2.0 endpoint",
                    "description": "All MCP requests must use JSON-RPC 2.0 format",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "jsonrpc": {"type": "string", "enum": ["2.0"]},
                                        "id": {"type": "integer"},
                                        "method": {"type": "string"},
                                        "params": {"type": "object"}
                                    },
                                    "required": ["jsonrpc", "id", "method"]
                                },
                                "examples": {
                                    "initialize": {
                                        "summary": "Initialize MCP connection",
                                        "value": {
                                            "jsonrpc": "2.0",
                                            "id": 1,
                                            "method": "initialize",
                                            "params": {"protocolVersion": "2024-11-05"}
                                        }
                                    },
                                    "list_tools": {
                                        "summary": "List available tools",
                                        "value": {
                                            "jsonrpc": "2.0",
                                            "id": 2,
                                            "method": "tools/list",
                                            "params": {}
                                        }
                                    },
                                    "search_components": {
                                        "summary": "Search for components",
                                        "value": {
                                            "jsonrpc": "2.0",
                                            "id": 3,
                                            "method": "tools/call",
                                            "params": {
                                                "name": "search_component",
                                                "arguments": {"query": "button", "limit": 10}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "JSON-RPC 2.0 response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "jsonrpc": {"type": "string", "enum": ["2.0"]},
                                            "id": {"type": "integer"},
                                            "result": {"type": "object"},
                                            "error": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "JsonRpcRequest": {
                    "type": "object",
                    "required": ["jsonrpc", "id", "method"],
                    "properties": {
                        "jsonrpc": {"type": "string", "enum": ["2.0"]},
                        "id": {"type": "integer"},
                        "method": {"type": "string"},
                        "params": {"type": "object"}
                    }
                }
            }
        }
    }


@router.get("/mcp-tools-manifest.json")
async def get_mcp_tools_manifest():
    """Standard MCP tools manifest for automatic agent discovery."""
    import json
    import os
    
    # Read the manifest file
    manifest_path = os.path.join(os.path.dirname(__file__), "..", "..", "mcp-tools-manifest.json")
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest
    except FileNotFoundError:
        # Fallback inline manifest
        return {
            "mcpVersion": "2024-11-05",
            "server": {
                "name": "lea-ui-components",
                "version": "1.0.0",
                "description": "LEA UI Components MCP Server - 66 production-ready components from 11 providers"
            },
            "tools": [tool["name"] for tool in MCP_TOOLS_SPEC],
            "capabilities": {
                "total_components": 66,
                "providers": 11,
                "enhanced_features": [
                    "Production-ready TSX code with TypeScript interfaces",
                    "Interactive components (forms, modals, galleries, calculators)",
                    "Enhanced template system for consistent code quality"
                ]
            }
        }


@router.get("/mcp-status")
async def mcp_status():
    """Current MCP server status and statistics."""
    return {
        "status": "active",
        "protocol_version": "2024-11-05",
        "server": {
            "name": "Lea UI Components",
            "version": "1.0.0"
        },
        "providers": {
            "total": 11,
            "active": ["magicui", "shadcn", "daisyui", "reactbits", "tremor", "nextui", "chakra", "mantine", "antd", "arco", "semi"]
        },
        "tools": {
            "available": 7,
            "names": ["list_components", "search_component", "get_component_code", "get_component_docs", "get_block", "install_plan", "verify"]
        },
        "endpoints": {
            "mcp": "/mcp",
            "discovery": "/mcp-discovery", 
            "tools_manifest": "/mcp-tools-manifest.json",
            "openapi": "/openapi-mcp.json",
            "status": "/mcp-status",
            "health": "/health"
        },
        "timestamp": datetime.utcnow().isoformat()
    }