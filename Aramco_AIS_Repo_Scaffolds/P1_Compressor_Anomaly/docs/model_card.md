# Model Card — P1_Compressor_Anomaly

**Intended Use**  
Advisory analytics for IsolationForest on rolling features; optional LSTM-AE; alarm budget thresholding.. Not a Safety Instrumented Function (SIS/SIF). Operators must confirm actions.

**Data**  
- Sources: Historian (PI Web API) / OPC UA (read-only).  
- Tags: flow, Ps, Pd, motor_current, temperature, vibration.  
- Sampling: 1 min (example; set to plant scan).  
- QA: units, ranges, gap policy (FFILL ≤ N min), quality flags respected.  
- Mapping: ISA-5.1 Tag→Loop/Area/Unit.

**Method**  
IsolationForest on rolling features; optional LSTM-AE; alarm budget thresholding.

**Metrics at Operating Point**  
- Discrimination: AUROC, AUPRC  
- Ops: False-alarms/hour, detection lead-time (min)  
- Threshold selection: Alarm budget of ≤ 0.1 FA/h/asset.

**Limitations**  
- Regime sensitivity, sensor failures, configuration drift, data latency.  
- Requires operator judgment; advisory only.

**Governance & Safety**  
- ISA/IEC-62443 zones & conduits; PI/OPC read-only identities; certificate-based auth.  
- NIST SP 800-82 controls.  
- Releases via MOC (OSHA 1910.119). MOC ID: <<fill>>.

**Versioning**  
- MLflow run: <<run_id>>  
- Artifact URI: <<uri>>  
- Changelog: /docs/changelog.md
