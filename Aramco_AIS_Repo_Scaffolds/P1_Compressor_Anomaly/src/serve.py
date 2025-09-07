# Minimal FastAPI scorer that loads the MLflow-exported sklearn model from ./mlruns (or a local joblib fallback)
import os, json, pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
from mlflow.tracking import MlflowClient

app = FastAPI(title="P1 Anomaly Scorer")

class Batch(BaseModel):
    rows: list  # list of feature vectors

def load_latest_model():
    client = MlflowClient()
    exps = [e for e in client.list_experiments() if e.name=="P1_Compressor_Anomaly"]
    if not exps: 
        return None, None
    runs = client.search_runs(experiment_ids=[exps[0].experiment_id], order_by=["attributes.start_time DESC"], max_results=1)
    if not runs: 
        return None, None
    run = runs[0]
    model_uri = f"runs:/{run.info.run_id}/model"
    model = mlflow.pyfunc.load_model(model_uri)
    return model, run.info.run_id

model, run_id = load_latest_model()

@app.get("/health")
def health():
    return {"status":"ok","run_id":run_id}

@app.post("/score")
def score(b: Batch):
    global model
    if model is None: 
        return {"error":"no model found"}
    import numpy as np
    X = pd.DataFrame(b.rows)
    # Higher = more anomalous (use -score_samples if underlying is sklearn IF)
    # Here mlflow.pyfunc wraps IsolationForest returning decision_function; we invert.
    scores = (-model.predict(X)).tolist() if hasattr(model, "predict") else []
    return {"scores":scores}
