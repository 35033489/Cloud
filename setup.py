from setuptools import setup, find_packages

setup(
    name="aws-db-monitoring",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'boto3>=1.26.137',
        'psycopg2-binary>=2.9.6',
        'aws-lambda-powertools>=2.15.0',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AWS RDS/Aurora PostgreSQL Monitoring Solution",
    keywords="aws,rds,aurora,postgresql,monitoring",
)
