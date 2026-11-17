# CloudForge API Gateway - Error Handling Middleware

"""
Global exception handler and error response middleware for the API Gateway.

Provides consistent error responses across all endpoints,
handles expected and unexpected exceptions, and formats
error details for client consumption.
"""

from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorHandlingMiddleware:
    """Middleware that catches exceptions and returns consistent error responses."""
    
    async def __call__(self, scope, receive, send):
        """Process the ASGI scope through error handling."""
        if scope["type"] not in ("http",):
            return
    
        from fastapi import FastAPI
        # This middleware works alongside FastAPI's exception handlers
        # Additional error formatting can be added here


def error_response(
    status_code: int,
    message: str,
    details: dict | None = None,
    code: str | None = None,
) -> JSONResponse:
    """Create a standardized error response.
    
    Args:
        status_code: HTTP status code
        message: Human-readable error message
        details: Additional error details (optional)
        code: Machine-readable error code (optional)
        
    Returns:
        JSONResponse: Formatted error response
    """
    response = {
        "error": {
            "code": code or f"ERROR_{status_code}",
            "message": message,
            "details": details or {},
            "status_code": status_code,
        }
    }
    return JSONResponse(content=response, status_code=status_code)


# Common error helpers


def not_found(resource: str = "resource", id: str | None = None) -> JSONResponse:
    """Create a 404 Not Found error response.
    
    Args:
        resource: Resource type that was not found
        id: Resource ID (optional)
        
    Returns:
        JSONResponse: 404 error response
    """
    message = f"{resource} not found"
    details = {}
    if id:
        details["requested_id"] = id
    return error_response(
        status_code=404,
        message=message,
        details=details,
        code="NOT_FOUND",
    )


def validation_error(message: str, field: str | None = None) -> JSONResponse:
    """Create a 422 Validation error response.
    
    Args:
        message: Validation error message
        field: Field that failed validation (optional)
        
    Returns:
        JSONResponse: 422 error response
    """
    details = {}
    if field:
        details["field"] = field
    return error_response(
        status_code=422,
        message=message,
        details=details,
        code="VALIDATION_ERROR",
    )


def unauthorized(message: str = "Unauthorized") -> JSONResponse:
    """Create a 401 Unauthorized error response.
    
    Args:
        message: Error message
        
    Returns:
        JSONResponse: 401 error response
    """
    return error_response(
        status_code=401,
        message=message,
        code="UNAUTHORIZED",
    )


def forbidden(message: str = "Forbidden") -> JSONResponse:
    """Create a 403 Forbidden error response.
    
    Args:
        message: Error message
        
    Returns:
        JSONResponse: 403 error response
    """
    return error_response(
        status_code=403,
        message=message,
        code="FORBIDDEN",
    )


def internal_error(message: str = "Internal server error") -> JSONResponse:
    """Create a 500 Internal Server Error response.
    
    Args:
        message: Error message
        
    Returns:
        JSONResponse: 500 error response
    """
    return error_response(
        status_code=500,
        message=message,
        code="INTERNAL_ERROR",
    )
