# Model Card – P3 RAG Safety Co‑Pilot

## System Details
This service is not a single model but a pipeline consisting of:
- Document retrieval using TF‑IDF embeddings.
- Redaction filters to remove personally identifiable information (PII).
- A lightweight summariser (placeholder for your chosen LLM).
- Prompt templates enforcing operator confirmation.

## Intended Use
Provide contextual answers to operators’ questions about procedures, diagrams, MOC and incident history.  The co‑pilot is advisory and must never initiate actions.  It must always ask for human confirmation.

## Data
Documents reside in `docs/corpus/` and should only include internally approved materials.  Indexing creates vector representations for retrieval.

## Performance
We recommend evaluating:
- Citation coverage (≥ 90 % of answers contain at least one source).
- Policy compliance (0 safety violations in red‑team tests).
- Mean response time (≤ 2 seconds on cached queries).

## Limitations
- Without a full language model this reference implementation produces simple summarisation.
- Retrieval is only as good as the quality and coverage of the corpus.
- Safety relies on guardrails; misconfiguration could leak sensitive information.

## Ethical & Safety Considerations
Ensure that all responses are reviewed by qualified personnel before taking any action.  All data must stay within secure OT networks.
