import boto3
import psycopg2
import os
import json
from datetime import datetime
from aws_lambda_powertools import Logger, Metrics, Tracer

logger = Logger()
metrics = Metrics()
tracer = Tracer()

class DatabaseMonitor:
    def __init__(self):
        self.session = boto3.session.Session()
        self.secretsmanager = self.session.client('secretsmanager')
        self.cloudwatch = self.session.client('cloudwatch')
        self.sns = self.session.client('sns')
        
    def get_db_connection(self):
        secret = self.secretsmanager.get_secret_value(
            SecretId=os.environ['SECRET_ARN']
        )
        credentials = json.loads(secret['SecretString'])
        return psycopg2.connect(
            host=credentials['host'],
            database=credentials['dbname'],
            user=credentials['username'],
            password=credentials['password']
        )

    @tracer.capture_method
    def collect_performance_metrics(self):
        metrics_data = []
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                # Query Performance
                cur.execute("""
                    SELECT queryid, 
                           calls, 
                           total_exec_time/calls as avg_exec_time,
                           rows/calls as avg_rows
                    FROM pg_stat_statements
                    WHERE calls > 100
                    ORDER BY total_exec_time DESC
                    LIMIT 10
                """)
                metrics_data.extend(self._process_query_metrics(cur.fetchall()))
                
                # Connection Stats
                cur.execute("""
                    SELECT count(*), state 
                    FROM pg_stat_activity 
                    GROUP BY state
                """)
                metrics_data.extend(self._process_connection_metrics(cur.fetchall()))
                
        return metrics_data

    def _process_query_metrics(self, query_data):
        metrics = []
        for query in query_data:
            metrics.append({
                'MetricName': 'QueryExecutionTime',
                'Value': query[2],
                'Unit': 'Milliseconds',
                'Dimensions': [
                    {'Name': 'QueryID', 'Value': str(query[0])}
                ]
            })
        return metrics

    def _process_connection_metrics(self, conn_data):
        metrics = []
        for conn in conn_data:
            metrics.append({
                'MetricName': 'DatabaseConnections',
                'Value': conn[0],
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'State', 'Value': conn[1]}
                ]
            })
        return metrics

    @metrics.log_metrics
    def publish_metrics(self, metrics_data):
        try:
            self.cloudwatch.put_metric_data(
                Namespace='Custom/Aurora/PostgreSQL',
                MetricData=metrics_data
            )
        except Exception as e:
            logger.error(f"Error publishing metrics: {str(e)}")
            self.sns.publish(
                TopicArn=os.environ['SNS_TOPIC_ARN'],
                Message=f"Error publishing metrics: {str(e)}"
            )
