<h1 align="center">⚡ LEA Backend Performance Optimization Guide</h1>

<p align="center">
  <strong>Complete guide to running high-performance FastAPI applications with LEA MCP Server</strong>
</p>

## 🚀 Performance Features

### 1. ASGI-Compliant Middleware
- **Latency Reduction**: ASGI middleware bypasses Starlette's BaseHTTPMiddleware overhead
- **Components**: Prometheus metrics, logging, security headers, compression
- **Impact**: Up to 30% reduction in middleware processing time

### 2. Optimized JSON Responses
- **ORJSONResponse**: 2-3x faster than standard JSON serialization
- **UJSONResponse**: 2x faster alternative fallback
- **Auto-Selection**: Automatically chooses best available serializer
- **Memory Efficient**: Reduced garbage collection overhead

### 3. Production Nginx Configuration
- **Persistent Connections**: HTTP/1.1 with keepalive for 15% performance gain
- **Compression**: gzip with optimized buffer sizes
- **Rate Limiting**: DDoS protection and fair usage
- **SSL/TLS**: Modern cipher suites and HSTS

### 4. Performance Profiling & Monitoring
- **Worker Optimization**: Tests 1-3 workers with ab/wrk benchmarking
- **Resource Monitoring**: CPU, memory, and connection tracking
- **Automated Reports**: Performance comparison and recommendations

## 🏁 Quick Start

### Generate Optimized Backend
```bash
# Generate FastAPI project with performance optimizations
python -m mcp_ui_aggregator.backend_tools.generator \
  --name my_app \
  --description "High-performance API" \
  --port 8000 \
  --db postgres \
  --auth jwt \
  --queue redis \
  --monitoring prometheus \
  --performance true
```

### Launch with Performance Settings
```bash
# Development with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production with optimized workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --worker-class uvicorn.workers.UvicornWorker

# Production with Gunicorn (recommended)
gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Performance Configuration

### JSON Response Optimization
```python
from mcp_ui_aggregator.core.optimized_responses import OptimizedJSONResponse

@app.get("/api/data", response_class=OptimizedJSONResponse)
async def get_data():
    return {"large_dataset": [...]}  # Automatically uses fastest serializer
```

### ASGI Middleware Integration
```python
from mcp_ui_aggregator.core.asgi_middleware import (
    ASGIPrometheusMiddleware,
    ASGILoggingMiddleware,
    ASGISecurityHeadersMiddleware,
    ASGICompressionMiddleware
)

# Add to FastAPI app
app.add_middleware(ASGICompressionMiddleware)
app.add_middleware(ASGISecurityHeadersMiddleware)
app.add_middleware(ASGILoggingMiddleware)
app.add_middleware(ASGIPrometheusMiddleware)
```

### Nginx Production Setup
```bash
# Copy optimized config
cp nginx.conf /etc/nginx/sites-available/my_app
ln -s /etc/nginx/sites-available/my_app /etc/nginx/sites-enabled/

# Test and reload
nginx -t && systemctl reload nginx
```

## 📊 Performance Testing

### Run Comprehensive Benchmarks
```bash
python performance_profiler.py --url http://localhost:8000 --workers 1,2,3
```

### Apache Bench Quick Test
```bash
ab -n 10000 -c 100 http://localhost:8000/api/health
```

### wrk Load Testing
```bash
wrk -t12 -c400 -d30s http://localhost:8000/api/health
```

## 🐳 Docker Deployment

### Optimized Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use optimized startup
CMD ["gunicorn", "main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Docker Compose with Nginx
```yaml
version: '3.8'
services:
  app:
    build: .
    environment:
      - WORKERS=2
    depends_on:
      - db
      - redis
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
```

## 📈 Monitoring & Metrics

### Prometheus Metrics
- **HTTP Metrics**: Request count, duration, in-progress
- **Application Info**: Version, environment tracking
- **Database**: Connection count, query duration
- **Queue**: Job count, duration, queue size

### Access Metrics
```bash
curl http://localhost:8000/metrics
```

### Grafana Dashboard
Import the generated Grafana dashboard for visualizing:
- Request rate and latency
- Error rates by endpoint
- Resource utilization
- Queue and database performance

## ⚙️ Tuning Recommendations

### Worker Configuration
```bash
# CPU-intensive workloads
workers = (2 * CPU_cores) + 1

# I/O-intensive workloads  
workers = (4 * CPU_cores) + 1

# Memory-constrained environments
workers = min(4, available_memory_gb)
```

### Database Optimization
```python
# SQLAlchemy pool settings
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

### Redis Configuration
```python
# Redis connection pool
redis_client = redis.Redis(
    connection_pool=redis.ConnectionPool(
        max_connections=20,
        retry_on_timeout=True
    )
)
```

## 🔍 Troubleshooting

### High Memory Usage
```bash
# Monitor memory per worker
ps aux | grep uvicorn
htop -p $(pgrep -f uvicorn)

# Adjust worker count
export WORKERS=1  # Reduce if memory constrained
```

### High CPU Usage
```bash
# Profile CPU usage
python -m cProfile -o profile.stats main.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"
```

### Connection Issues
```bash
# Check connection limits
ulimit -n  # File descriptors
netstat -an | grep :8000 | wc -l  # Active connections

# Increase limits if needed
echo "fs.file-max = 100000" >> /etc/sysctl.conf
echo "* soft nofile 100000" >> /etc/security/limits.conf
```

### Database Performance
```bash
# PostgreSQL performance
EXPLAIN ANALYZE SELECT * FROM table WHERE condition;

# Check slow queries
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

## 🎯 Performance Targets

### Latency Goals
- **P50**: < 10ms for simple endpoints
- **P95**: < 50ms for complex queries
- **P99**: < 200ms under normal load

### Throughput Targets  
- **Simple endpoints**: 5,000+ req/s per worker
- **Database queries**: 1,000+ req/s per worker
- **File uploads**: 100+ req/s per worker

### Resource Utilization
- **CPU**: < 70% average per worker
- **Memory**: < 500MB per worker  
- **Connections**: < 80% of pool size

## 📚 Advanced Topics

### Custom Middleware
```python
class CustomPerformanceMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Add custom performance logic
        await self.app(scope, receive, send)
```

### Background Tasks
```python
from fastapi import BackgroundTasks

@app.post("/api/heavy-task")
async def process_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(heavy_computation)
    return {"status": "processing"}
```

### Caching Strategies
```python
from functools import lru_cache
import redis

# In-memory caching
@lru_cache(maxsize=1000)
def expensive_computation(param):
    return result

# Redis caching
async def cached_api_call(key):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    result = await api_call()
    redis_client.setex(key, 300, json.dumps(result))
    return result
```

## 🛠️ Development vs Production

### Development Settings
```python
# settings/development.py
DEBUG = True
RELOAD = True
WORKERS = 1
LOG_LEVEL = "debug"
```

### Production Settings  
```python
# settings/production.py
DEBUG = False
RELOAD = False
WORKERS = 2  # Based on your profiling
LOG_LEVEL = "info"
ACCESS_LOG = False  # Disable for performance
```

## 📞 Support & Resources

- **Documentation**: Full API docs at `/docs`
- **Metrics**: Performance metrics at `/metrics`
- **Health Check**: Status endpoint at `/health`
- **GitHub Issues**: Report performance issues
- **Benchmarks**: Run `performance_profiler.py` for custom tests

---

<p align="center">
  <strong>🚀 Built with LEA MCP Server - Optimized for Speed & Scale</strong>
</p>