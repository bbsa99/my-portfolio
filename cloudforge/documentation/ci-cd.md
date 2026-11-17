# CI/CD

## Overview

CloudForge uses GitHub Actions for continuous integration and continuous deployment (CI/CD). The workflow is defined in `.github/workflows/ci-cd.yml`.

## Workflow Structure

The CI/CD pipeline consists of the following jobs:

### 1. Lint and Test

Runs on every push and pull request to `main` and `develop` branches.

**Steps:**
- Checkout code
- Set up Python 3.12
- Install dependencies from `requirements.txt`
- Lint with `ruff`
- Format check with `black`
- Type check with `mypy`
- Run pytest test suite

**Outputs:**
- `test_passed`: Boolean indicating if all tests passed

### 2. Build Image

Runs on push to `main` branch only.

**Dependencies:** lint-test job

**Steps:**
- Log in to GitHub Container Registry (GHCR)
- Build and push API Gateway Docker image
- Build and push Catalog Docker image
- Build and push Orders Docker image

### 3. Deploy to Kubernetes

Runs on push to `main` branch.

**Dependencies:** build-image job

**Environment:** production

**Steps:**
- Install kubectl and eksctl
- Configure AWS Kubeconfig
- Update kubeconfig for the EKS cluster
- Deploy with Helm:
  - Install nginx ingress controller
  - Deploy CloudForge Helm chart with updated image tags

### 4. Health Check

Runs after deployment completes.

**Steps:**
- Wait for all pods to be ready
- Port-forward to services and verify health endpoints
- Check `/api/v1/health` on gateway, catalog, and orders

## Local Development Workflow

### Running Tests Locally

```bash
# Install dependencies
pip install -r cloudforge/api_gateway/requirements.txt

# Run linting
ruff check .

# Format check
black --check .

# Type checking
mypy cloudforge/api_gateway/

# Run tests
python -m pytest cloudforge/api_gateway/tests/ -v
```

### Docker Compose for Local Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Kubernetes Local Development

```bash
# Install kind or use Docker Desktop Kubernetes
kind create cluster --name cloudforge

# Or enable Docker Desktop Kubernetes

# Deploy manifests
kubectl apply -f kubernetes/

# Port-forward for development
kubectl port-forward svc/cloudforge-gateway 8000:8000 -n cloudforge
```

## Deployment Commands

```bash
# Lint Helm chart
helm lint cloudforge/helm-chart

# Dry run installation
helm install cloudforge-test ./cloudforge/helm-chart --dry-run --debug

# Install release
helm upgrade --install cloudforce ./cloudforge/helm-chart --namespace cloudforge

# View release status
helm status cloudforce -n cloudforge

# Rollback to previous version
helm rollback cloudforce 1 -n cloudforce
```

## Environment Promotion

The pipeline supports promotion through environments:

1. **Development**: Automatically deployed on feature branch pushes
2. **Staging**: Deployed after integration testing
3. **Production**: Deployed after all tests pass and manual approval
```
