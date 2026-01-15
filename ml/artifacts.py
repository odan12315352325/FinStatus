

from pathlib import Path
import joblib

ARTIFACTS_DIR = Path("ml_artifacts")
MODEL_PATH = ARTIFACTS_DIR / "financial_model.h5"
SCALER_PATH = ARTIFACTS_DIR / "scaler.pkl"
META_PATH   = ARTIFACTS_DIR / "meta.json"

def ensure_dir():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

def save_scaler(scaler) -> None:
    ensure_dir()
    joblib.dump(scaler, SCALER_PATH)

def load_scaler():
    return joblib.load(SCALER_PATH)

def save_meta(meta: dict) -> None:
    ensure_dir()
    META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def load_meta() -> dict:
    if not META_PATH.exists():
        return {}
    return json.loads(META_PATH.read_text(encoding="utf-8"))
