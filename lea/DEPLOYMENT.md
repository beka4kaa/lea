# Deployment Guide for Lea MCP Server

## 🚀 Production Deployment Options

### 1. Railway (Recommended)
Railway automatically detects Python apps and uses Nixpacks for building.

**Files needed:**
- `requirements.txt` - Python dependencies
- `Procfile` - Start command
- `start.sh` - Startup script
- `runtime.txt` - Python version
- `railway.json` - Railway config (optional)
- `nixpacks.toml` - Build config (optional)

**Environment Variables:**
```bash
PORT=8000
HOST=0.0.0.0
DEBUG=false
LOG_LEVEL=info
DATABASE_URL=sqlite+aiosqlite:///./mcp_ui_aggregator.db
```

### 2. Heroku
```bash
# Deploy to Heroku
heroku create lea-mcp-server
heroku config:set DEBUG=false
heroku config:set LOG_LEVEL=info
git push heroku main
```

### 3. Docker
```bash
# Build and run with Docker
docker build -t lea-mcp-server .
docker run -p 8000:8000 -e DEBUG=false lea-mcp-server
```

### 4. DigitalOcean App Platform
```yaml
# .do/app.yaml
name: lea-mcp-server
services:
- name: web
  source_dir: /
  github:
    repo: beka4kaa/lea
    branch: main
  run_command: ./start.sh
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8000
  health_check:
    http_path: /health
  envs:
  - key: DEBUG
    value: "false"
  - key: LOG_LEVEL
    value: "info"
```

## 🔧 Configuration

### Environment Variables
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `DEBUG` - Debug mode (default: false for production)
- `LOG_LEVEL` - Logging level (info, warning, error)
- `DATABASE_URL` - Database connection string
- `WORKERS` - Number of worker processes (default: 1)

### Health Check
The server provides a health check endpoint at `/health`:
```json
{
  "status": "healthy",
  "server": "mcp-ui-aggregator",
  "version": "0.1.0",
  "database": "connected"
}
```

## 🏃‍♂️ Quick Start

1. **Clone and configure:**
   ```bash
   git clone https://github.com/beka4kaa/lea.git
   cd lea
   cp .env.example .env
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database:**
   ```bash
   python init_db.py
   ```

4. **Start server:**
   ```bash
   ./start.sh
   ```

## 📊 Monitoring

### Logs
The application logs to stdout in production. Configure your hosting platform to capture and store logs.

### Metrics
- Health check: `GET /health`
- Server info: `GET /`
- API stats: `GET /api/v1/stats`

### Database
SQLite database is created automatically and stored as `mcp_ui_aggregator.db`.
For production with high load, consider PostgreSQL.

## 🔒 Security

### CORS
CORS is configured to allow all origins for development.
For production, update the allowed origins in `app.py`:

```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

### HTTPS
Ensure your hosting platform provides HTTPS. Most modern platforms do this automatically.