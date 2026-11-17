# Helm

## Overview

CloudForge uses Helm charts for packaging and deploying Kubernetes applications. The Helm chart is located in the `helm-chart/` directory.

## Chart Structure

```
helm-chart/
  Chart.yaml    # Chart metadata
  values.yaml   # Default configuration values
  templates/    # Kubernetes template files
```

## Installation

### Prerequisites

```bash
# Add Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install nginx ingress controller
helm upgrade --install ingress-bitnami bitnami/nginx-ingress \
  --namespace cloudforge --create-namespace
```

### Deploy CloudForge

```bash
# Update Helm repositories
helm repo update

# Install CloudForge with Helm
helm upgrade --install cloudforge ./cloudforge/helm-chart \
  --namespace cloudforge
```

## Configuration

### Default Values

The `values.yaml` file contains all configurable options:

```yaml
# Key configuration options
global:
  namespace: cloudforge
  nameOverride: cloudforge
  fullnameOverride: cloudforge

image:
  registry: ghcr.io
  repository: ghcr.io/cloudforge/cloudforge
  tag: "latest"

service:
  gatewayPort: 8000
  catalogPort: 8001
  ordersPort: 8002

replicas:
  gateway: 2
  catalog: 2
  orders: 2

resources:
  limits:
    memory: "512Mi"
    cpu: "750m"
  requests:
    memory: "256Mi"
    cpu: "250m"

gateway:
  enabled: true
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 50
    targetMemoryUtilizationPercentage: 70
  serviceType: LoadBalancer
  ingress:
    enabled: true
    className: nginx
    hosts:
      - host: api.cloudforge.local
        paths:
          - path: /
            pathType: ImplementationSpecific

catalog:
  enabled: true
  serviceType: ClusterIP

orders:
  enabled: true
  serviceType: ClusterIP

postgres:
  enabled: true
  persistence:
    enabled: true
    size: 20Gi
    storageClass: gp2

redis:
  enabled: true
  persistence:
    enabled: true
    size: 100Mi
    storageClass: redis

monitoring:
  enabled: true
  prometheus:
    enabled: true
    servicePort: 9090
  grafana:
    enabled: true
    adminPassword: admin
    serviceType: LoadBalancer
```

### Custom Values

```bash
# Install with custom values
helm upgrade --install cloudforge ./cloudforge/helm-chart \
  --namespace cloudforge \
  --set gateway.replicas=3 \
  --set monitoring.grafana.adminPassword=secure-password
```

## Chart Template Files

### namespace.yaml

Creates the `cloudforge` namespace for all resources.

### configmap.yaml

Configures environment variables for the services.

### secret.yaml

Stores sensitive data like JWT secrets and database passwords.

### gateway-deployment.yaml

Deploys the API Gateway with autoscaling and health checks.

### secret.yaml (in templates)

Stores sensitive configuration data.

### ingress.yaml

Configures the NGINX Ingress controller for external access.

## Testing

```bash
# Lint the chart
helm lint ./cloudforge/helm-chart

# Dry run the installation
helm install my-release ./cloudforge/helm-chart --dry-run --debug

# List installed releases
helm list -n cloudforge
```
