# P5 – Emissions & Flaring Anomaly Reduction

## Problem
Flaring events and emissions peaks are closely monitored by regulators and internal safety teams.  However, simple threshold systems often produce frequent false alarms due to normal operational variability.  This project aims to distinguish true anomalies from expected behaviour and to provide operators with root‑cause insights.

## Data
We expect time‑series tags such as flare flow rate, stack temperature, steam or air assist, and gas composition, along with event logs describing maintenance, pressure upsets and other disturbances.  The included example uses synthetic data with seasonal patterns and injected anomalies.

## Method
The pipeline includes:
1. **Seasonal decomposition** of each tag (e.g. via STL) to isolate residuals.
2. **Changepoint detection** on residuals using algorithms like PELT or Bayesian online changepoint detection.
3. **Event classification** based on residual signatures and contextual tags.
4. **Root‑cause tagging** where each detected event is assigned a probable cause category.

## Metrics
We report:
- **False alarm reduction (%)** relative to fixed thresholds.
- **Event detection rate** (sensitivity).
- **Detection delay (min)**.
- **Compliance metrics** tied to regulatory reporting.

## Ops
Training and inference scripts log runs to MLflow.  Prometheus and Grafana monitor detection counts, false alarm rates and event durations.  Dependencies are listed in `requirements.txt`; there is no conda environment file.

## Cyber
The system runs within the OT network using secure protocols for historian access.  It does not automatically adjust controls; it simply notifies operators.  Follow ISA/IEC‑62443 and NIST SP‑800‑82 guidelines for network segmentation and secure service deployment.

## Value
Reducing nuisance flaring alarms improves operator trust, ensures focus on genuine issues, helps meet regulatory requirements and reduces CO₂e emissions.
