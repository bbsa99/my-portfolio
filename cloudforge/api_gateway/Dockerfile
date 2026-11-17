# CloudForge API Gateway - Dockerfile
# Multi-stage build for production-ready FastAPI application

###############################################################################
# Stage 1: Build
###############################################################################
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Install dependencies first (leveraging Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

# Set working directory
WORKDIR /app

# Install runtime dependencies only (smaller image)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (same UID as builder)
RUN useradd --create-home --shell /bin/bash app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app ./app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Change to non-root user
USER app

# Expose the application port
EXPOSE 8000

# Health check for Docker/Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Application entry point
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]