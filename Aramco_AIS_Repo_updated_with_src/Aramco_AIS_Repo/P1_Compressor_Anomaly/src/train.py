import argparse
import json
import os

import numpy as np
import pandas as pd
import joblib
import yaml
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score, average_precision_score


def simulate_compressor_data(n_samples: int = 1440, n_anomalies: int = 30, seed: int = 42):
    """
    Create a simple synthetic compressor dataset with correlated signals and injected anomalies.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n_samples)

    # base signals with mild seasonality
    flow = 100 + 10 * np.sin(2 * np.pi * t / 1440) + rng.normal(0, 1, n_samples)
    ps = 2.5 - 0.002 * (flow - 100) + rng.normal(0, 0.05, n_samples)
    pd = 6.0 + 0.010 * (flow - 100) + rng.normal(0, 0.08, n_samples)
    vib = 1.5 + 0.005 * (flow - 100) + rng.normal(0, 0.05, n_samples)
    current = 200 + 0.8 * (flow - 100) + rng.normal(0, 1, n_samples)
    temp = 45 + 0.03 * (current - 200)

    df = pd.DataFrame({
        "flow": flow,
        "Ps": ps,
        "Pd": pd,
        "vib": vib,
        "current": current,
        "temp": temp
    })

    labels = np.zeros(n_samples, dtype=int)

    # inject simple anomalies (vibration spikes)
    for _ in range(n_anomalies):
        idx = rng.integers(60, n_samples - 60)
        width = rng.integers(10, 30)
        df.loc[idx:idx + width, "vib"] += rng.normal(0.5, 0.1, width + 1)
        labels[idx:idx + width] = 1

    return df, labels


def make_features(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Compute rolling-window statistics for each signal to provide temporal context to a pointwise model.
    """
    feats = []
    roll = df.rolling(window, min_periods=window)
    for col in df.columns:
        feats.append(roll[col].mean().rename(f"{col}_mean"))
        feats.append(roll[col].std().rename(f"{col}_std"))
        feats.append(roll[col].min().rename(f"{col}_min"))
        feats.append(roll[col].max().rename(f"{col}_max"))
        feats.append(df[col].rename(f"{col}_last"))
        feats.append(df[col].diff().rename(f"{col}_diff"))
    X = pd.concat(feats, axis=1).dropna().reset_index(drop=True)
    return X


def main():
    parser = argparse.ArgumentParser(description="Train an IsolationForest on compressor data.")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to configuration YAML.")
    args = parser.parse_args()

    # Load configuration
    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    # Generate or load data
    df, labels = simulate_compressor_data(seed=cfg["data"]["seed"])
    window = cfg["data"]["window_size"]
    X = make_features(df, window)
    y = labels[window - 1:]

    # Split train/test chronologically
    split = int((1 - cfg["train"]["test_split_ratio"]) * len(X))
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y[:split], y[split:]

    # Fit IsolationForest on normal operating periods
    clf = IsolationForest(
        n_estimators=cfg["model"]["params"]["n_estimators"],
        contamination=cfg["model"]["params"]["contamination"],
        random_state=cfg["data"]["seed"]
    )
    clf.fit(X_train[y_train == 0])

    # Score test data
    test_scores = -clf.score_samples(X_test)
    train_scores = -clf.score_samples(X_train[y_train == 0])
    threshold = float(np.quantile(train_scores, cfg["train"]["alarm_quantile"]))

    # Evaluate metrics
    metrics = {}
    if y_test.sum() > 0:
        metrics["auroc"] = roc_auc_score(y_test, test_scores)
        metrics["average_precision"] = average_precision_score(y_test, test_scores)
    else:
        metrics["auroc"] = None
        metrics["average_precision"] = None

    # False alarms per hour
    neg_mask = (y_test == 0)
    false_positives = int(((test_scores > threshold) & neg_mask).sum())
    neg_minutes = max(int(neg_mask.sum()), 1)
    metrics["false_alarms_per_hour"] = false_positives / (neg_minutes / 60.0)
    metrics["threshold"] = threshold

    # Persist artifacts
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/isolation_forest.joblib")

    print("Training complete. Metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()