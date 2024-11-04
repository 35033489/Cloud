CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

CREATE SCHEMA IF NOT EXISTS monitoring;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA monitoring TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA monitoring TO readonly;
