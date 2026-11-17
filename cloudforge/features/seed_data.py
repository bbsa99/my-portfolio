"""Feature Seed Data Module
# Feature names across all technology domains
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
    "name": "catalog-service",
    "description": "Catalog microservice with FastAPI",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "backend-team",
        "notes": "Catalog routes and HTTP client implemented",
    },
},
    "name": "orders-service",
    "description": "Orders microservice with FastAPI",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "backend-team",
        "notes": "Orders routes and services implemented",
    },
},
    "name": "database-postgres-schema",
    "description": "PostgreSQL schema and seed data setup",
    "status": FeatureStatus.NOT_IMPLEMENTED,
    "metadata": {
        "owner": "backend-team",
        "notes": "TODO: Set up database schema and seed data",
    },
},
    "name": "features-inventory-tracking",
    "description": "Feature inventory tracking system implementation",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "features/ directory created with tracker, models, and seed data",
    },
},
    "name": "documentation-all-domains",
    "description": "Comprehensive documentation for all 11 technology domains",
    "status": FeatureStatus.NOT_IMPLEMENTED,
    "metadata": {
        "owner": "documentation-team",
        "notes": "TODO: Create comprehensive documentation",
    },
},
    "name": "helm-charts",
    "description": "Helm charts for service deployment",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "Helm chart scaffolding created under helm-chart/",
    },
},
    "name": "ci-cd-github-actions",
    "description": "GitHub Actions CI/CD workflows",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "ci-cd.yml workflow created for lint, test, build, and deploy",
    },
},
    "name": "monitoring-otel-collector",
    "description": "OpenTelemetry Collector configuration",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "monitoring-team",
        "notes": "otel-collector.yaml created for Kubernetes",
    },
},
    "name": "monitoring-grafana-dashboards",
    "description": "Grafana dashboards for CloudForge monitoring",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "monitoring-team",
        "notes": "grafana-dashboard.json created",
    },
},
    "name": "monitoring-prometheus",
    "description": "Prometheus monitoring configuration",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "monitoring-team",
        "notes": "prometheus.yml configured",
    },
},
    "name": "terraform-eks-cluster",
    "description": "EKS cluster configuration with node groups",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "infra-team",
        "notes": "AWS EKS cluster resources configured",
    },
},
    "name": "terraform-aws-infrastructure",
    "description": "Terraform configuration for AWS infrastructure provisioning",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "infra-team",
        "notes": "main.tf, variables.tf, outputs.tf created",
    },
},
    "name": "kubernetes-hpa",
    "description": "Horizontal Pod Autoscaler configurations",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "HPA manifests created for gateway, catalog, and orders",
    },
},
    "name": "kubernetes-manifests",
    "description": "Complete Kubernetes manifests for all resources",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "All manifests created under kubernetes/ directory",
    },
},
    "name": "docker-compose-local-dev",
    "description": "Docker Compose for local development environment",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "docker-compose.yml set up with PostgreSQL, Redis, Catalog, and Orders",
    },
},
    "name": "docker-gateway-image",
    "description": "Docker image for API Gateway service",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "devops-team",
        "notes": "Dockerfile created at api_gateway/Dockerfile",
    },
},
    "name": "api-gateway-request-logging",
    "description": "Request logging middleware",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "backend-team",
        "notes": "Configured in api_gateway main.py",
    },
},
    "name": "api-gateway-tracing",
    "description": "OpenTelemetry tracing middleware",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "backend-team",
        "notes": "Implemented in api_gateway/middleware/tracing.py",
    },
},
    "name": "api-gateway-cors",
    "description": "CORS configuration for API Gateway",
    "status": FeatureStatus.IMPLEMENTED,
    "metadata": {
        "owner": "backend-team",
        "notes": "Set up in FastAPI app initialization",
    },
},
FEATURE_SET = [
    # API Gateway
    {
        "name": "api-gateway-jwt-auth",
        "description": "JWT authentication middleware for API Gateway",
        "status": FeatureStatus.IMPLEMENTED,
        "metadata": {
            "owner": "backend-team",
            "notes": "Implemented in api_gateway/middleware/auth.py",
        },
    },
    {
        "name": "api-gateway-rate-limiting",
        "description": "Rate limiting middleware for API Gateway",
        "status": FeatureStatus.IMPLEMENTED,
        "metadata": {
            "owner": "backend-team",
            "notes": "Configured in api_gateway/middleware/error_handling.py",
        },
    },

Seed data for populating the CloudForge feature inventory.
"""
from .models import Feature, FeatureMetadata, FeatureStatus
