# CloudForge - Terraform Configuration
# Provider and general configuration for infrastructure resources

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }

    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    bucket = "cloudforge-terraform-state"
    key    = "cloudforge/terraform.tfstate"
    region = "us-east-1"

    dynamodb_table = "cloudforge-terraform-lock"
    encrypt        = true
  }
}

# Provider configurations
provider "aws" {
  region = var.aws_region
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  certificate_authority_data = data.aws_eks_cluster.cluster.certificate_authority_data
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.cluster.endpoint
    token                  = data.aws_eks_cluster_auth.cluster.token
    certificate_authority_data = data.aws_eks_cluster.cluster.certificate_authority_data
  }
}

# Input variables
variable "aws_region" {
  description = "AWS region for resources"
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "development"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "cloudforge-cluster"
}
