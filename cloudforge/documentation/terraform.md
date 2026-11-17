# Terraform

## Overview

CloudForge uses Terraform for AWS infrastructure provisioning. The Terraform configuration is located in the `terraform/` directory.

## Configuration Files

### main.tf

The main Terraform configuration that defines AWS resources including:

- EKS cluster with node groups
- IAM roles and policies
- RDS PostgreSQL instance
- Elasticache Redis cluster
- ALB Ingress controller
- Kubernetes cluster integration

### variables.tf

Input variables for infrastructure configuration:

- AWS region and credentials
- Environment (development, staging, production)
- EKS cluster name and node group settings
- Database instance classes and storage
- Service port configurations

### outputs.tf

Output values from infrastructure deployment:

- Cluster name and endpoint
- Service URLs (gateway, catalog, orders)
- Database endpoint and port
- Monitoring URLs (Prometheus, Grafana)
- Terraform state bucket name

## AWS Resources Provisioned

### EKS Cluster

- Managed Kubernetes cluster
- Node group with auto-scaling
- Integrated with ALB Ingress

### RDS PostgreSQL

- Managed PostgreSQL database
- Configurable instance class and storage
- Automated backups

### Elasticache Redis

- Managed Redis cluster
- Used for caching and session storage

### IAM Roles

- EKS node group IAM role
- Service account policies
- least-privilege access model

## Usage

### Initialization

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan the deployment
terraform plan -var="environment=development"
```

### Apply

```bash
# Apply the configuration
terraform apply -var="environment=development"

# Confirm changes with auto-approve
terraform apply -auto-approve -var="environment=production"
```

### Destroy

```bash
# Destroy all resources
terraform destroy -var="environment=development"
```

## Best Practices

- Use separate workspaces for each environment
- Store sensitive data in AWS Systems Manager Parameter Store
- Implement Terraform remote state backend (S3 + DynamoDB)
- Regularly run `terraform plan` to detect drift
- Tag all resources for cost tracking and identification
