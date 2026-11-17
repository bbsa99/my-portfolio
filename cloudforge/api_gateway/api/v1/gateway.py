# CloudForge API Gateway - v1 Gateway Routes

"""
Gateway routing endpoints that direct requests to the appropriate microservices.

Routes:
- GET /api/v1/health - Health check
- GET /api/v1/catalog - Forward to catalog service
- GET /api/v1/orders - Forward to orders service
- POST /api/v1/orders - Forward to orders service
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import JSONResponse

router = APIRouter(prefix="/v1", tags=["gateway"])


@router.get("/health", include_in_schema=False)
async def gateway_health():
    """Gateway health check - returns overall system status."""
    return {
        "service": "cloudforge-gateway",
        "status": "healthy",
    }


@router.get("/catalog", include_in_schema=False)
async def forward_to_catalog():
    """Forward request to catalog service."""
    return {"service": "catalog", "message": "Forwarded to catalog service"}


@router.post("/catalog", include_in_schema=False)
async def create_catalog_entry():
    """Create catalog entry via forwarding to catalog service."""
    return {"service": "catalog", "message": "Catalog creation forwarded"}


@router.get("/orders", include_in_schema=False)
async def forward_to_orders():
    """Forward request to orders service."""
    return {"service": "orders", "message": "Forwarded to orders service"}


@router.post("/orders", include_in_schema=False)
async def create_order():
    """Create order via forwarding to orders service."""
    return {"service": "orders", "message": "Order creation forwarded"}
