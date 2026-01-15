
from backend.app.db import get_conn
from backend.app.repositories.prediction_repo import (
    upsert_company, upsert_period, upsert_features, insert_prediction, insert_audit
)
from ml.predictor import predict_financial_state

def predict_and_persist(payload: dict) -> dict:
    # payload: inn, company_name, year, quarter, features[35]
    features_dict = {FEATURE_KEYS[i]: payload["features"][i] for i in range(35)}

import math

def calc_drift_score(features_dict: dict, baseline: dict) -> float:
    # ПСЕВДО: L2 расстояние между текущими значениями и baseline
    s = 0.0
    for k, v in features_dict.items():
        b = float(baseline.get(k, 0.0))
        x = float(v)
        s += (x - b) ** 2
    return math.sqrt(s)

def drift_detected(score: float, threshold: float = 100.0) -> bool:
    return score >= threshold
