# Lea MCP Server Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [MCP Protocol](#mcp-protocol)
4. [Available Tools](#available-tools)
5. [API Reference](#api-reference)
6. [Configuration](#configuration)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## 🎯 Overview

Lea MCP Server is a Model Context Protocol (MCP) compliant server that provides access to a comprehensive library of UI components from 11+ popular design systems. It allows AI assistants to search, retrieve, and generate UI components programmatically.

### Key Features

- **MCP 2024-11-05 Protocol** compliant
- **326+ UI Components** from 11 providers
- **7 Specialized Tools** for component operations
- **Multi-framework Support** (React, Next.js, Vue, etc.)
- **JSON-RPC 2.0** communication
- **Real-time Code Generation** with validation

### Supported Providers

| Provider | Components | Framework | Styling |
|----------|------------|-----------|---------|
| shadcn/ui | 50+ | React | Tailwind CSS |
| Magic UI | 40+ | React | Tailwind CSS |
| daisyUI | 60+ | Any | Tailwind CSS |
| React Bits | 30+ | React | CSS Modules |
| Aceternity UI | 45+ | React | Tailwind CSS |
| AlignUI | 25+ | React | Tailwind CSS |
| 21st.dev | 35+ | React | Custom CSS |
| BentoGrids | 20+ | React | Tailwind CSS |
| Next.js Design | 15+ | Next.js | Tailwind CSS |
| HyperUI | 40+ | HTML/React | Tailwind CSS |
| Tailwind Gallery | 30+ | HTML | Tailwind CSS |

## 🚀 Installation

### Prerequisites

- Python 3.8+
- FastAPI
- MCP SDK
- Virtual environment (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/beka4kaa/lea.git
cd lea

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Setup

```bash
# Build Docker image
docker build -t lea-mcp-server .

# Run container
docker run -p 8000:8000 lea-mcp-server
```

## 🔌 MCP Protocol

Lea implements the MCP 2024-11-05 specification with JSON-RPC 2.0 transport.

### Endpoint

```
POST http://localhost:8000/mcp
Content-Type: application/json
```

### Protocol Methods

#### 1. Initialize

Establishes connection and capabilities negotiation.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "Your MCP Client",
      "version": "1.0.0"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "Lea UI Components",
      "version": "1.0.0"
    }
  }
}
```

#### 2. Tools List

Retrieves available tools.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "list_components",
        "description": "List all available UI components with filters",
        "inputSchema": {
          "type": "object",
          "properties": {
            "provider": {"type": "string"},
            "category": {"type": "string"},
            "limit": {"type": "integer"}
          }
        }
      }
      // ... 6 more tools
    ]
  }
}
```

#### 3. Tool Call

Executes a specific tool.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
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

## 🛠️ Available Tools

### 1. list_components

Lists available UI components with optional filtering.

**Parameters:**
```typescript
{
  provider?: string;    // Filter by provider (e.g., "shadcn", "magic-ui")
  category?: string;    // Filter by category (e.g., "form", "navigation")
  limit?: number;       // Limit results (default: 50)
  search?: string;      // Search in name/description
}
```

**Example:**
```json
{
  "name": "list_components",
  "arguments": {
    "provider": "shadcn",
    "category": "form",
    "limit": 10
  }
}
```

**Response:**
```json
{
  "content": [{
    "type": "text",
    "text": "{\"components\": [{\"id\": \"shadcn-button\", \"name\": \"Button\", \"provider\": \"shadcn\", \"category\": \"form\", \"description\": \"Customizable button component\"}]}"
  }]
}
```

### 2. search_components

Search components by name, description, or tags.

**Parameters:**
```typescript
{
  query: string;        // Search query
  provider?: string;    // Filter by provider
  exact?: boolean;      // Exact match (default: false)
  limit?: number;       // Limit results (default: 20)
}
```

**Example:**
```json
{
  "name": "search_components",
  "arguments": {
    "query": "button gradient",
    "provider": "magic-ui",
    "limit": 5
  }
}
```

### 3. get_component_code

Retrieves the source code for a specific component.

**Parameters:**
```typescript
{
  component_id: string; // Component identifier
  framework?: string;   // Target framework (default: "react")
  typescript?: boolean; // TypeScript version (default: true)
}
```

**Example:**
```json
{
  "name": "get_component_code",
  "arguments": {
    "component_id": "shadcn-button",
    "framework": "react",
    "typescript": true
  }
}
```

**Response:**
```json
{
  "content": [{
    "type": "text", 
    "text": "{\"code\": \"import React from 'react';\\n\\ninterface ButtonProps {\\n  children: React.ReactNode;\\n  onClick?: () => void;\\n}\\n\\nexport const Button: React.FC<ButtonProps> = ({ children, onClick }) => {\\n  return (\\n    <button className='px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600' onClick={onClick}>\\n      {children}\\n    </button>\\n  );\\n};\", \"dependencies\": [\"react\"], \"file_name\": \"Button.tsx\"}"
  }]
}
```

### 4. get_component_docs

Retrieves documentation for a component.

**Parameters:**
```typescript
{
  component_id: string; // Component identifier
  format?: string;      // Documentation format ("markdown" | "json")
}
```

**Example:**
```json
{
  "name": "get_component_docs",
  "arguments": {
    "component_id": "shadcn-dialog",
    "format": "markdown"
  }
}
```

### 5. get_block

Generates complete UI blocks (multiple components working together).

**Parameters:**
```typescript
{
  block_type: string;   // "auth" | "navbar" | "hero" | "pricing" | "dashboard"
  target: string;       // Target framework ("nextjs" | "react" | "vue")
  style?: string;       // Styling approach ("tailwind" | "styled" | "css")
  theme?: string;       // Theme variant ("light" | "dark" | "auto")
}
```

**Example:**
```json
{
  "name": "get_block",
  "arguments": {
    "block_type": "auth",
    "target": "nextjs", 
    "style": "tailwind",
    "theme": "dark"
  }
}
```

**Response:**
```json
{
  "content": [{
    "type": "text",
    "text": "{\"name\": \"Authentication Form\", \"description\": \"Complete login/signup form with validation\", \"files\": [{\"path\": \"components/AuthForm.tsx\", \"content\": \"'use client';\\nimport React, { useState } from 'react';\\n// ... complete component code\"}], \"dependencies\": [\"react-hook-form\", \"zod\"], \"instructions\": \"Copy the file to your components directory and install dependencies\"}"
  }]
}
```

### 6. install_plan

Generates installation and setup instructions for components.

**Parameters:**
```typescript
{
  component_ids: string[];  // Array of component IDs 
  target: string;           // Target framework
  package_manager?: string; // "npm" | "yarn" | "pnpm"
}
```

**Example:**
```json
{
  "name": "install_plan",
  "arguments": {
    "component_ids": ["shadcn-button", "shadcn-input"],
    "target": "nextjs",
    "package_manager": "npm"
  }
}
```

**Response:**
```json
{
  "content": [{
    "type": "text",
    "text": "{\"runtime_dependencies\": [\"react\", \"@radix-ui/react-slot\"], \"dev_dependencies\": [\"@types/react\"], \"commands\": [\"npm install react @radix-ui/react-slot\", \"npm install -D @types/react\"], \"setup_steps\": [\"1. Install dependencies\", \"2. Copy component files\", \"3. Update tailwind.config.js\"]}"
  }]
}
```

### 7. verify

Validates component code for syntax and compatibility issues.

**Parameters:**
```typescript
{
  code: string;            // Component code to validate
  framework: string;       // Target framework  
  check_imports?: boolean; // Validate imports (default: true)
  check_syntax?: boolean;  // Validate syntax (default: true)
}
```

**Example:**
```json
{
  "name": "verify",
  "arguments": {
    "code": "import React from 'react'; export const Button = () => <button>Click me</button>;",
    "framework": "react",
    "check_imports": true,
    "check_syntax": true
  }
}
```

## 🔧 Configuration

### Environment Variables

```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0
RELOAD=true

# Database (Future)
DATABASE_URL=postgresql://user:pass@localhost/lea

# Cache (Future)  
REDIS_URL=redis://localhost:6379

# Rate Limiting (Future)
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Server Settings

Create `config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Lea MCP Server"
    version: str = "1.0.0"
    debug: bool = True
    
    # MCP Configuration
    mcp_protocol_version: str = "2024-11-05"
    max_components_per_request: int = 50
    
    # Component Settings
    default_framework: str = "react"
    default_styling: str = "tailwind"
    enable_typescript: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 💡 Examples

### Basic MCP Client Integration

```python
import httpx
import json

class LeaMCPClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = httpx.AsyncClient()
        
    async def initialize(self):
        response = await self.session.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "Python Client", "version": "1.0.0"}
                }
            }
        )
        return response.json()
    
    async def get_components(self, provider: str = None):
        response = await self.session.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0", 
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "list_components",
                    "arguments": {"provider": provider, "limit": 20}
                }
            }
        )
        return response.json()
    
    async def generate_auth_form(self):
        response = await self.session.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 3, 
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
        )
        return response.json()

# Usage
async def main():
    client = LeaMCPClient()
    
    # Initialize connection
    init_result = await client.initialize()
    print("Connected:", init_result["result"]["serverInfo"]["name"])
    
    # Get components
    components = await client.get_components("shadcn")
    print("Found components:", len(components))
    
    # Generate auth form
    auth_form = await client.generate_auth_form()
    form_data = json.loads(auth_form["result"]["content"][0]["text"])
    print("Generated:", form_data["name"])
```

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lea-ui": {
      "command": "python",
      "args": ["-m", "uvicorn", "mcp_ui_aggregator.api.app:app", "--port", "8000"],
      "env": {
        "PYTHONPATH": "/path/to/lea"
      }
    }
  }
}
```

### Cursor IDE Integration

```json
{
  "mcp": {
    "servers": {
      "lea": {
        "url": "http://localhost:8000/mcp",
        "name": "Lea UI Components",
        "description": "Access to 326+ UI components"
      }
    }
  }
}
```

## 🔄 REST API Fallback

In addition to MCP protocol, the server provides REST endpoints:

```bash
# Health check
GET /health

# List providers
GET /api/v1/providers

# Search components  
GET /api/v1/components/search?q=button&provider=shadcn

# Get component
GET /api/v1/components/{component_id}

# Generate blocks
POST /api/v1/blocks
{
  "block_type": "hero",
  "target": "react",
  "style": "tailwind"
}

# OpenAPI documentation
GET /docs
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Server Not Starting

```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep fastapi
pip list | grep mcp

# Check port availability
lsof -i :8000
```

#### 2. MCP Connection Issues

```bash
# Test MCP endpoint
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

#### 3. Component Not Found

```json
// Check available providers
{
  "method": "tools/call",
  "params": {
    "name": "list_components", 
    "arguments": {"limit": 5}
  }
}
```

#### 4. Import Errors

```python
# Make sure PYTHONPATH includes project root
export PYTHONPATH="${PYTHONPATH}:/path/to/lea"

# Or use absolute imports
from mcp_ui_aggregator.api.app import app
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Start server with debug
uvicorn mcp_ui_aggregator.api.app:app --reload --log-level debug
```

### Performance Monitoring

```bash
# Monitor server performance
pip install uvicorn[standard]

# Enable access logs
uvicorn app:app --access-log

# Monitor with htop/top
htop
```

## 📚 Additional Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Lea GitHub Repository](https://github.com/beka4kaa/lea)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Lea MCP Server v1.0.0** - Built with ❤️ for the AI development community