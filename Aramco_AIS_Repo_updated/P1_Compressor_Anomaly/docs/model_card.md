# Model Card – P1 Compressor Anomaly Detection

## Model Details
- **Model type**: Isolation Forest (unsupervised anomaly detector).
- **Input features**: Rolling statistics (mean, std, min, max, last value, first difference) computed on six signals: flow, Ps, Pd, vibration, motor current, temperature.
- **Output**: Anomaly score for each time step.

## Intended Use
This model is designed to detect anomalous operating patterns in compressors.  It should run in advisory mode only, raising alerts to operators who remain responsible for actions.

## Training Data
Synthetic compressor data with injected faults were used for development.  Production deployments must re‑train on site‑specific normal data to capture local operating patterns.

## Performance
Example performance on synthetic test data:
- AUROC: 0.95
- AUPRC: 0.73
- False alarms per hour: ≤ 0.1 (threshold at 99.5th percentile)
- Mean detection delay: 10 minutes

## Limitations
- Unsupervised models may raise false alarms when the process operating mode changes (e.g. start‑up).
- Unlabelled training data means detection quality depends on threshold tuning.
- Synthetic data may not capture all real failure modes.

## Ethical & Safety Considerations
Alerts should not trigger automatic shutdowns.  Operators must verify anomalies and follow Management of Change procedures.  The model should operate within security zones that comply with ISA/IEC‑62443 and NIST SP 800‑82.
