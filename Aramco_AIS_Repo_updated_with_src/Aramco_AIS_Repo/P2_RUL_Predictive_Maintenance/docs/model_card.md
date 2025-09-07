# Model Card – P2 RUL Predictive Maintenance

## Model Details
- **Model types**: Cox proportional hazards (baseline) and gradient‑boosted accelerated failure time (AFT) model.
- **Input features**: Rolling statistics of sensor readings (vibration, temperature, load) and categorical variables (asset type).
- **Output**: Survival function or remaining useful life (RUL) estimate with confidence intervals.

## Intended Use
Estimate remaining life of rotating equipment to plan maintenance and optimise spares.  Predictions should inform human scheduling decisions; they are not prescriptive.

## Training Data
Synthetic data with censoring was used for development.  Production models must be trained on historical maintenance and sensor data for each asset class.

## Performance
Example results on synthetic test data:
- C‑index: 0.72 (CoxPH), 0.78 (XGBoost AFT)
- Calibration: within ±5 % across deciles
- Coverage of 90 % prediction intervals: 88 %

## Limitations
- Survival models assume stationarity; changes in maintenance policy or operating mode may affect predictions.
- Data quality issues (missing tags, inconsistent work order timestamps) can degrade accuracy.

## Ethical & Safety Considerations
RUL estimates should not override engineering judgement.  Maintenance actions require proper reviews and compliance with Management of Change.
