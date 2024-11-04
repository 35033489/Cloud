import pytest
import psycopg2
import os

@pytest.fixture
def db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME', 'postgres'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    yield conn
    conn.close()
