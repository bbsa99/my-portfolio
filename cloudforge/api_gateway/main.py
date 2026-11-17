# CloudForge API Gateway - Main Application Entry Point

"""
FastAPI application serving as the central API Gateway for CloudForge microservices.

Features:
- Request validation and routing
- JWT authentication and authorization
- Rate limiting
- Health check endpoints
- OpenAPI/Swagger documentation
- Request/response logging
- CORS configuration
"""

import logging
import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from core.config import settings
from core.logging import setup_logging
from api.v1.gateway import router as gateway_router
from api.v1.health import router as health_router
from api.v1.auth import router as auth_router
from api.v1.catalog import router as catalog_router
from api.v1.orders import router as orders_router

# Setup structured logging
setup_logging()

logger = structlog.get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title="CloudForge API Gateway",
    description="""
    Central entry point for all CloudForge microservices.
    
    Provides:
    - Request validation and routing to appropriate microservices
    - JWT authentication and authorization
    - Rate limiting per endpoint
    - Health checks for service discovery
    - OpenAPI documentation for all endpoints
    - Centralized request logging and tracing
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include versioned API routers
app.include_router(gateway_router, prefix="/api/v1", tags=["gateway"])
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
app.include_router(catalog_router, prefix="/api/v1", tags=["catalog"])
app.include_router(orders_router, prefix="/api/v1", tags=["orders"])


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Middleware that logs every request with structured data.
    
    Tracks:
    - Request method and path
    - Client IP address
    - Processing time
    - Response status code
    - User agent
    """
    import time
    
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        "request_start",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else "unknown",
        user_agent=request.headers.get("User-Agent"),
    )
    
    response = await call_next(request)
    
    processing_time = time.time() - start_time
    
    # Log completed request
    logger.info(
        "request_complete",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        processing_time_seconds=round(processing_time, 4),
    )
    
    # Add processing time header
    response.headers["X-Processing-Time"] = str(round(processing_time, 4))
    
    return response


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint returning gateway status."""
    return {
        "message": "CloudForge API Gateway is running",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.exception_handler(404)
async not_found_handler(request: Request, exc):
    """Handle 404 errors with consistent format."""
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "detail": "Endpoint not found"},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors with consistent format."""
    logger.error(
        "internal_error",
        detail=str(exc),
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "An unexpected error occurred"},
    )


# Graceful shutdown
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("api_gateway_shutting_down")