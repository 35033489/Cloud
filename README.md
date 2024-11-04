# AWS RDS/Aurora PostgreSQL Monitoring Solution

This repository contains a complete solution for monitoring AWS RDS/Aurora PostgreSQL databases through a CI/CD pipeline.

## Prerequisites

- AWS Account with appropriate permissions
- GitHub repository with Actions enabled
- PostgreSQL database running on RDS/Aurora
- Terraform installed locally for testing

## Setup Instructions

### 1. GitHub Secrets

Add the following secrets to your GitHub repository:

```plaintext
AWS_REGION                 # AWS region where resources will be deployed
AWS_ROLE_ARN              # ARN of IAM role for GitHub Actions
TF_STATE_BUCKET           # S3 bucket for Terraform state
TEST_DB_HOST              # Test database hostname
TEST_DB_USER              # Test database username
TEST_DB_PASSWORD          # Test database password
PROD_DB_HOST              # Production database hostname
PROD_DB_USER              # Production database username
PROD_DB_PASSWORD          # Production database password
```

### 2. Environment Configuration

1. Create environments in GitHub:
   - test
   - production

2. Configure environment protection rules:
   - Required reviewers for production
   - Environment-specific secrets

### 3. AWS Resources Required

- S3 bucket for Terraform state
- IAM role for GitHub Actions with necessary permissions
- RDS/Aurora PostgreSQL instances
- SecretsManager secrets for database credentials

### 4. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/unit/
pytest tests/integration/

# Local Terraform testing
cd infra/terraform
terraform init
terraform plan -var-file=environments/dev.tfvars
```

## Directory Structure

```plaintext
.
├── .github/workflows/          # GitHub Actions workflows
├── infra/terraform/           # Terraform configurations
├── monitoring/               # Monitoring code
│   ├── lambda/              # Lambda functions
│   └── sql/                # SQL migrations
└── tests/                  # Test suites
```

## Deployment

The solution uses a GitOps approach with the following workflow:

1. Development
   - Create feature branch
   - Implement changes
   - Run local tests
   - Create pull request

2. Testing
   - Automated tests run
   - Changes deployed to test environment
   - Integration tests run

3. Production
   - Manual approval required
   - Changes deployed to production
   - Monitoring begins

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create pull request

## Confluence 
https://cloud-dba.atlassian.net/wiki/x/AYCnB
