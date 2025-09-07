# Model Card — P3_RAG_Safety_Copilot

**Intended Use**  
Advisory analytics for Retrieval with guardrails and operator-confirm UX; advisory only.. Not a Safety Instrumented Function (SIS/SIF). Operators must confirm actions.

**Data**  
- Sources: Historian (PI Web API) / OPC UA (read-only).  
- Tags: SOPs, P&IDs, incidents, MOC.  
- Sampling: —.  
- QA: units, ranges, gap policy (FFILL ≤ N min), quality flags respected.  
- Mapping: ISA-5.1 Tag→Loop/Area/Unit.

**Method**  
Retrieval with guardrails and operator-confirm UX; advisory only.

**Metrics at Operating Point**  
- Discrimination: Citation coverage, groundedness (for LLM variant)  
- Ops: Latency, token cost (for LLM variant)  
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
