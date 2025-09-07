# Model Card — P2_RUL_Predictive_Maintenance

**Intended Use**  
Advisory analytics for Cox proportional hazards on engineered features; AFT variant for comparison.. Not a Safety Instrumented Function (SIS/SIF). Operators must confirm actions.

**Data**  
- Sources: Historian (PI Web API) / OPC UA (read-only).  
- Tags: usage, vibration, temperature, work orders.  
- Sampling: Daily/weekly aggregates.  
- QA: units, ranges, gap policy (FFILL ≤ N min), quality flags respected.  
- Mapping: ISA-5.1 Tag→Loop/Area/Unit.

**Method**  
Cox proportional hazards on engineered features; AFT variant for comparison.

**Metrics at Operating Point**  
- Discrimination: C-index  
- Ops: —  
- Threshold selection: Alarm budget of —.

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
