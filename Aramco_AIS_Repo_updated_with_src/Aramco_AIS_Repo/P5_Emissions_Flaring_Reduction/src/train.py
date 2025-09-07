import argparse
import json
import os
from dataclasses import dataclass
from typing import List, Tuple, Dict

import numpy as np
import pandas as pd
import yaml
from ruptures import Pelt
from ruptures.costs import CostRbf


@dataclass
class AnomalyEvent:
    start: int
    duration: int


def simulate_flare_data(
    n_samples: int = 2880,
    n_anomalies: int = 4,
    anomaly_duration_range: Tuple[int, int] = (30, 90),
    seed: int = 7,
) -> Tuple[pd.Series, np.ndarray, List[AnomalyEvent]]:
    """
    Generate synthetic flare flow data with a seasonal pattern and injected anomalies.

    Parameters
    ----------
    n_samples : int
        Number of time steps to simulate (e.g. minutes).
    n_anomalies : int
        Number of anomalous events to inject.
    anomaly_duration_range : tuple
        Minimum and maximum duration (in samples) of each anomaly.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.Series
        The flare flow time series.
    np.ndarray
        A binary label array (1 during anomaly).
    list of AnomalyEvent
        Metadata about each injected anomaly (start index and length).
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n_samples)
    # Seasonal baseline: daily sinusoidal pattern with noise
    baseline = 5.0 + 1.0 * np.sin(2 * np.pi * t / 1440) + rng.normal(0, 0.2, n_samples)
    labels = np.zeros(n_samples, dtype=int)
    events: List[AnomalyEvent] = []

    # Inject step anomalies representing flaring events
    for _ in range(n_anomalies):
        start = rng.integers(120, n_samples - 120)
        dur = rng.integers(anomaly_duration_range[0], anomaly_duration_range[1])
        amplitude = rng.uniform(1.5, 2.5)
        baseline[start : start + dur] += amplitude
        labels[start : start + dur] = 1
        events.append(AnomalyEvent(start=start, duration=int(dur)))

    return pd.Series(baseline, name="flare_flow"), labels, events


def baseline_threshold_detector(series: pd.Series) -> List[int]:
    """
    Simple fixed-threshold detector: flags indices where the value exceeds
    mean + 3*std.  Returns a list of detected index positions.
    """
    mean = series.mean()
    std = series.std()
    thr = mean + 3 * std
    return [i for i, v in enumerate(series) if v > thr]


def changepoint_detector(series: pd.Series, penalty: float = 10.0) -> List[int]:
    """
    Detect change points in a time series using the PELT algorithm with an
    RBF cost function.  Returns the indices where changes are detected.
    """
    algo = Pelt(cost=CostRbf()).fit(series.values)
    # Pelt returns last index equal to n_samples; exclude it
    bkps = algo.predict(pen=penalty)[:-1]
    return bkps


def match_detections_to_events(detections: List[int], events: List[AnomalyEvent]) -> Tuple[int, int, List[int]]:
    """
    Match detected change points to injected anomalies.

    Parameters
    ----------
    detections : list of int
        Indices flagged as change points or anomalies.
    events : list of AnomalyEvent
        The ground truth anomaly windows.

    Returns
    -------
    int
        Number of true positives.
    int
        Number of false positives.
    list of int
        Detection delays (in samples) for each true positive.  If no detection
        occurs within a given event window, the delay equals the event duration.
    """
    tp = 0
    fp = 0
    delays = []
    for det in detections:
        matched = False
        for event in events:
            if event.start <= det < event.start + event.duration:
                tp += 1
                delays.append(det - event.start)
                matched = True
                break
        if not matched:
            fp += 1
    # Account for missed events: assign full duration as delay
    missed = len(events) - tp
    delays.extend([event.duration for event in events[tp:]])
    return tp, fp, delays


def main():
    parser = argparse.ArgumentParser(description="Train and evaluate an emissions/flaring anomaly detector.")
    parser.add_argument(
        "--config", type=str, default="configs/config.yaml", help="Path to configuration YAML file."
    )
    args = parser.parse_args()

    # Load configuration (unused currently but available for future extensions)
    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    # Simulate data and anomalies
    # Use the seed from the config if provided; default to 13 otherwise
    series, labels, events = simulate_flare_data(seed=cfg.get("data", {}).get("seed", 13))

    # Baseline detector (fixed threshold)
    baseline_detections = baseline_threshold_detector(series)
    # Change‑point detector (PELT)
    # Penalty for the change‑point detector can be specified under
    # ``changepoint.penalty``; fall back to 10.0 if not set.
    cp_penalty = cfg.get("changepoint", {}).get("penalty", 10.0)
    cp_detections = changepoint_detector(series, penalty=cp_penalty)

    # Evaluate baseline
    baseline_tp, baseline_fp, _ = match_detections_to_events(baseline_detections, events)
    baseline_fpr = baseline_fp  # number of false positives as proxy for false alarm count

    # Evaluate change‑point model
    tp, fp, delays = match_detections_to_events(cp_detections, events)
    fpr = fp
    detection_rate = tp / len(events) if events else 0.0
    mean_delay = float(np.mean(delays)) if delays else 0.0

    # Compute false alarm reduction (%): (baseline_fp - fp) / baseline_fp
    if baseline_fpr > 0:
        reduction = (baseline_fpr - fpr) / baseline_fpr
    else:
        reduction = 0.0

    metrics = {
        "false_alarm_reduction_percent": reduction * 100.0,
        "event_detection_rate": detection_rate,
        "average_detection_delay_minutes": mean_delay,
    }

    # Persist metrics
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("Evaluation complete. Metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()