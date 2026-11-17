# CloudForge API Gateway - Catalog Service Client

"""
HTTP client for the Catalog microservice.

Provides a Python interface to the Catalog service API endpoints.
Handles request formatting, response parsing, and error handling.
"""

import httpx
from typing import List, Optional, Dict, Any
from fastapi import HTTPException

from ...core.config import settings


class CatalogClient:
    """Client for interacting with the Catalog service."""
    
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.catalog_service_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
    
    async def list_items(
        self,
        page: int = 1,
        per_page: int = 50,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List catalog items with pagination and optional search.
        
        Args:
            page: Page number (1-indexed)
            per_page: Items per page
            search: Optional search query
            
        Returns:
            Dict with items list and pagination metadata
        """
        params = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        
        try:
            response = await self.client.get("/catalog", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Catalog service unavailable: {str(e)}",
            )
    
    async def get_item(self, item_id: int) -> Dict[str, Any]:
        """Get a specific catalog item by ID.
        
        Args:
            item_id: The catalog item ID
            
        Returns:
            Dict with catalog item details
        """
        try:
            response = await self.client.get(f"/catalog/{item_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Catalog item {item_id} not found",
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Catalog service error: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Catalog service unavailable: {str(e)}",
            )
    
    async def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new catalog item.
        
        Args:
            item_data: Catalog item data (name, description, price, etc.)
            
        Returns:
            Dict with created catalog item details
        """
        try:
            response = await self.client.post("/catalog", json=item_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to create catalog item: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Catalog service unavailable: {str(e)}",
            )
    
    async def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing catalog item.
        
        Args:
            item_id: The catalog item ID to update
            item_data: Updated catalog item data
            
        Returns:
            Dict with updated catalog item details
        """
        try:
            response = await self.client.put(f"/catalog/{item_id}", json=item_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to update catalog item: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Catalog service unavailable: {str(e)}",
            )
    
    async def delete_item(self, item_id: int) -> Dict[str, Any]:
        """Delete a catalog item.
        
        Args:
            item_id: The catalog item ID to delete
            
        Returns:
            Dict with deletion confirmation
        """
        try:
            response = await self.client.delete(f"/catalog/{item_id}")
            response.raise_for_status()
            return {"detail": f"Catalog item {item_id} deleted successfully"}
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to delete catalog item: {str(e)}",
            )
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Catalog service unavailable: {str(e)}",
            )
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Singleton instance for dependency injection
catalog_client = CatalogClient()
