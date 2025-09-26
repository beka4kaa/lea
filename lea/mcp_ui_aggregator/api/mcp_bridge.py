"""JSON-RPC to REST API bridge for MCP protocol."""

from fastapi import APIRouter, Request, HTTPException
from typing import Any, Dict, List, Optional
import json
import httpx
from datetime import datetime

from ..core.config import settings

router = APIRouter()

# Server info for MCP initialize
SERVER_INFO = {
    "name": "Lea UI Components",
    "version": "1.0.0",
    "protocolVersion": "2024-11-05"
}

# Available tools mapping to REST endpoints
TOOLS = [
    {
        "name": "list_components",
        "description": "List all available UI components with optional filtering",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "Filter by provider (magicui, shadcn, daisyui, etc.)"
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
    },
    {
        "name": "search_component",
        "description": "Search UI components by query with semantic matching",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., 'button', 'navigation menu', 'form input')"
                },
                "provider": {
                    "type": "string",
                    "description": "Filter by provider"
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
    },
    {
        "name": "get_component_code",
        "description": "Get the complete source code for a specific component",
        "inputSchema": {
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
    },
    {
        "name": "get_component_docs",
        "description": "Get documentation and usage examples for a component",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_id": {
                    "type": "string",
                    "description": "Component ID"
                }
            },
            "required": ["component_id"]
        }
    },
    {
        "name": "get_block",
        "description": "Get a ready-to-use UI block with multiple components (auth, pricing, navbar, hero)",
        "inputSchema": {
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
    },
    {
        "name": "install_plan",
        "description": "Get installation plan and dependencies for components or blocks",
        "inputSchema": {
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
    },
    {
        "name": "verify",
        "description": "Verify component code and dependencies for correctness",
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
    }
]


@router.post("/mcp")
async def mcp_handler(request: Request):
    """Handle MCP JSON-RPC requests."""
    try:
        data = await request.json()
        
        # Handle different MCP methods
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": SERVER_INFO["protocolVersion"],
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": SERVER_INFO["name"],
                        "version": SERVER_INFO["version"]
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": TOOLS
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_arguments = params.get("arguments", {})
            
            # Map tool calls to REST API endpoints
            result = await handle_tool_call(tool_name, tool_arguments)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": data.get("id") if "data" in locals() else None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }


async def handle_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tool calls by mapping to REST API endpoints."""
    base_url = f"http://localhost:{settings.port}"
    
    async with httpx.AsyncClient() as client:
        try:
            if tool_name == "list_components":
                # Map to GET /api/v1/components
                params = {}
                if arguments.get("provider"):
                    params["provider"] = arguments["provider"]
                if arguments.get("category"):
                    params["category"] = arguments["category"]
                if arguments.get("framework"):
                    params["framework"] = arguments["framework"]
                if arguments.get("limit"):
                    params["limit"] = arguments["limit"]
                if arguments.get("offset"):
                    params["offset"] = arguments["offset"]
                
                response = await client.get(f"{base_url}/api/v1/components", params=params)
                response.raise_for_status()
                return response.json()
            
            elif tool_name == "search_component":
                # Map to GET /api/v1/search
                params = {"q": arguments["query"]}
                if arguments.get("provider"):
                    params["provider"] = arguments["provider"]
                if arguments.get("category"):
                    params["category"] = arguments["category"]
                if arguments.get("framework"):
                    params["framework"] = arguments["framework"]
                if arguments.get("free_only"):
                    params["free_only"] = arguments["free_only"]
                if arguments.get("limit"):
                    params["limit"] = arguments["limit"]
                
                response = await client.get(f"{base_url}/api/v1/search", params=params)
                response.raise_for_status()
                return response.json()
            
            elif tool_name == "get_component_code":
                # Parse component_id and map to GET /api/v1/components/{provider}/{component}
                component_id = arguments["component_id"]
                
                if "/" not in component_id:
                    return {"error": "Component ID must be in format 'provider/component'"}
                
                provider, component = component_id.split("/", 1)
                
                params = {}
                if arguments.get("format"):
                    params["format"] = arguments["format"]
                
                response = await client.get(f"{base_url}/api/v1/components/{provider}/{component}", params=params)
                response.raise_for_status()
                return response.json()
            
            elif tool_name == "get_component_docs":
                # Map to GET /api/v1/components/{provider}/{component}/docs
                component_id = arguments["component_id"]
                
                if "/" not in component_id:
                    return {"error": "Component ID must be in format 'provider/component'"}
                
                provider, component = component_id.split("/", 1)
                
                response = await client.get(f"{base_url}/api/v1/components/{provider}/{component}/docs")
                response.raise_for_status()
                return response.json()
            
            elif tool_name == "get_block":
                # Map to POST /api/v1/blocks
                block_data = {
                    "block_type": arguments["block_type"],
                    "target": arguments.get("target", "nextjs"),
                    "style": arguments.get("style", "tailwind")
                }
                
                response = await client.post(f"{base_url}/api/v1/blocks", json=block_data)
                response.raise_for_status()
                return response.json()
            
            elif tool_name == "install_plan":
                # Map to POST /api/v1/install-plan
                plan_data = {
                    "component_ids": arguments["component_ids"],
                    "target": arguments.get("target", "nextjs"),
                    "package_manager": arguments.get("package_manager", "npm")
                }
                
                response = await client.post(f"{base_url}/api/v1/install-plan", json=plan_data)
                response.raise_for_status()
                return response.json()
            
            elif tool_name == "verify":
                # Map to POST /api/v1/verify
                verify_data = {
                    "code": arguments["code"],
                    "framework": arguments["framework"],
                    "check_imports": arguments.get("check_imports", True),
                    "check_syntax": arguments.get("check_syntax", True)
                }
                
                response = await client.post(f"{base_url}/api/v1/verify", json=verify_data)
                response.raise_for_status()
                return response.json()
            
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": f"Tool call failed: {str(e)}"}


# Health check for MCP endpoint
@router.get("/mcp/health")
async def mcp_health():
    """Health check for MCP endpoint."""
    return {
        "status": "healthy",
        "server_info": SERVER_INFO,
        "tools_count": len(TOOLS),
        "timestamp": datetime.utcnow().isoformat()
    }