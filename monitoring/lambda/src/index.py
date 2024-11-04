from monitoring import DatabaseMonitor

def handler(event, context):
    monitor = DatabaseMonitor()
    try:
        metrics_data = monitor.collect_performance_metrics()
        monitor.publish_metrics(metrics_data)
        return {
            'statusCode': 200,
            'body': 'Metrics collected and published successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error collecting metrics: {str(e)}'
        }
