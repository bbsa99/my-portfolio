# Docker

## Overview

CloudForge uses Docker for containerization of all microservices. The project includes Docker configurations for local development and production deployment.

## Docker Compose

Local development environment is orchestrated using Docker Compose:

```yaml
# cloudforge/api_gateway/docker-compose.yml
services:
  gateway:
    build: ./api_gateway
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
  
  catalog:
    build: ./catalog
    ports:
      - "8001:8001"
  
  orders:
    build: ./orders
    ports:
      - "8002:8002"
  
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: cloudforge
      POSTGRES_USER: cloudforge
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  redis:
    image: redis:7
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

## Individual Service Dockerfiles

### API Gateway Dockerfile

```dockerfile
# cloudforge/api_gateway/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api_v1.gateway:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Catalog Service Dockerfile

```dockerfile
# cloudforge/catalog/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "api_v1.catalog:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Orders Service Dockerfile

```dockerfile
# cloudforge/orders/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["uvicorn", "api_v1.orders:app", "--host", "0.0.0.0", "--port", "8002"]
```

## Building and Running

```bash
# Build all services
docker-compose build

# Start local development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```
