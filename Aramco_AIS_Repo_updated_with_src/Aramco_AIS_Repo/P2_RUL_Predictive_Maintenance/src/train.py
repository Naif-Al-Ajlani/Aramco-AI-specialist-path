import argparse
import json
import os

import numpy as np
import pandas as pd
import yaml
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index


def simulate_rul_dataset(n_samples: int = 300, seed: int = 42):
    """
    Generate a simple synthetic remaining useful life dataset.
    Each sample represents a piece of rotating equipment with vibration and temperature features.
    The time_to_event follows an exponential distribution; 30 % of samples are censored.
    """
    rng = np.random.default_rng(seed)
    vibration = rng.normal(0.5, 0.1, n_samples)
    temperature = rng.normal(50, 5, n_samples)
    baseline_hazard = 0.01 + 0.05 * vibration + 0.03 * (temperature - 50)
    # Exponential survival times
    time_to_event = rng.exponential(1 / baseline_hazard)
    # Random censoring: 30 % censored
    censor_mask = rng.random(n_samples) < 0.3
    observed_time = np.where(censor_mask, time_to_event * 0.7, time_to_event)
    event_observed = (~censor_mask).astype(int)

    df = pd.DataFrame({
        "vibration": vibration,
        "temperature": temperature,
        "duration": observed_time,
        "event": event_observed
    })
    return df


def main():
    parser = argparse.ArgumentParser(description="Train a Cox proportional hazards model on synthetic RUL data.")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to configuration YAML.")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    df = simulate_rul_dataset()

    # Split into train/test in time order (here random order because synthetic)
    split = int((1 - cfg["train"]["test_split_ratio"]) * len(df))
    train_df = df.iloc[:split].copy()
    test_df = df.iloc[split:].copy()

    # Fit Cox proportional hazards model
    cph = CoxPHFitter()
    cph.fit(train_df, duration_col="duration", event_col="event", show_progress=False)

    # Evaluate concordance on test set
    ci = concordance_index(test_df["duration"], -cph.predict_partial_hazard(test_df), test_df["event"])

    metrics = {"concordance_index": ci}

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    os.makedirs("models", exist_ok=True)
    cph.save("models/coxph_model.pkl")

    print("Training complete. Metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()