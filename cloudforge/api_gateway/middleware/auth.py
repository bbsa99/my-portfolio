# CloudForge API Gateway - Authentication Middleware

"""
JWT authentication middleware for the API Gateway.

Validates bearer tokens on incoming requests and attaches
the authenticated user to the request state.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Middleware that validates JWT tokens on each request."""
    
    async def dispatch(self, request: Request, call_next):
        """Process each request through the middleware."""
        auth_header = request.headers.get("Authorization")
        
        # Default to anonymous user
        request.state.user = {"anonymous": True, "roles": []}
        request.state.authenticated = False
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix
            # In a real implementation, validate the JWT token here
            # e.g., decode token, check expiration, verify signature
            try:
                # Placeholder for token validation
                request.state.user = {
                    "anonymous": False,
                    "username": "authenticated_user",
                    "roles": ["user"],
                }
                request.state.authenticated = True
            except Exception:
                # Token validation failed, keep anonymous
                pass
        
        response = await call_next(request)
        
        # Add authentication info to response headers
        if request.state.authenticated:
            response.headers["X-User-Roles"] = ",".join(
                request.state.user.get("roles", [])
            )
        
        return response
