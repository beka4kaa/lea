# LEA UI Components MCP Server 🎨✨

> **A comprehensive Model Context Protocol (MCP) server providing 66 production-ready UI components from 11 providers with AI agent auto-discovery**

## 🤖 AI Agent Integration

**LEA UI Components MCP Server is designed for automatic discovery by AI agents!**

### Quick Start for AI Agents

1. **Auto-Discovery**: `GET /mcp-discovery` - Complete server capabilities
2. **Tools Manifest**: `GET /mcp-tools-manifest.json` - Standard MCP specification  
3. **Documentation**: [Complete AI Agent Guide](./MCP_AI_AGENT_GUIDE.md)

### Example Usage in AI Agents
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call", 
  "params": {
    "name": "search_component",
    "arguments": {
      "query": "animated button with hover effects",
      "limit": 5
    }
  }
}
```

**Available Tools for AI Agents:**
- `search_component` - Natural language component search
- `get_component_code` - Production-ready TSX/JSX code
- `list_components` - Browse all 66 components  
- `get_component_docs` - Installation & usage docs
- `get_block` - Complete UI blocks (auth, pricing, etc.)
- `install_plan` - Dependency management
- `verify` - Code validation

[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue.svg)](https://spec.modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Quick Start

```bash
# Clone and setup
git clone https://github.com/beka4kaa/lea.git
cd lea

# Install and run
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn mcp_ui_aggregator.api.app:app --reload --port 8000
```

**MCP Server ready at:** `http://localhost:8000/mcp` 🚀

## 🎯 Core Features

### 📦 Component Library (326+ Components)
- **shadcn/ui** - Modern React components with Tailwind CSS
- **Magic UI** - Animated components for modern web apps  
- **daisyUI** - Semantic component classes for Tailwind
- **React Bits** - Copy-paste React components
- **Aceternity UI** - Beautiful animated components
- **AlignUI** - Professional UI components
- **21st.dev** - Modern component library
- **BentoGrids** - Grid layout components
- **Next.js Design** - Official Next.js components
- **HyperUI** - Tailwind CSS components
- **Tailwind Gallery** - Community components

### 🔧 MCP Tools (7 Specialized Functions)
1. **`list_components`** - Browse all available components
2. **`search_components`** - Semantic search with AI
3. **`get_component_code`** - Retrieve ready-to-use code
4. **`get_component_docs`** - Complete documentation
5. **`get_block`** - Generate complete page sections
6. **`install_plan`** - Dependency installation guide
7. **`verify`** - Component compatibility check

### 🎨 Block Generators (Ready-Made Sections)
- **Authentication** - Login/signup forms
- **Navigation** - Headers, sidebars, breadcrumbs
- **Hero Sections** - Landing page headers
- **Pricing** - Subscription plans and pricing tables

## 🚀 Installation & Setup

### 1. Environment Setup
```bash
git clone https://github.com/beka4kaa/lea.git
cd lea
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Initialization
```bash
# Initialize database and load components
python -m mcp_ui_aggregator.data.demo_seed
```

### 3. Start MCP Server
```bash
# Production mode
python -m uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port 8000

# Development mode
python -m uvicorn mcp_ui_aggregator.api.app:app --reload --port 8000
```

### 4. Verify Installation
```bash
# Test MCP protocol
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'

# Expected response: {"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05", ...}}
```

## 🔌 MCP Client Integration

### Claude Desktop Configuration
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "lea-ui-components": {
      "command": "python",
      "args": ["-m", "uvicorn", "mcp_ui_aggregator.api.app:app", "--host", "localhost", "--port", "8000"],
      "cwd": "/path/to/lea"
    }
  }
}
```

### VS Code MCP Extension
```json
{
  "mcp.servers": [
    {
      "name": "Lea UI Components",
      "command": ["python", "-m", "uvicorn", "mcp_ui_aggregator.api.app:app", "--port", "8000"],
      "cwd": "/path/to/lea"
    }
  ]
}
## 📖 Usage Examples

### Basic Component Search
```python
# Search for button components
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_components",
    "arguments": {"query": "button primary", "provider": "shadcn"}
  }
}
```

### Generate Complete Page Section
```python
# Generate hero section
{
  "jsonrpc": "2.0", 
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_block",
    "arguments": {
      "type": "hero",
      "style": "modern",
      "props": {
        "title": "Welcome to Our App",
        "subtitle": "Build faster with pre-made components"
      }
    }
  }
}
```

### Next.js Demo Application
```bash
# Try the working demo
cd examples/nextjs-demo
npm install
npm run dev
# Visit http://localhost:3000
```

## 📚 Documentation

- **[📖 MCP Server API Reference](MCP_SERVER_DOCS.md)** - Complete MCP tools documentation
- **[🏗️ Technical Architecture](TECHNICAL_ARCHITECTURE.md)** - System design and implementation
- **[🧪 Testing Guide](tests/)** - Unit and integration tests

## 🛠️ Development

### Running Tests
```bash
# Unit tests
python -m pytest tests/unit/ -v

# Integration tests
python -m pytest tests/ -v

# Smoke test
python validate_mvp.py
```

### Adding New Component Libraries
1. Create new ingestion module in `mcp_ui_aggregator/ingestion/`
2. Implement `BaseIngestionModule` interface
3. Add to component registry
4. Run ingestion: `python load_new_modules.py`

## 🚀 Production Roadmap

### Phase 1: Infrastructure (Current) ✅
- [x] MCP server with 7 specialized tools
- [x] 326+ components from 11 providers
- [x] Next.js demo application  
- [x] Comprehensive documentation

### Phase 2: Scale & Performance 🔄
- [ ] PostgreSQL migration
- [ ] Redis caching layer
- [ ] Rate limiting & API keys
- [ ] Horizontal scaling

### Phase 3: Enterprise Features 📋
- [ ] JWT authentication
- [ ] Role-based access control
- [ ] Usage analytics & monitoring
- [ ] CI/CD pipeline

### Phase 4: Developer Experience 🛠️
- [ ] TypeScript SDK generation
- [ ] Python client library  
- [ ] OpenAPI specification
- [ ] Interactive documentation

### Phase 5: Go-to-Market 🎯
- [ ] Component marketplace
- [ ] Premium templates
- [ ] SaaS deployment
- [ ] Enterprise licensing

## 🤝 Contributing

```bash
# Setup development environment
git clone https://github.com/beka4kaa/lea.git
cd lea
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests before contributing
python -m pytest tests/ -v
python validate_mvp.py

# Submit pull request
git checkout -b feature/your-feature
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/beka4kaa/lea/issues)
- **Discord**: [Join our community](#) 
- **Documentation**: [Full docs](MCP_SERVER_DOCS.md)
- **Email**: [support@lea-ui.com](mailto:support@lea-ui.com)

---

**Made with ❤️ for the MCP ecosystem** | [⭐ Star on GitHub](https://github.com/beka4kaa/lea)

