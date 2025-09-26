# 🚀 Quick Deploy to Railway

## Automatic Deploy Button
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/lea-mcp-server)

## Manual Deploy Steps

1. **Fork this repository** to your GitHub account

2. **Connect to Railway:**
   - Go to [Railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked `lea` repository

3. **Configure Environment (Optional):**
   ```
   DEBUG=false
   LOG_LEVEL=info
   ```

4. **Deploy:**
   - Railway will automatically detect Python and deploy
   - Build time: ~2-3 minutes
   - Your MCP server will be available at: `https://your-app.railway.app`

## Verify Deployment

Check these endpoints:
- **Health Check:** `https://your-app.railway.app/health`
- **MCP Protocol:** `https://your-app.railway.app/mcp`
- **API Docs:** `https://your-app.railway.app/docs`

## Use with Claude Desktop

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "lea-ui-components": {
      "command": "curl",
      "args": ["-X", "POST", "https://your-app.railway.app/mcp", "-H", "Content-Type: application/json"]
    }
  }
}
```

## Success! 🎯

Your MCP server is now running in production with:
- ✅ 326+ UI components from 11 design systems
- ✅ 7 specialized MCP tools
- ✅ Automatic database initialization
- ✅ Health monitoring
- ✅ Production logging

**Next Steps:**
- Test MCP tools in Claude Desktop
- Explore component search and generation
- Build amazing UIs faster! 🎨