from backend.app.services.explain_service import build_explanation

def predict_and_persist(payload: dict) -> dict:
    ...
    features_dict = {FEATURE_KEYS[i]: payload["features"][i] for i in range(35)}
    ...
    y = predict_financial_state(payload["features"])

    explanation = build_explanation(features_dict, y["reg_outputs"], y["risk_score"])

    pred_id = insert_prediction(...)
    update explanation_json
    with conn.cursor() as cur:
        cur.execute("UPDATE predictions SET explanation_json=%s WHERE id=%s",
                    (json.dumps(explanation), pred_id))
    ...
    return {"prediction_id": pred_id, **y, "explanation": explanation}
