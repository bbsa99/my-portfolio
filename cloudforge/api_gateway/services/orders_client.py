# CloudForge API Gateway - Orders Service Client

"""
HTTP client for the Orders microservice.

Provides a Python interface to the Orders service API endpoints.
Handles request formatting, response parsing, and error handling.
"""

import httpx
from typing import List, Optional, Dict, Any
from fastapi import HTTPException

from ...core.config import settings


class OrdersClient:
    """Client for interacting with the Orders service."""
    
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.orders_service_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
    
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order.
        
        Args:
            order_data: Order data (items, customer_id, etc.)
            
        Returns:
            Dict with created order details
        """
        try:
            response = await self.client.post("/orders", json=order_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to create order: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Orders service unavailable: {str(e)}",
            )
    
    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get an order by ID.
        
        Args:
            order_id: The order ID
            
        Returns:
            Dict with order details
        """
        try:
            response = await self.client.get(f"/orders/{order_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Order {order_id} not found",
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Orders service error: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Orders service unavailable: {str(e)}",
            )
    
    async def list_user_orders(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List orders for the current user with optional status filter.
        
        Args:
            page: Page number (1-indexed)
            per_page: Items per page
            status: Optional status filter (pending, paid, shipped, cancelled)
            
        Returns:
            Dict with orders list and pagination metadata
        """
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        
        try:
            response = await self.client.get("/orders", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Orders service unavailable: {str(e)}",
            )
    
    async def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        """Update order status.
        
        Args:
            order_id: The order ID
            status: New order status
            
        Returns:
            Dict with update confirmation
        """
        try:
            response = await self.client.put(
                f"/orders/{order_id}/status",
                json={"status": status},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to update order status: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Orders service unavailable: {str(e)}",
            )
    
    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order.
        
        Args:
            order_id: The order ID to cancel
            
        Returns:
            Dict with cancellation confirmation
        """
        try:
            response = await self.client.delete(f"/orders/{order_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to cancel order: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Orders service unavailable: {str(e)}",
            )
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Singleton instance for dependency injection
orders_client = OrdersClient()
