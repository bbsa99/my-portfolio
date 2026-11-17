# CloudForge Catalog Service - Database Models
"""SQLAlchemy models for the Catalog service PostgreSQL database."""

from sqlalchemy import (
    Column,
    UUID,
    String,
    Text,
    DECIMAL,
    Integer,
    Boolean,
    DateTime,
    JSON,
    Index,
)
from sqlalchemy.sql import func

from ...core.database import Base


class Product(Base):
    """Product model representing a catalog item."""
    
    __tablename__ = "products"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=func.gen_random_uuid(),
        comment="Unique product identifier",
    )
    name = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Product name",
    )
    description = Column(
        Text,
        nullable=True,
        comment="Product description",
    )
    price = Column(
        DECIMAL(10, 2),
        nullable=False,
        comment="Product price in USD",
    )
    category = Column(
        String(100),
        nullable=True,
        index=True,
        comment="Product category",
    )
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        comment="Whether the product is active",
    )
    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Current stock quantity",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        comment="Record creation timestamp",
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="Last update timestamp",
    )
    
    __table_args__ = (
        Index("ix_products_name", "name"),
        Index("ix_products_category", "category"),
        Index("ix_products_active", "is_active"),
    )
    
    def to_dict(self) -> dict:
        """Convert model to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": float(self.price) if self.price else None,
            "category": self.category,
            "is_active": self.is_active,
            "stock_quantity": self.stock_quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create model from dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description"),
            price=data.get("price"),
            category=data.get("category"),
            is_active=data.get("is_active", True),
            stock_quantity=data.get("stock_quantity", 0),
        )
