# MCP Agent Integration Guide

## Overview

The Lea UI Components server implements the **Model Context Protocol (MCP) 2024-11-05** using **JSON-RPC 2.0** transport. This guide helps AI agents integrate successfully with the server.

## 🔍 Discovery Endpoints

### GET /mcp-discovery
Returns complete integration information for agents:

```bash
curl http://localhost:8000/mcp-discovery
```

**Response includes:**
- Protocol version and transport
- Available tools and capabilities
- Complete example requests
- Documentation links

### GET /mcp-status
Returns current server status and statistics:

```bash
curl http://localhost:8000/mcp-status
```

### GET /openapi-mcp.json
Returns OpenAPI 3.0 schema for the MCP endpoints:

```bash
curl http://localhost:8000/openapi-mcp.json
```

## 📋 JSON-RPC 2.0 Format

**All MCP requests MUST use JSON-RPC 2.0 format:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": {}
}
```

### Required Fields
- `jsonrpc`: Must be `"2.0"`
- `id`: Integer for request correlation
- `method`: Method name (see below)
- `params`: Parameters object (can be empty)

## 🔧 Available Methods

### 1. initialize
Start MCP session:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {"protocolVersion": "2024-11-05"}
}
```

### 2. tools/list
List all available tools:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

### 3. tools/call
Call a specific tool:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {}
  }
}
```

## 🛠️ Available Tools

### list_components
List UI components with optional filtering:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_components",
    "arguments": {
      "provider": "shadcn",
      "category": "buttons",
      "limit": 10
    }
  }
}
```

### search_component
Search components by query:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_component",
    "arguments": {
      "query": "button beautiful modern",
      "limit": 5
    }
  }
}
```

### get_component_code
Get component source code:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_component_code",
    "arguments": {
      "component_id": "shadcn/button",
      "format": "tsx"
    }
  }
}
```

### get_component_docs
Get component documentation:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "get_component_docs",
    "arguments": {
      "component_id": "shadcn/button"
    }
  }
}
```

### get_block
Get UI blocks (auth, pricing, etc.):

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "get_block",
    "arguments": {
      "block_type": "auth",
      "target": "nextjs",
      "style": "tailwind"
    }
  }
}
```

### install_plan
Get installation dependencies:

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "install_plan",
    "arguments": {
      "component_ids": ["shadcn/button", "magicui/animated-beam"],
      "target": "nextjs",
      "package_manager": "npm"
    }
  }
}
```

### verify
Verify component code:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "verify",
    "arguments": {
      "code": "export const Button = () => <button>Click me</button>",
      "framework": "react"
    }
  }
}
```

## ❌ Error Handling

The server provides helpful error messages for common mistakes:

### REST-style Request (Wrong!)
```json
{"query": "button", "limit": 10}
```

**Server Response:**
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "error": {
    "code": -32600,
    "message": "PROTOCOL MISMATCH: You sent a REST request to a JSON-RPC 2.0 endpoint",
    "data": {
      "correct_format": {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
          "name": "search_component",
          "arguments": {"query": "button", "limit": 10}
        }
      },
      "fix": "Wrap your request in JSON-RPC 2.0 format as shown in 'correct_format'"
    }
  }
}
```

### Missing Required Fields
The server validates all required JSON-RPC 2.0 fields and provides helpful error messages with examples.

### Unknown Methods/Tools
The server lists available methods and tools when unknown ones are requested.

## 🎯 Quick Integration

1. **Discovery**: Start with `GET /mcp-discovery` to get examples
2. **Initialize**: Call `initialize` method to start session
3. **List Tools**: Call `tools/list` to see available capabilities
4. **Use Tools**: Call `tools/call` with appropriate tool name and arguments

## 📚 Example Agent Code

### Python Example
```python
import requests

def call_mcp_server(method, params=None):
    url = "http://localhost:8000/mcp"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    response = requests.post(url, json=payload)
    return response.json()

# Initialize session
result = call_mcp_server("initialize", {"protocolVersion": "2024-11-05"})

# List available tools
tools = call_mcp_server("tools/list")

# Search for button components
search_result = call_mcp_server("tools/call", {
    "name": "search_component",
    "arguments": {"query": "button beautiful", "limit": 5}
})
```

### JavaScript Example
```javascript
async function callMcpServer(method, params = {}) {
  const response = await fetch('http://localhost:8000/mcp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method,
      params
    })
  });
  return response.json();
}

// Search for components
const result = await callMcpServer('tools/call', {
  name: 'search_component',
  arguments: { query: 'button modern', limit: 10 }
});
```

## 🔗 Additional Resources

- **Server Repository**: https://github.com/beka4kaa/lea
- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **Issue Tracker**: https://github.com/beka4kaa/lea/issues

## 🎉 Success Criteria

Your integration is successful when:
- ✅ All requests use JSON-RPC 2.0 format
- ✅ You receive structured responses with `result` or `error`
- ✅ Tool calls return component data in `result.content[0].text`
- ✅ Error messages guide you to correct format when needed

---

**Happy coding! 🚀**