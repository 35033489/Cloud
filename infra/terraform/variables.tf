variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "environment" {
  type        = string
  description = "Environment (dev, test, prod)"
}

variable "db_cluster_identifier" {
  type        = string
  description = "RDS/Aurora cluster identifier"
}

variable "db_cluster_arn" {
  type        = string
  description = "RDS/Aurora cluster ARN"
}

variable "db_secret_arn" {
  type        = string
  description = "Database credentials secret ARN"
}
