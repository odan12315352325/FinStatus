

import math

def build_explanation(features_dict: dict, reg_outputs: dict, risk_score: float) -> dict:
    flags = []
    recommendations = []

    # пример правил (замени на свои признаки по смыслу)
    if risk_score > 0.7:
        flags.append({"factor": "Высокий интегральный риск", "severity": "high"})
        recommendations.append("Провести анализ ликвидности и оптимизировать структуру обязательств.")

    # суррогатный вклад (пример)
    contributions = []
    for k, v in features_dict.items():
        score = abs(float(v))  # псевдо
        contributions.append({"feature": k, "contribution": score})
    contributions.sort(key=lambda x: x["contribution"], reverse=True)
    top = contributions[:7]

    return {
        "risk_level": ("high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"),
        "flags": flags,
        "top_factors": top,
        "recommendations": recommendations
    }
