import pytest
from monitoring.lambda.src.monitoring import DatabaseMonitor

def test_process_query_metrics():
    monitor = DatabaseMonitor()
    test_data = [(1, 100, 150.5, 1000)]
    metrics = monitor._process_query_metrics(test_data)
    
    assert len(metrics) == 1
    assert metrics[0]['MetricName'] == 'QueryExecutionTime'
    assert metrics[0]['Value'] == 150.5
