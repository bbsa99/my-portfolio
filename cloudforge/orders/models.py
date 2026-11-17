# CloudForge Orders Service - Database Models
"""SQLAlchemy models for the Orders service PostgreSQL database."""

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
    ForeignKey,
)
from sqlalchemy.sql import func

from ...core.database import Base


class Order(Base):
    """Order model representing a customer order."""
    
    __tablename__ = "orders"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=func.gen_random_uuid(),
        comment="Unique order identifier",
    )
    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Reference to the user who placed the order",
    )
    status = Column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
        comment="Current order status",
    )
    total_amount = Column(
        DECIMAL(10, 2),
        nullable=False,
        comment="Total order amount in USD",
    )
    shipping_address = Column(
        JSON,
        nullable=True,
        comment="Shipping address as JSON object",
    )
    payment_id = Column(
        String(255),
        nullable=True,
        comment="Payment transaction ID",
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
        Index("ix_orders_user_id", "user_id"),
        Index("ix_orders_status", "status"),
    )
    
    def to_dict(self) -> dict:
        """Convert model to dictionary representation."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "status": self.status,
            "total_amount": float(self.total_amount) if self.total_amount else None,
            "shipping_address": self.shipping_address,
            "payment_id": self.payment_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        """Create model from dictionary."""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            status=data.get("status", "pending"),
            total_amount=data.get("total_amount"),
            shipping_address=data.get("shipping_address"),
            payment_id=data.get("payment_id"),
        )


class OrderItem(Base):
    """Order item model representing a product within an order."""
    
    __tablename__ = "order_items"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=func.gen_random_uuid(),
        comment="Unique order item identifier",
    )
    order_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        ForeignKey("orders.id", ondelete="CASCADE"),
        comment="Reference to the parent order",
    )
    product_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="Reference to the product",
    )
    quantity = Column(
        Integer,
        nullable=False,
        default=1,
        comment="Number of units ordered",
    )
    unit_price = Column(
        DECIMAL(10, 2),
        nullable=False,
        comment="Price per unit at time of purchase",
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        comment="Record creation timestamp",
    )
    
    __table_args__ = (
        Index("ix_order_items_order_id", "order_id"),
        Index("ix_order_items_product_id", "product_id"),
    )
    
    def to_dict(self) -> dict:
        """Convert model to dictionary representation."""
        return {
            "id": str(self.id),
            "order_id": str(self.order_id) if self.order_id else None,
            "product_id": str(self.product_id) if self.product_id else None,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price) if self.unit_price else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        """Create model from dictionary."""
        return cls(
            id=data.get("id"),
            order_id=data.get("order_id"),
            product_id=data.get("product_id"),
            quantity=data.get("quantity", 1),
            unit_price=data.get("unit_price"),
        )

