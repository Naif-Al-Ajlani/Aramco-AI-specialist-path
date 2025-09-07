# P2: Simple RUL with CoxPH (lifelines); synthetic censored data + MLflow logging
import os, json, argparse, numpy as np, pandas as pd, mlflow
from lifelines import CoxPHFitter

def synth(n=120, seed=42):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({
        "usage": rng.normal(8,2,n).clip(1, 16),
        "vibration": rng.normal(1.5,0.3,n),
        "temp": rng.normal(60,5,n)
    })
    baseline = 120 - 5*X["usage"] + 8*(X["vibration"]<1.6) - 0.5*(X["temp"]-60)
    noise = rng.normal(0,10,n)
    T = (baseline + noise).clip(5, 180)
    E = (rng.random(n) < 0.6).astype(int)  # event observed
    df = X.copy(); df["T"]=T; df["E"]=E
    return df

def main(cfg):
    df = synth(n=cfg.get("n_assets",120), seed=cfg.get("seed",42))
    cph = CoxPHFitter()
    cph.fit(df, duration_col="T", event_col="E")
    cindex = float(cph.concordance_index_)
    os.makedirs(cfg.get("output_dir","artifacts"), exist_ok=True)
    with open(os.path.join(cfg.get("output_dir","artifacts"), "metrics.json"),"w") as f:
        json.dump({"C_index":cindex}, f)
    mlflow.set_experiment("P2_RUL")
    with mlflow.start_run(run_name="coxph_synth"):
        mlflow.log_metric("C_index", cindex)
        cph.save_model(os.path.join(cfg.get("output_dir","artifacts"),"coxph_model.pkl"))
    print("C-index:", cindex)

if __name__=="__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config"); args=ap.parse_args()
    cfg = {"seed":42,"n_assets":120,"output_dir":"artifacts"}
    if args.config:
        import yaml; cfg.update(yaml.safe_load(open(args.config)))
    main(cfg)
