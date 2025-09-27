# MCP UI Aggregator – Usage Guide

This guide explains how to run the Lea MCP UI Components server locally or remotely, validate it with the Model Context Protocol (MCP), and connect popular MCP-compatible clients.

> **Short on time?** Jump straight to the [Quick Start Checklist](#quick-start-checklist).

---

## 1. Overview

- **Project name:** Lea – MCP UI Components Server
- **Purpose:** Expose 300+ UI components, prebuilt sections, and helper tools via the Model Context Protocol.
- **Entry point (ASGI app):** `mcp_ui_aggregator.api.app:app`
- **Default HTTP port:** `8000`
- **Health check:** `GET /health`
- **MCP endpoint:** `POST /mcp`

---

## 2. Prerequisites

- Python **3.11+** (recommended 3.11.9)
- git
- (Optional) Node.js 18+ if you want to run the Next.js demo
- An MCP-compatible client (Claude Desktop, VS Code MCP extension, MCP CLI, etc.)

---

## 3. Local Setup & Run

```bash
# Clone and enter the repo
git clone https://github.com/beka4kaa/lea.git
cd lea

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies from the root-level requirements.txt
pip install -r ../requirements.txt  # repo root has requirements

# Seed demo data (optional, but recommended)
python -m mcp_ui_aggregator.data.demo_seed

# Start the server
python -m uvicorn mcp_ui_aggregator.api.app:app --host 0.0.0.0 --port 8000
```

Once uvicorn prints `Uvicorn running on http://0.0.0.0:8000`, the server is ready.

### 3.1. Quick verification

```bash
# Health check
curl http://localhost:8000/health

# Minimal MCP handshake
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
          "protocolVersion": "2024-11-05",
          "clientInfo": {"name": "curl", "version": "1.0"},
          "capabilities": {}
        }
      }'
```

Expected response:

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05", ... }}
```

---

## 4. Available MCP Tools

All tools follow the MCP JSON-RPC 2.0 convention. Invoke them through the `/mcp` endpoint or via an MCP client. Parameters are sent inside `params.arguments`.

| Tool name | Description | Key arguments |
|-----------|-------------|---------------|
| `list_components` | Returns metadata for all available components. | `provider` *(optional)* – limit to a design system |
| `search_components` | Semantic search over the component index. | `query` *(required)*, `provider` *(optional)* |
| `get_component_code` | Fetches ready-to-use code for a component. | `component_id` *(required)* |
| `get_component_docs` | Provides documentation and usage tips. | `component_id` *(required)* |
| `get_block` | Generates full UI blocks (hero, auth forms, pricing, etc.). | `type`, `style`, `props` |
| `install_plan` | Lists npm/pnpm/yarn packages needed for a component. | `component_id` *(required)* |
| `verify` | Checks component compatibility against your stack. | `component_id`, `target_stack` |

Example request payload:

```json
{
  "jsonrpc": "2.0",
  "id": "search-1",
  "method": "tools/call",
  "params": {
    "name": "search_components",
    "arguments": {
      "query": "login form",
      "provider": "shadcn"
    }
  }
}
```

---

## 5. Connecting Clients

### 5.1 Claude Desktop (macOS)

```jsonc
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "lea-ui-components": {
      "command": "python",
      "args": [
        "-m", "uvicorn",
        "mcp_ui_aggregator.api.app:app",
        "--host", "localhost",
        "--port", "8000"
      ],
      "cwd": "/absolute/path/to/lea"
    }
  }
}
```

Restart Claude Desktop. The Lea server should appear in the MCP servers list.

### 5.2 VS Code MCP Extension

Open **Settings → Extensions → MCP Configuration** and add:

```json
{
  "mcp.servers": [
    {
      "name": "Lea UI Components",
      "command": ["python", "-m", "uvicorn", "mcp_ui_aggregator.api.app:app", "--port", "8000"],
      "cwd": "/absolute/path/to/lea"
    }
  ]
}
```

Reload VS Code. The Lea server will be available in the MCP side panel.

### 5.3 MCP CLI (open-source reference implementation)

```bash
# Install the CLI
pip install mcp-cli

# Point it at the running server
mcp-cli --url http://localhost:8000/mcp list-tools
mcp-cli --url http://localhost:8000/mcp call search_components '{"query": "button", "provider": "shadcn"}'
```

---

## 6. Production / Railway Deployment

1. Push the repository to GitHub (already configured at `https://github.com/beka4kaa/lea`).
2. Create a new Railway project from that repo.
3. **Important:** set the Railway service root directory to the repo root (`.`).
4. Ensure the following files exist at the repo root:
   - `start.sh` (executable)
   - `Procfile`
   - `requirements.txt`
   - `runtime.txt`
   - `nixpacks.toml`
5. Leave the Railway start command empty (Procfile handles it).
6. On successful deploy you should see logs similar to the local uvicorn startup. The service will publish a public URL, e.g. `https://lea-production.up.railway.app`.

### 6.1 Remote health check & MCP handshake

```bash
# Replace <railway-url>
curl https://<railway-url>/health
curl -X POST https://<railway-url>/mcp -H "Content-Type: application/json" -d '{ ... }'
```

---

## 7. Quick Start Checklist

- [ ] Python 3.11+ installed
- [ ] Repo cloned & virtual env activated
- [ ] Dependencies installed from root `requirements.txt`
- [ ] Database seeded (`python -m mcp_ui_aggregator.data.demo_seed`)
- [ ] Server running (`uvicorn mcp_ui_aggregator.api.app:app`)
- [ ] Health check returns `200`
- [ ] MCP `initialize` request returns expected payload
- [ ] Client (Claude, VS Code, CLI) successfully connected

---

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: mcp_ui_aggregator...` | Not running from repo root or missing PYTHONPATH | Use provided `start.sh` or run `export PYTHONPATH="$(pwd)"` before uvicorn |
| `422 Unprocessable Entity` for tool calls | Payload shape incorrect | Follow the JSON structures above; include `jsonrpc`, `id`, `method`, `params` |
| Railway error `Script start.sh not found` | Deployment root misconfigured | Set Railway root to repo root and ensure `start.sh` is executable |
| Railway error `Railpack could not determine how to build` | Python markers missing | Confirm `requirements.txt`, `runtime.txt`, and optional `nixpacks.toml` are present at root |

Feel free to extend this guide with additional client integrations or automation scripts. Pull requests are welcome!
