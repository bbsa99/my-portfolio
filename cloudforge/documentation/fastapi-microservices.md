# Python FastAPI Microservices

## Overview

CloudForge implements a complete microservices architecture using Python FastAPI. The system consists of three main services:

- **API Gateway**: Entry point for all external requests, handling authentication, routing, and rate limiting
- **Catalog Service**: Manages product catalog operations
- **Orders Service**: Handles order processing and management

## Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   API Gateway   │──────▶│   Catalog Service│──────▶│   Orders Service│
└─────────────────┘      └─────────────────┘      └─────────────────┘
       │                       │                      │
       │                       │                      │
       ▼                       ▼                      ▼
   PostgreSQL               Redis                  PostgreSQL
```

## Key Features

- **JWT Authentication**: Token-based authentication with middleware
- **Rate Limiting**: Configurable rate limits per endpoint
- **CORS**: Cross-origin resource sharing configured
- **Request Logging**: Structured logging for all requests
- **OpenTelemetry Tracing**: Distributed tracing support
- **Pydantic-Settings**: Environment-based configuration

## Service Structure

Each service follows the same pattern:

```
cloudforge/api_gateway/       # API Gateway service
cloudforge/catalog/           # Catalog service
cloudforge/orders/            # Orders service
```

### Core Components

- `main.py` - FastAPI application entry point
- `core/config.py` - Pydantic-settings configuration
- `api/v1/` - Versioned API routes
- `middleware/` - Custom middleware (auth, error handling, tracing)
- `services/` - HTTP clients for inter-service communication
- `docker-compose.yml` - Local development orchestration
- `Dockerfile` - Container definition
