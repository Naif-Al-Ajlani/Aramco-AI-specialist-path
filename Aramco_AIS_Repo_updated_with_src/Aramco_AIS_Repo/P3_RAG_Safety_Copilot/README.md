# P3 – Generative Safety Co‑Pilot (RAG)

## Problem
Operators often need to consult multiple documents—standard operating procedures, piping and instrumentation diagrams (P&IDs), management of change (MOC) records and incident reports—to resolve issues.  Searching manually is slow and error‑prone.  This project builds a **retrieval‑augmented generation (RAG)** co‑pilot that answers questions by retrieving relevant passages and generating concise summaries.  It enforces guardrails so that responses never take autonomous actions and always require human confirmation.

## Data
Place your domain documents (PDFs, Word files, text exports) into the `docs/corpus/` directory.  These might include SOPs, P&ID annotations, MOC logs and incident write‑ups.  During indexing we split documents into chunks, compute embeddings (or TF‑IDF vectors) and store them in a simple in‑memory index for retrieval.

## Method
The pipeline is implemented in `src/app.py`:
1. **Retrieval** – Query terms are matched against the corpus using TF‑IDF or embedding similarity.
2. **Filtering** – Results pass through **Presidio** for PII redaction and domain‑specific safety filters.
3. **Generation** – A prompt template combines the question and retrieved snippets and is passed to a language model.  In this reference implementation we do not call external LLMs; instead we provide a placeholder summariser.
4. **Guardrails** – The response template always cites its sources and requests operator confirmation before proceeding with any action.

## Metrics
We measure:
- **Citation coverage** – the fraction of answers with at least one source citation.
- **Policy compliance** – the rate of safety violations in red‑team tests.
- **Latency** – average response time.

## Ops
Run the service with FastAPI.  The repository contains a sample Grafana dashboard that tracks query volumes, latency, citation coverage and violations.  Extend the retrieval and generation components to integrate your preferred embedding model and LLM.

## Cyber
All documents are processed locally and remain within the plant network.  No external API calls are made.  Redaction ensures that sensitive identifiers and facility details are not surfaced.  The system must operate within the secure OT zone per ISA/IEC‑62443.

## Value
A safety co‑pilot can dramatically reduce the time required to locate procedures and past incident information, improving first‑time fix rates while ensuring that only authorised personnel make decisions.
