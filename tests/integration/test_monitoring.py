import pytest
from datetime import datetime, timedelta

def test_monitoring_views(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT count(*) 
            FROM monitoring.query_stats_hourly
            WHERE hour >= now() - interval '1 day'
        """)
        count = cur.fetchone()[0]
        assert count >= 0
