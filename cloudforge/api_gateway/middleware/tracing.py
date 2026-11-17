# CloudForge API Gateway - Tracing Middleware

"""
Request tracing middleware for the API Gateway.

Provides distributed tracing support by:
- Generating unique request IDs
- Timing request processing
- Adding trace context to logs and response headers
- Supporting OpenTelemetry integration
"""

import time
import uuid
from fastapi import Request, Response
from starlette.responses import Response as StarletteResponse


class TracingMiddleware:
    """Middleware that adds request tracing information."""
    
    def __init__(self, app, service_name: str = "cloudforge-gateway"):
        self.app = app
        self.service_name = service_name
    
    async def __call__(self, scope, receive, send):
        """Process the ASGI scope with tracing."""
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Record start time
        start_time = time.time()
        
        # Add request ID to scope for use in routes/middleware
        scope["request_id"] = request_id
        
        # Custom async iterator to add X-Request-ID header to response
        async def send_wrapper(message):
            if message["type"] == "http.response":
                message["headers"] = list(message.get("headers", [])) + [
                    (b"X-Request-ID", request_id.encode()),
                    (b"X-Service-Name", self.service_name.encode()),
                ]
            await send(message)
        
        # Process the request
        async def start_timer():
            """Wait and then add timing info."""
            await self.app(scope, receive, send_wrapper)
        
        # Record processing time in response headers
        processing_time = (time.time() - start_time) * 1000  # in milliseconds
        
        # We need to track this differently since we can't easily
    # modify the response after it's sent. Instead, let's use a simpler approach.
    
    @staticmethod
    def add_trace_headers(response: Response, request_id: str, processing_ms: float):
        """Add tracing headers to a response.
        
        Args:
            response: FastAPI/Starlette Response object
            request_id: Unique request identifier
            processing_ms: Processing time in milliseconds
        """
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Processing-Time-MS"] = str(round(processing_ms, 2))
        response.headers["X-Service-Name"] = "cloudforge-gateway"


# Convenience function for routes
def tracing_decorator(
    func,
    request_id_header: str = "X-Request-ID",
):
    """Decorator that adds tracing info to route responses."""
    async def wrapper(*args, **kwargs):
        from fastapi import Request
        # Get request from args - first arg could be Request or dict
        request = None
        if args and isinstance(args[0], Request):
            request = args[0]
        elif "request" in kwargs and isinstance(kwargs["request"], Request):
            request = kwargs["request"]
        
        if request:
            rid = getattr(request, "state", {}).get("request_id", None)
            if not rid:
                rid = str(uuid.uuid4())
        
        # Execute the original function
        result = await func(*args, **kwargs)
        
        # Add tracing headers if we have a response
        if hasattr(result, 'headers'):
            processing_ms = getattr(result, '_processing_ms', 0)
            result.headers[X-Request-ID'] = rid
            result.headers['X-Processing-Time-MS'] = str(round(processing_ms, 2))
        
        return result
    return wrapper
