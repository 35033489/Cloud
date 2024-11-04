terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

# SNS Topic for Alerts
resource "aws_sns_topic" "monitoring_alerts" {
  name = "db-monitoring-alerts-${var.environment}"
}

# Lambda IAM Role
resource "aws_iam_role" "monitoring_lambda_role" {
  name = "db-monitoring-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "monitoring" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "db-monitoring-${var.environment}"
  role            = aws_iam_role.monitoring_lambda_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
  timeout         = 300
  memory_size     = 256

  environment {
    variables = {
      ENVIRONMENT       = var.environment
      DB_CLUSTER_ARN   = var.db_cluster_arn
      SNS_TOPIC_ARN    = aws_sns_topic.monitoring_alerts.arn
      SECRET_ARN       = var.db_secret_arn
    }
  }
}

# CloudWatch Event Rule
resource "aws_cloudwatch_event_rule" "monitoring_schedule" {
  name                = "db-monitoring-schedule-${var.environment}"
  description         = "Schedule for DB monitoring"
  schedule_expression = "rate(5 minutes)"
}

# CloudWatch Event Target
resource "aws_cloudwatch_event_target" "monitoring_target" {
  rule      = aws_cloudwatch_event_rule.monitoring_schedule.name
  target_id = "MonitoringLambda"
  arn       = aws_lambda_function.monitoring.arn
}

# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "monitoring" {
  dashboard_name = "db-monitoring-${var.environment}"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/RDS", "CPUUtilization", "DBClusterIdentifier", var.db_cluster_identifier]
          ]
          period = 300
          stat = "Average"
          region = var.aws_region
          title = "CPU Utilization"
        }
      },
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/RDS", "FreeableMemory", "DBClusterIdentifier", var.db_cluster_identifier]
          ]
          period = 300
          stat = "Average"
          region = var.aws_region
          title = "Freeable Memory"
        }
      }
    ]
  })
}
