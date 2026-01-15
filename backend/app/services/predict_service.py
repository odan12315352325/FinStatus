
from backend.app.db import get_conn
from backend.app.repositories.prediction_repo import (
    upsert_company, upsert_period, upsert_features, insert_prediction, insert_audit
)
from ml.predictor import predict_financial_state

FEATURE_KEYS = [f"f{i+1}" for i in range(35)]

def predict_and_persist(payload: dict) -> dict:
    # payload: inn, company_name, year, quarter, features[35]
    features_dict = {FEATURE_KEYS[i]: payload["features"][i] for i in range(35)}

    with get_conn() as conn:
        company_id = upsert_company(conn, payload["inn"], payload.get("company_name"))
        period_id  = upsert_period(conn, payload["year"], payload.get("quarter"))

        upsert_features(conn, company_id, period_id, features_dict)

        y = predict_financial_state(payload["features"])

        pred_id = insert_prediction(
            conn, company_id, period_id,
            y["model_version"], y["reg_outputs"], y["risk_score"]
        )

        insert_audit(conn, actor="system", action="PREDICT",
                     entity="predictions", entity_id=pred_id,
                     payload={"inn": payload["inn"], "year": payload["year"], "quarter": payload.get("quarter")})

        return {"prediction_id": pred_id, **y}
