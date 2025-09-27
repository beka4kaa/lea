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
def validate_jsonrpc_format(data: dict) -> Optional[dict]:
    """Validate JSON-RPC 2.0 format and return error response if invalid."""
    request_id = data.get("id")
    
    # Check for JSON-RPC 2.0 compliance
    if not data.get("jsonrpc") == "2.0":
        # Check if this looks like a REST-style request
        if "query" in data and "jsonrpc" not in data:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "PROTOCOL MISMATCH: You sent a REST request to a JSON-RPC 2.0 endpoint",
                    "data": {
                        "your_request": data,
                        "correct_format": {
                            "jsonrpc": "2.0",
                            "id": 1,
                            "method": "tools/call",
                            "params": {
                                "name": "search_component",
                                "arguments": data  # Use their original data as arguments
                            }
                        },
                        "documentation": "https://github.com/beka4kaa/lea/blob/main/MCP_AGENT_INTEGRATION.md",
                        "discovery_endpoint": "/mcp-discovery",
                        "fix": "Wrap your request in JSON-RPC 2.0 format as shown in 'correct_format'"
                    }
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: Missing 'jsonrpc': '2.0'. This is a JSON-RPC 2.0 server.",
                    "data": {
                        "expected_format": {
                            "jsonrpc": "2.0",
                            "id": 1,
                            "method": "tools/call",
                            "params": {
                                "name": "search_component", 
                                "arguments": {"query": "your_query"}
                            }
                        },
                        "documentation": "https://github.com/beka4kaa/lea/blob/main/MCP_AGENT_INTEGRATION.md",
                        "discovery_endpoint": "/mcp-discovery"
                    }
                }
            }
    
    # Check for required method field
    if "method" not in data:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32600,
                "message": "Invalid Request: Missing 'method' field",
                "data": {
                    "available_methods": ["initialize", "tools/list", "tools/call"],
                    "example": {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/list",
                        "params": {}
                    }
                }
            }
        }
    
    # Check for required id field
    if "id" not in data:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32600,
                "message": "Invalid Request: Missing 'id' field",
                "data": {
                    "note": "JSON-RPC 2.0 requires an 'id' field for correlation",
                    "example": {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/list",
                        "params": {}
                    }
                }
            }
        }
    
    return None  # No validation errors


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


@router.get("/mcp")
async def mcp_info():
    """MCP endpoint information - GET requests return usage info."""
    return {
        "endpoint": "/mcp",
        "protocol": "Model Context Protocol (MCP)",
        "version": "2024-11-05",
        "method": "POST",
        "format": "JSON-RPC 2.0",
        "description": "This endpoint accepts JSON-RPC 2.0 requests for MCP protocol communication",
        "example_request": {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        },
        "documentation": "https://github.com/beka4kaa/lea/blob/main/MCP_AGENT_INTEGRATION.md",
        "discovery": "/mcp-discovery",
        "error": "Use POST method with JSON-RPC 2.0 format for actual MCP communication"
    }

@router.post("/mcp")
async def mcp_handler(request: Request):
    """Handle MCP JSON-RPC requests with format validation."""
    try:
        data = await request.json()
        
        # First check for JSON-RPC 2.0 format compliance
        format_validation_error = validate_jsonrpc_format(data)
        if format_validation_error:
            return format_validation_error
        
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
                    "message": f"Method not found: {method}",
                    "data": {
                        "available_methods": ["initialize", "tools/list", "tools/call"],
                        "suggestions": {
                            "initialize": "Start MCP session",
                            "tools/list": "List available tools",
                            "tools/call": "Call a specific tool"
                        },
                        "example": {
                            "jsonrpc": "2.0",
                            "id": 1,
                            "method": "tools/list",
                            "params": {}
                        },
                        "documentation": "https://github.com/beka4kaa/lea/blob/main/MCP_AGENT_INTEGRATION.md"
                    }
                }
            }
    
    except json.JSONDecodeError as e:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": "Parse error: Invalid JSON",
                "data": {
                    "error_details": str(e),
                    "fix": "Ensure your request is valid JSON",
                    "example": {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/list",
                        "params": {}
                    }
                }
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": data.get("id") if "data" in locals() else None,
            "error": {
                "code": -32603,
                "message": "Internal error",
                "data": {
                    "error_details": str(e),
                    "contact": "https://github.com/beka4kaa/lea/issues",
                    "discovery": "/mcp-discovery",
                    "status": "/mcp-status"
                }
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
                # Map to GET /api/v1/components with search query
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
                
                response = await client.get(f"{base_url}/api/v1/components", params=params)
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
                return {
                    "error": f"Unknown tool: {tool_name}",
                    "available_tools": [tool["name"] for tool in TOOLS],
                    "suggestions": {
                        "list_components": "List UI components with optional filtering",
                        "search_component": "Search components by query",
                        "get_component_code": "Get component source code",
                        "get_block": "Get UI blocks (auth, pricing, etc.)",
                        "install_plan": "Get installation dependencies"
                    },
                    "documentation": "Use 'tools/list' method to see full tool schemas"
                }
        
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if hasattr(e.response, 'text') else str(e)
            return {
                "error": f"HTTP {e.response.status_code}",
                "details": error_detail,
                "tool": tool_name,
                "arguments": arguments,
                "fix": "Check tool arguments and try again",
                "status_endpoint": "/mcp-status"
            }
        except httpx.RequestError as e:
            return {
                "error": "Network error",
                "details": str(e),
                "tool": tool_name,
                "fix": "Check if server is running and accessible",
                "health_check": "/health"
            }
        except Exception as e:
            return {
                "error": "Tool execution failed",
                "details": str(e),
                "tool": tool_name,
                "arguments": arguments,
                "contact": "https://github.com/beka4kaa/lea/issues"
            }


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