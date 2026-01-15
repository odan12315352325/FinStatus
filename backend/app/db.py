
import os
import psycopg2
from contextlib import contextmanager

DSN = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/finance_ml")

@contextmanager
def get_conn():
    conn = psycopg2.connect(DSN)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
