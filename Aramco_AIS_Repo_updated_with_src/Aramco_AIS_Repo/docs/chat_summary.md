# Project Background and Design Rationale

This repository contains five research‑grade example projects developed in response to the Aramco Artificial Intelligence Specialist (AIS) job description.  The content was derived from a long technical conversation that walked through career planning, domain‑specific requirements, study plans, project outlines, code prototypes and best‑practice recommendations.

## Conversation highlights

- **Role analysis** – The AIS role blends machine‑learning engineering and AI engineering.  To satisfy Aramco’s requirements we designed a path that is roughly 65 % predictive analytics (time‑series modelling, survival analysis, optimisation) and 35 % generative AI (retrieval‑augmented generation, guardrails and product integration).
- **Study plans** – We drafted an eight‑semester bachelor plan for ML engineers and AI engineers, then combined them to target Oil & Gas applications.  These plans include statistics, deep learning, time‑series analysis, survival/risk models, MLOps, cybersecurity, retrieval techniques and product design.
- **Career & portfolio map** – A 180‑day execution plan was created with five portfolio projects (P1–P5).  Each project is tightly aligned to safety, environment, energy and efficiency use‑cases in Gas Operations.  Metrics such as false‑alarms per hour, lead‑time, concordance index, energy reduction and CO₂e avoided were emphasised.
- **Prototype code** – We implemented synthetic compressor telemetry generators, Isolation Forest and LSTM‑autoencoder detectors, survival models with conformal intervals, a minimal RAG safety co‑pilot, a safe Bayesian optimisation loop and a seasonal change‑point detector.  These examples demonstrate how to build, evaluate and deploy models while obeying time‑aware splits and alarm budget thresholds.
- **Best practices** – Guidance was provided on OT/ICS cybersecurity (ISA/IEC‑62443, NIST SP 800‑82), Management of Change (OSHA 1910.119), data quality, drift monitoring, value tracking, MLOps/MLflow, Prometheus/Grafana observability, and Business Intelligence (Power BI) dashboards.
- **Application documents** – A board pack, portfolio READMEs, resume and cover letter templates were generated, along with repo scaffolds, model cards and dashboards.

This file consolidates those discussions to explain why the repository looks the way it does and to ensure that any reader can trace the reasoning behind the chosen architectures, metrics and tooling.  Feel free to adapt or extend these projects for your own learning or to meet your organisation’s needs.
