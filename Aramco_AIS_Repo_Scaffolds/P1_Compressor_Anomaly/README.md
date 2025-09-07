# P1 — Multivariate Anomaly Detection for Compressors

## Problem
Detect early-stage faults on rotating equipment (compressors) to reduce unplanned downtime and alarm fatigue.

## Data
Tags: flow, Ps, Pd, motor_current, temperature, vibration. Historian (PI Web API) and OPC UA (read-only).

## Method
IsolationForest baseline on 30-min rolling features; threshold by alarm budget (≤0.1 FA/h/asset). Optional LSTM-AE.

## Metrics
AUROC, AUPRC, false-alarms/hour, detection lead-time (min).

## Ops Constraints
p95 < 120 ms; time-aware backtests; canary + rollback; exporter for Prometheus.

## Cyber
62443 zones/conduits; OPC UA SignAndEncrypt; PI least-privilege; MOC linkage in Model Card.

## Value
Downtime avoided (SAR), MTBF ↑, safety narrative.
