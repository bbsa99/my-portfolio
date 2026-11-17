"""Alembic environment configuration for CloudForge API Gateway."""

from importlib import context
import os
import sys

from alembic import context

# Add the api_gateway directory to the path so we can import our code
sys.path.insert(0, os.path.dirname(__file__) + "/../../../..")

from core.config import Settings
from core.database import Base, engine, get_session_factory

# Get settings
settings = Settings()

# Import all models to ensure they are registered with Base
# This is important for Alembic to detect new models
import core.database  # noqa: F401
import catalog.models  # noqa: F401
import orders.models  # noqa: F401

# This is the target metadata for Alembic auto-generates
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = settings.postgres_dsn
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
