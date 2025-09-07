from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="Compressor Anomaly Service")
_model = None
_feature_columns = ["flow", "Ps", "Pd", "vib", "current", "temp"]


def load_model():
    global _model
    if _model is None:
        # Load the trained IsolationForest model from disk
        path = os.path.join("models", "isolation_forest.joblib")
        if not os.path.exists(path):
            raise RuntimeError(f"Model file not found at {path}. Please run train.py first.")
        _model = joblib.load(path)


class Sample(BaseModel):
    values: list  # expects a list of 6 numeric values matching the feature order


@app.on_event("startup")
def startup_event():
    load_model()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
def score(sample: Sample):
    """
    Score a single sample.  The client must send a JSON body like:
      {"values": [flow, Ps, Pd, vib, current, temp]}
    Returns an anomaly score where higher means more anomalous.
    """
    load_model()
    if len(sample.values) != len(_feature_columns):
        return {"error": f"Expected {len(_feature_columns)} values but received {len(sample.values)}"}
    x = pd.DataFrame([sample.values], columns=_feature_columns)
    # IsolationForest outputs negative scores; invert sign so that higher = more anomalous
    score_value = float(-_model.score_samples(x)[0])
    return {"anomaly_score": score_value}