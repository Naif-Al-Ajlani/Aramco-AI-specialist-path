# P2 – Predictive Maintenance – Remaining Useful Life

## Problem
Rotating equipment such as pumps and compressors degrade over time.  Planning maintenance too late leads to catastrophic failures, whereas replacing parts too early wastes resources.  The goal of this project is to estimate the **remaining useful life (RUL)** of assets so that maintenance can be scheduled at the optimal time.

## Data
The example uses a synthetic dataset with sensor streams (vibration, temperature, current) and work orders.  In real settings you would gather sensor tags from the historian and merge them with maintenance logs to derive failure times.  Censored samples (units still healthy at the end of observation) are handled correctly.

## Method
We frame RUL prediction as a **survival analysis** problem.  Two models are provided:
- A **Cox proportional hazards** baseline using the `lifelines` library.
- A **gradient‑boosted accelerated failure time (AFT)** model using `xgboost`’s survival objectives.

Rolling statistics are computed per signal to summarise recent behaviour.  Models output a survival function or RUL estimate along with confidence bands (via bootstrap or conformal prediction).

## Metrics
Key evaluation metrics include:
- **Concordance index (C‑index)** for ranking accuracy.
- **Calibration curves** to check whether predicted survival probabilities match observed frequencies.
- **Prediction interval coverage** to quantify uncertainty.

These metrics are computed on time‑ordered splits to respect temporal causality.

## Ops
Scripts in `src/train.py` train and evaluate the models and log results to MLflow.  Inference can be served via a simple API for integration with maintenance systems.  Grafana dashboards can display predicted RUL distributions and maintenance alerts.  Without a separate conda environment, dependencies are installed from `requirements.txt`.

## Cyber
Integration with OT data sources should use secure protocols (OPC UA or PI Web API over TLS) and adhere to least privilege access.  Compliance with ISA/IEC‑62443 and NIST SP 800‑82 guidelines is recommended.

## Value
Accurate RUL estimates enable planned maintenance, reduce unplanned downtime, optimise spares inventory and improve overall equipment effectiveness (OEE).
