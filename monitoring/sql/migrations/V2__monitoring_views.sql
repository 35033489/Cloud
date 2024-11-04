CREATE MATERIALIZED VIEW monitoring.query_stats_hourly
AS
SELECT 
    date_trunc('hour', query_start) as hour,
    queryid,
    count(*) as execution_count,
    avg(total_exec_time) as avg_exec_time,
    sum(rows) as total_rows
FROM pg_stat_statements
GROUP BY 1, 2;

CREATE UNIQUE INDEX ON monitoring.query_stats_hourly(hour, queryid);
