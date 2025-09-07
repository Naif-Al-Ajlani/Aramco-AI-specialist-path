# Model Card – P5 Emissions & Flaring Reduction

## Model Details
- **Model type**: Seasonal decomposition plus changepoint detection with residual classification.
- **Inputs**: Time‑series tags such as flare flow rate, stack temperature, composition, steam assist and event log indicators.
- **Outputs**: Binary or categorical event flags with root‑cause tags.

## Intended Use
Identify abnormal flaring events and assign probable root causes to support compliance reporting and operator response.  The system is advisory; it does not act automatically on control systems.

## Training Data
Synthetic data with injected anomalies was used for development.  For deployment, train the detector using historical data labelled with known events and false alarms.

## Performance
Example metrics on synthetic test data:
- False alarm reduction: 35 %
- Event detection rate: 92 %
- Mean detection delay: 5 minutes

## Limitations
- Seasonal patterns may change over time; re‑training and drift monitoring are needed.
- Root‑cause tags require engineering input and may not generalise.

## Ethical & Safety Considerations
Alarm quality metrics should be communicated transparently to operators.  Regulatory reporting must be performed by qualified personnel.
