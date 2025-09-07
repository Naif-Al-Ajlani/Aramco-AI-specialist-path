# P2 — Remaining Useful Life (RUL) Prediction

**Goal:** RUL estimates for planned maintenance & spares optimization.  
**Method:** CoxPH baseline with synthetic censored data (swap in plant data later); XGB-AFT variant recommended.  
**Metrics:** C-index, calibration.  
**Ops:** Batch scoring; MLflow registry.
