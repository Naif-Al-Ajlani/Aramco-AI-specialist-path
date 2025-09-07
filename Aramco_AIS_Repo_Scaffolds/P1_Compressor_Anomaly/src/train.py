# P1: Train IsolationForest on synthetic compressor data and log to MLflow
import os, json, argparse, yaml, numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score, average_precision_score
import mlflow

def simulate(minutes=2880, seed=42):
    rng = np.random.default_rng(seed)
    t = np.arange(minutes)
    flow = 100 + 15*np.sin(2*np.pi*t/1440.0) + rng.normal(0, 1.5, minutes)
    Ps = 2.5 - 0.002*(flow - 100) + rng.normal(0, 0.05, minutes)
    Pd = 6.0 + 0.010*(flow - 100) + rng.normal(0, 0.08, minutes)
    current = 200 + 0.8*(flow - 100) + 0.002*(flow - 100)**2 + rng.normal(0, 1.8, minutes)
    vib = 1.5 + 0.005*(flow - 100) + rng.normal(0, 0.05, minutes)
    temp = np.zeros(minutes); base_temp = 45.0; alpha = 0.02
    temp[0] = base_temp + 0.03*(current[0] - 200)
    for i in range(1, minutes):
        target = base_temp + 0.03*(current[i] - 200)
        temp[i] = (1 - alpha)*temp[i-1] + alpha*target + rng.normal(0, 0.05)
    # Inject two events
    labels = np.zeros(minutes, dtype=np.int8)
    s, d = int(0.35*minutes), 60
    vib[s:s+d] += 0.8; labels[s:s+d]=1
    s2, d2 = int(0.7*minutes), 150
    temp[s2:s2+d2] += np.linspace(0, 5, d2); labels[s2:s2+d2]=1
    df = pd.DataFrame({"flow":flow,"Ps":Ps,"Pd":Pd,"current":current,"vib":vib,"temp":temp})
    return df, labels

def make_rolling(df, win=30):
    roll = df.rolling(win, min_periods=win)
    feats = []
    for c in df.columns:
        feats += [roll[c].mean().rename(f"{c}_mean"),
                  roll[c].std().rename(f"{c}_std"),
                  roll[c].min().rename(f"{c}_min"),
                  roll[c].max().rename(f"{c}_max"),
                  df[c].rename(f"{c}_last"),
                  df[c].diff().rename(f"{c}_diff")]
    X = pd.concat(feats, axis=1).dropna().reset_index(drop=True)
    return X

def main(cfg):
    os.makedirs(cfg["output_dir"], exist_ok=True)
    df, y = simulate(minutes=cfg["train_minutes"]+cfg["val_minutes"], seed=cfg["seed"])
    X = make_rolling(df, win=cfg["window_minutes"])
    y = y[cfg["window_minutes"]-1:]
    split = int(0.75*len(X))
    Xtr, Xte = X.iloc[:split], X.iloc[split:]
    ytr, yte = y[:split], y[split:]
    Xtr_norm = Xtr[ytr==0]
    iforest = IsolationForest(n_estimators=cfg["iforest"]["n_estimators"],
                              contamination=cfg["iforest"]["contamination"],
                              random_state=cfg["seed"])
    iforest.fit(Xtr_norm)
    s_tr = -iforest.score_samples(Xtr_norm)
    s_te = -iforest.score_samples(Xte)
    thr = float(np.quantile(s_tr, 0.995))
    auroc = float(roc_auc_score(yte, s_te))
    aupr = float(average_precision_score(yte, s_te))
    neg = (yte==0)
    fp = int(((s_te>thr)&neg).sum()); neg_minutes=int(neg.sum())
    fa_per_hour = 60.0*fp/max(neg_minutes,1)
    metrics = {"AUROC":auroc,"AUPRC":aupr,"threshold":thr,"FA_per_hour":fa_per_hour}
    with open(os.path.join(cfg["output_dir"], "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    # MLflow
    mlflow.set_experiment("P1_Compressor_Anomaly")
    with mlflow.start_run(run_name="iforest_baseline"):
        for k,v in metrics.items(): mlflow.log_metric(k, v)
        mlflow.log_params({"window":cfg["window_minutes"],"n_estimators":cfg["iforest"]["n_estimators"]})
        mlflow.sklearn.log_model(iforest, artifact_path="model")
        mlflow.log_artifact(os.path.join(cfg["output_dir"], "metrics.json"))
    print("Saved metrics:", metrics)

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    main(cfg)
