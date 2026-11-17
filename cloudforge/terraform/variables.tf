# CloudForge - Terraform Variables
# Input variables for infrastructure configuration

# AWS Configuration
variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "AWS Access Key ID (optional, uses default chain if omitted)"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS Secret Access Key (optional, uses default chain if omitted)"
  type        = string
  sensitive   = true
}

# Environment Configuration
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"
  validation {
    condition     = contains(["development", "staging", "production"], self)
    error_message = "Environment must be one of: development, staging, production"
  }
}

# Cluster Configuration
variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "cloudforge-cluster"
}

variable "node_group_name" {
  description = "ECS node group name"
  type        = string
  default     = "cloudforge-workers"
}

variable "desired_capacity" {
  description = "Desired number of nodes"
  type        = number
  default     = 2
}

variable "max_capacity" {
  description = "Maximum number of nodes"
  type        = number
  default     = 3
}

variable "min_capacity" {
  description = "Minimum number of nodes"
  type        = number
  default     = 1
}

# Database Configuration
variable "postgres_instance_class" {
  description = "PostgreSQL instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "postgres_allocated_storage" {
  description = "PostgreSQL storage in GB"
  type        = number
  default     = 20
}

# Service Configuration
variable "gateway_service_port" {
  description = "API Gateway service port"
  type        = number
  default     = 8000
}

variable "catalog_service_port" {
  description = "Catalog service port"
  type        = number
  default     = 8001
}

variable "orders_service_port" {
  description = "Orders service port"
  type        = number
  default     = 8002
}
