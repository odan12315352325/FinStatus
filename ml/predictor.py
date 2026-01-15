

import numpy as np
from tensorflow.keras.models import load_model
from ml.artifacts import MODEL_PATH, load_scaler, load_meta

def predict_financial_state(x_vector_35: list[float]) -> dict:
    assert len(x_vector_35) == 35

    scaler = load_scaler()
    model = load_model(MODEL_PATH)
    meta = load_meta()  # {"model_version":"1.0.1", ...}

    x = np.array([x_vector_35], dtype=float)
    x_scaled = scaler.transform(x)

    # модель возвращает несколько выходов: 11 регрессий + 1 классификация
    y = model.predict(x_scaled)

    # ПСЕВДО: привести к единому виду
    reg_11 = y[0][0] if isinstance(y, list) else y[0]
    risk   = float(y[-1][0][0]) if isinstance(y, list) else float(y[-1])

    return {
        "model_version": meta.get("model_version", "1.0.1"),
        "reg_outputs": {f"y{i+1}": float(reg_11[i]) for i in range(11)},
        "risk_score": risk
    }
