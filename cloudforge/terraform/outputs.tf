# CloudForge - Terraform Outputs
# Output values from infrastructure deployment

# Kubernetes Cluster
output "cluster_name" {
  description = "EKS cluster name"
  value       = var.cluster_name
}

output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = data.aws_eks_cluster.cluster.endpoint
}

output "cluster_version" {
  description = "EKS cluster version"
  value       = data.aws_eks_cluster.cluster.version
}

# Service Endpoints
output "gateway_url" {
  description = "API Gateway URL"
  value       = "http://${aws_lb.gateway.dns_name}:${var.gateway_service_port}"
}

output "catalog_url" {
  description = "Catalog service URL"
  value       = "http://${aws_lb.catalog.dns_name}:${var.catalog_service_port}"
}

output "orders_url" {
  description = "Orders service URL"
  value       = "http://${aws_lb.orders.dns_name}:${var.orders_service_port}"
}

# Database
output "postgres_endpoint" {
  description = "PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "postgres_port" {
  description = "PostgreSQL port"
  value       = aws_db_instance.postgres.port
}

# Monitoring
output "prometheus_url" {
  description = "Prometheus monitoring URL"
  value       = "http://${aws_lb.prometheus.dns_name}:9090"
}

output "grafana_url" {
  description = "Grafana dashboard URL"
  value       = "http://${aws_lb.grafana.dns_name}:3000"
}

# Terraform State
output "terraform_state_bucket" {
  description = "S3 bucket for Terraform state"
  value       = "cloudforge-terraform-state"
}
