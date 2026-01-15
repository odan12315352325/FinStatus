
def build_report(prediction: dict) -> dict:
    return {
        "title": "Отчёт по прогнозу финансового состояния",
        "model_version": prediction["model_version"],
        "risk_score": prediction["risk_score"],
        "reg_outputs": prediction["reg_outputs"],
        "explanation": prediction.get("explanation", {})
    }
