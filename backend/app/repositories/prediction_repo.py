"""
V1: запись features + prediction + audit_log.
"""

import json
from backend.app.db import get_conn

def upsert_company(conn, inn: str, name: str | None) -> int:
    with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO companies(inn, name) VALUES (%s, %s)
          ON CONFLICT (inn) DO UPDATE SET name=COALESCE(EXCLUDED.name, companies.name)
          RETURNING id
        """, (inn, name))
        return cur.fetchone()[0]

def upsert_period(conn, year: int, quarter: int | None) -> int:
    with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO reporting_periods(year, quarter) VALUES (%s, %s)
          ON CONFLICT (year, quarter) DO UPDATE SET year=EXCLUDED.year
          RETURNING id
        """, (year, quarter))
        return cur.fetchone()[0]

def upsert_features(conn, company_id: int, period_id: int, features: dict) -> int:
    with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO financial_features(company_id, period_id, features_json)
          VALUES (%s, %s, %s)
          ON CONFLICT (company_id, period_id)
          DO UPDATE SET features_json=EXCLUDED.features_json
          RETURNING id
        """, (company_id, period_id, json.dumps(features)))
        return cur.fetchone()[0]

def insert_prediction(conn, company_id: int, period_id: int, model_version: str,
                      reg_outputs: dict, risk_score: float) -> int:
    with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO predictions(company_id, period_id, model_version, reg_outputs_json, risk_score)
          VALUES (%s, %s, %s, %s, %s)
          RETURNING id
        """, (company_id, period_id, model_version, json.dumps(reg_outputs), risk_score))
        return cur.fetchone()[0]

def insert_audit(conn, actor: str, action: str, entity: str, entity_id: int | None, payload: dict):
    with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO audit_log(actor, action, entity, entity_id, payload)
          VALUES (%s, %s, %s, %s, %s)
        """, (actor, action, entity, entity_id, json.dumps(payload)))
