"""MCP Discovery endpoints for agent integration."""

from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime

router = APIRouter()

@router.get("/mcp-discovery")
async def mcp_discovery():
    """MCP protocol discovery endpoint for agents."""
    return {
        "protocol": "MCP 2024-11-05",
        "transport": "JSON-RPC 2.0",
        "endpoint": "/mcp",
        "server_info": {
            "name": "Lea UI Components",
            "version": "1.0.0",
            "description": "UI component aggregator with 11 providers"
        },
        "capabilities": [
            "list_components",
            "search_component", 
            "get_component_code",
            "get_component_docs",
            "get_block",
            "install_plan",
            "verify"
        ],
        "example_requests": {
            "list_components": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "list_components",
                    "arguments": {"limit": 5}
                }
            },
            "search_components": {
                "jsonrpc": "2.0", 
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "search_component",
                    "arguments": {"query": "button beautiful modern", "limit": 5}
                }
            },
            "get_component": {
                "jsonrpc": "2.0",
                "id": 3, 
                "method": "tools/call",
                "params": {
                    "name": "get_component_code",
                    "arguments": {"component_id": "shadcn/button"}
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
            "openapi": "/openapi-mcp.json",
            "status": "/mcp-status",
            "health": "/mcp/health"
        },
        "timestamp": datetime.utcnow().isoformat()
    }