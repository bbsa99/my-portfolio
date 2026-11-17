# API Gateway

## Overview

The API Gateway serves as the entry point for all external requests to the CloudForge microservices architecture. It handles authentication, routing, rate limiting, and provides a unified interface to downstream services.

## Architecture

```
Client Requests
       ↓
┌─────────────────────┐
│   API Gateway (FastAPI) │
│  - JWT Authentication  │
│  - Rate Limiting      │
│  - CORS Headers      │
│  - Request Logging    │
│  - Health Checks      │
└─────────────────────┘
       ↓
┌─────────────────────┐      ┌─────────────────────┐
│   Catalog Service   │──────▶│   PostgreSQL DB      │
│   - Product listings │      │   - Products table   │
│   - Search          │      └─────────────────────┘
│   - Filter          │
└─────────────────────┘
       ↓
┌─────────────────────┐      ┌─────────────────────┐
│   Orders Service    │──────▶│   PostgreSQL DB      │
│   - Create order    │      │   - Orders table     │
│   - Get order       │      └─────────────────────┘
│   - Update order    │
│   - Cancel order    │
└─────────────────────┘
       ↓
┌─────────────────────┐
│   Redis Cache       │
│   - Session storage │
│   - Rate limiting   │
└─────────────────────┘
```

## API Routes (v1)

### Health Checks

- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health status

### Auth Routes

- `POST /api/v1/auth/login` - User login with JWT token
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Revoke token

### Catalog Routes

- `GET /api/v1/catalog/` - List all products
- `GET /api/v1/catalog/{id}` - Get product by ID
- `GET /api/v1/catalog/search/{query}` - Search products
- `POST /api/v1/catalog/` - Create new product (admin)
- `PUT /api/v1/catalog/{id}` - Update product (admin)
- `DELETE /api/v1/catalog/{id}` - Delete product (admin)

### Orders Routes

- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/{id}` - Get order by ID
- `GET /api/v1/orders/user/{user_id}` - Get user's orders
- `PUT /api/v1/orders/{id}/status` - Update order status
- `DELETE /api/v1/orders/{id}` - Cancel order

## Middleware

### JWT Authentication Middleware

- Validates JWT tokens on protected routes
- Extracts user identity from token
- Attaches user context to request state
- Returns 401 Unauthorized for invalid/missing tokens

### Error Handling Middleware

- Catches unhandled exceptions
- Returns consistent error format
- Logs error details for debugging
- Handles validation errors gracefully

### Tracing Middleware

- Integrates with OpenTelemetry
- Creates spans for each request
- Records request duration and attributes
- Exports traces to collector

## Configuration

### Environment Variables (.env.example)

```env
# Application
APP_NAME=cloudforge
DEBUG=true
ENVIRONMENT=development

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
POSTGRES_SERVER=postgres
POSTGRES_PORT=5432
POSTGSES_DB=cloudforge
POSTGRES_USER=cloudforge
POSTGRES_PASSWORD=your-postgres-password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Services
CATALOG_SERVICE_URL=http://catalog:8001
ORDERS_SERVICE_URL=http://orders:8002

# OpenTelemetry
OTEL_SERVICE_NAME=cloudforge-gateway
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
CORS_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
CORS_HEADERS=*
```

## Docker Deployment

```bash
# Build the gateway image
docker build -t cloudforge-gateway -f Dockerfile ./api_gateway

# Run with Docker Compose
docker-compose up -d

# Or run manually
docker run -d -p 8000:8000 \
  -e JWT_SECRET_KEY=your-key \
  -e POSTGRES_PASSWORD=your-password \
  -e REDIS_PASSWORD=your-redis-password \
  cloudforge-gateway
```

## Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f kubernetes/

# Check gateway status
kubectl get deployment cloudforge-gateway -n cloudforge

# View logs
kubectl logs deployment/cloudforge-gateway -n cloudforge

# Port-forward for testing
kubectl port-forward svc/cloudforge-gateway 8000:8000 -n cloudforge
```
