"""High-performance ASGI-compliant middleware for FastAPI applications."""

import time
from typing import Callable, Dict, Any
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import Counter, Histogram, Gauge


# Metrics definitions
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

REQUEST_IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests currently being processed'
)


class ASGIPrometheusMiddleware:
    """High-performance ASGI-compliant Prometheus metrics middleware."""
    
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI middleware implementation."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Skip metrics endpoint
        if request.url.path == "/metrics":
            await self.app(scope, receive, send)
            return
        
        # Extract metrics data
        method = scope["method"]
        endpoint = self._extract_endpoint(scope)
        
        # Track request in progress
        REQUEST_IN_PROGRESS.inc()
        start_time = time.perf_counter()
        
        # Wrap send to capture response status
        status_code = "500"  # Default for errors
        
        async def send_wrapper(message: Dict[str, Any]) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = str(message["status"])
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Record metrics
            duration = time.perf_counter() - start_time
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
            REQUEST_IN_PROGRESS.dec()
    
    def _extract_endpoint(self, scope: Scope) -> str:
        """Extract endpoint pattern from ASGI scope."""
        # Try to get route pattern
        if "route" in scope:
            route = scope["route"]
            if hasattr(route, "path"):
                return route.path
        
        # Fallback to path with normalization
        path = scope["path"]
        
        # Normalize common patterns
        if path.startswith("/api/"):
            parts = path.split("/")
            if len(parts) > 3:
                # Replace IDs with placeholder
                if parts[3].isdigit() or len(parts[3]) > 10:
                    parts[3] = "{id}"
            return "/".join(parts[:4]) if len(parts) > 3 else path
        
        return path


class ASGILoggingMiddleware:
    """High-performance ASGI-compliant logging middleware."""
    
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI middleware implementation."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        start_time = time.perf_counter()
        
        # Wrap send to capture response data
        status_code = 500
        response_size = 0
        
        async def send_wrapper(message: Dict[str, Any]) -> None:
            nonlocal status_code, response_size
            if message["type"] == "http.response.start":
                status_code = message["status"]
            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                response_size += len(body)
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Log request completion
            duration = time.perf_counter() - start_time
            print(f"{request.method} {request.url.path} {status_code} "
                  f"{response_size}B {duration:.3f}s")


class ASGISecurityHeadersMiddleware:
    """High-performance ASGI-compliant security headers middleware."""
    
    def __init__(self, app: ASGIApp, security_headers: Dict[str, str] = None) -> None:
        self.app = app
        self.security_headers = security_headers or {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI middleware implementation."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        async def send_wrapper(message: Dict[str, Any]) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                
                # Add security headers
                for name, value in self.security_headers.items():
                    headers.append((name.encode(), value.encode()))
                
                message["headers"] = headers
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


class ASGICompressionMiddleware:
    """High-performance ASGI-compliant compression middleware."""
    
    def __init__(self, app: ASGIApp, minimum_size: int = 1024) -> None:
        self.app = app
        self.minimum_size = minimum_size
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI middleware implementation."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Check if client accepts gzip
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding.lower():
            await self.app(scope, receive, send)
            return
        
        # Collect response body
        response_started = False
        response_body = b""
        headers = []
        status_code = 200
        
        async def send_wrapper(message: Dict[str, Any]) -> None:
            nonlocal response_started, response_body, headers, status_code
            
            if message["type"] == "http.response.start":
                response_started = True
                status_code = message["status"]
                headers = list(message.get("headers", []))
                # Don't send start yet, collect body first
            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                response_body += body
                more_body = message.get("more_body", False)
                
                if not more_body:
                    # All body collected, decide on compression
                    if len(response_body) >= self.minimum_size:
                        import gzip
                        compressed_body = gzip.compress(response_body)
                        
                        # Add compression headers
                        headers.append((b"content-encoding", b"gzip"))
                        headers.append((b"content-length", str(len(compressed_body)).encode()))
                        
                        # Send start with updated headers
                        await send({
                            "type": "http.response.start",
                            "status": status_code,
                            "headers": headers
                        })
                        
                        # Send compressed body
                        await send({
                            "type": "http.response.body",
                            "body": compressed_body
                        })
                    else:
                        # Send without compression
                        headers.append((b"content-length", str(len(response_body)).encode()))
                        await send({
                            "type": "http.response.start",
                            "status": status_code,
                            "headers": headers
                        })
                        await send({
                            "type": "http.response.body",
                            "body": response_body
                        })
        
        await self.app(scope, receive, send_wrapper)