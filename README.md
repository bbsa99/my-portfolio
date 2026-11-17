# CloudForge - Comprehensive Cloud Engineering & DevOps Reference Project

## Overview

CloudForge is a production-style Cloud Engineering and DevOps reference project that demonstrates
integration of major cloud technologies and DevOps practices. This project serves as a comprehensive
learning laboratory for studying, experimenting with, and understanding how modern cloud engineering
components work together in a real engineering environment.

## Architecture

CloudForge consists of the following microservices:

- **API Gateway** (`cloudforge/api_gateway/`) - FastAPI-based gateway serving as the entry point
  - Request validation and routing
  - Authentication and authorization
  - Rate limiting and health checks
  
- **Catalog Service** (`cloudforge/catalog/`) - Product/catalog management
  - CRUD operations for catalog items
  - Database integration with PostgreSQL
  
- **Orders Service** (`cloudforge/orders/`) - Order processing system
  - Order creation, tracking, and management
  - Inter-service communication via messages

- **Shared Infrastructure** (`cloudforge/infrastructure/`)
  - Docker configurations and Dockerfiles
  - Kubernetes manifests
  - Helm charts
  - Terraform configurations
  - Monitoring stack (Prometheus + Grafana)
  - CI/CD pipelines (GitHub Actions)

## Technology Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy async
- **Database**: PostgreSQL with async driver
- **Cache/Queue**: Redis
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **Package Management**: Helm
- **Infrastructure as Code**: Terraform
- **Monitoring**: Prometheus, Grafana
- **CI/CD**: GitHub Actions
- **API Documentation**: OpenAPI/Swagger

## Quick Start

```bash
# Start all services with Docker Compose
docker-compose up -d

# Access the API Gateway
http://localhost:8000

# Access Grafana dashboards
http://localhost:3000 (admin/admin)

# Access API docs
http://localhost:8000/docs
```

## Repository Structure

```
cloudforge/
├── api_gateway/       # FastAPI API Gateway
├── catalog/           # Catalog service
├── orders/            # Orders service
├── infrastructure/
│   ├── docker/        # Docker configs and Dockerfiles
│   ├── k8s/           # Kubernetes manifests
│   ├── terraform/     # Terraform configurations
│   ├── monitoring/    # Prometheus + Grafana
│   └── ci_cd/         # GitHub Actions workflows
├── docs/              # Comprehensive documentation
└── tests/             # Unit, integration, and e2e tests
```

## Implementation Roadmap

This project tracks features at five levels:
- **NOT IMPLEMENTED** - Feature not yet started
- **IMPLEMENTED** - Configuration/code exists
- **TESTED** - Feature works as expected
- **DOCUMENTED** - Documentation written
- **PRODUCTION VALIDATED** - Validated in production-like environment

See each technology section for detailed feature inventories.

---

*CloudForge - Study. Experiment. Understand. Engineer.*