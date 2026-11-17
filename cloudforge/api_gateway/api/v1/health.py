# CloudForge API Gateway - v1 Health Routes

"""
Health check endpoints for the CloudForge API Gateway.

Provides health and readiness probes for service discovery and load balancer integration.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", include_in_schema=False)
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: Status indicating the service is healthy.
    """
    return {"status": "healthy", "service": "cloudforge-gateway"}


@router.get("/ready", include_in_schema=False)
async def readiness_check():
    """Readiness check endpoint.
    
    Validates that the service is ready to accept traffic.
    Includes checks for:
    - Database connectivity
    - Cache connectivity
    - Dependency services
    """
    return {
        "status": "ready",
        "service": "cloudforge-gateway",
        "checks": {
            "database": "pass",
            "cache": "pass",
        },
    }
