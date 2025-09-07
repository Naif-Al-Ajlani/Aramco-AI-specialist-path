# P1 – Multivariate Anomaly Detection for Compressors

## Problem
Gas plants rely on large compressors to maintain flow and pressure.  Unexpected faults can cause unplanned shutdowns, safety incidents and emissions.  This project demonstrates how to detect early signs of failure by analysing multivariate telemetry from compressors.

## Data
The reference implementation uses synthetic telemetry with six signals sampled at one‑minute intervals: **flow**, **suction pressure (Ps)**, **discharge pressure (Pd)**, **vibration**, **motor current** and **temperature**.  Real deployments should replace the simulator with data pulled from the process historian (e.g. PI System) or OPC UA servers.  Each record may optionally carry a label indicating whether a fault is underway for evaluation.

## Method
A pointwise detector such as an **Isolation Forest** or a **LSTM autoencoder** is trained on normal operating periods.  To give a pointwise model temporal context we compute rolling 30‑minute statistics for each signal (mean, standard deviation, minimum, maximum, last value and first differences).  The detector outputs an anomaly score per timestep.  A threshold is chosen by setting an alarm budget (e.g. ≤ 0.1 false alarms per hour) on a normal validation slice.  When the score exceeds the threshold an alert is raised.

## Metrics
- **AUROC** and **average precision** summarise discriminative power.
- **Precision@k** measures the fraction of true events in the top k scored samples.
- **False‑alarms per hour** quantifies alarm burden.
- **Detection delay** measures the minutes between the start of an event and the first alert.

All evaluations use time‑aware splits (train on past, test on future) to avoid leakage.

## Ops
Training and inference are captured in the `src/train.py` and `src/serve.py` scripts.  MLflow is used to log runs and persist models.  A **FastAPI** service exposes a `/score` endpoint and a **Prometheus** exporter publishes metrics.  A sample **Grafana** dashboard visualises anomaly scores, alarms and performance indicators.  For deployment, see the Dockerfile and docker‑compose configuration in this directory.

## Cyber
Industrial AI solutions must respect OT security.  This project assumes a two‑zone architecture: the model service runs in a semi‑trusted DMZ and communicates with the plant historian via HTTPS/OPC UA using `SignAndEncrypt` and certificate‑based authentication.  Network policies follow the ISA/IEC‑62443 zones/conduits concept and the code avoids making outbound internet calls.

## Value
Early detection of multivariate anomalies helps reduce unplanned downtime, protects safety and environmental targets, and lowers maintenance cost.  A well‑tuned system can deliver several minutes of lead time before a failure fully develops and can dramatically cut false alarm rates compared to static thresholds.
