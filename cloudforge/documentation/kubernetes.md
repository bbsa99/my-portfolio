# Kubernetes

## Overview

CloudForge uses Kubernetes for container orchestration. All Kubernetes manifests are stored in the `kubernetes/` directory and can be deployed using `kubectl`.

## Namespace

All CloudForge resources are deployed to the `cloudforge` namespace:

```bash
kubectl apply -f kubernetes/namespace.yaml
```

## Core Resources

### PostgreSQL Deployment

```bash
kubectl apply -f kubernetes/postgres-deployment.yaml
```

### PostgreSQL Service

```bash
kubectl apply -f kubernetes/postgres-service.yaml
```

### Redis Deployment

```bash
kubectl apply -f kubernetes/redis-deployment.yaml
```

### Redis Service

```bash
kubectl apply -f kubernetes/redis-service.yaml
```

### API Gateway Deployment

```bash
kubectl apply -f kubernetes/gateway-deployment.yaml
```

### API Gateway Service

```bash
kubectl apply -f kubernetes/gateway-service.yaml
```

### Catalog Deployment

```bash
kubectl apply -f kubernetes/catalog-deployment.yaml
```

### Catalog Service

```bash
kubectl apply -f kubernetes/catalog-service.yaml
```

### Orders Deployment

```bash
kubectl apply -f kubernetes/orders-deployment.yaml
```

### Orders Service

```bash
kubectl apply -f kubernetes/orders-service.yaml
```

## Advanced Kubernetes Resources

### ConfigMap

```bash
kubectl apply -f kubernetes/configmap.yaml
```

### Secret

```bash
kubectl apply -f kubernetes/secret.yaml
```

### Ingress

```bash
kubectl apply -f kubernetes/ingress.yaml
```

### Horizontal Pod Autoscaler

```bash
kubectl apply -f kubernetes/hpa.yaml
```

### OpenTelemetry Collector

```bash
kubectl apply -f kubernetes/otel-collector.yaml
```

## Validation

```bash
# Dry run client validation
kubectl apply --dry-run=client -f kubernetes/

# Check resource status
kubectl get all -n cloudforge

# Describe a specific resource
kubectl describe deployment cloudforge-gateway -n cloudforge
```
