# P4 – Energy & Setpoint Optimization

## Problem
Gas processing units consume large amounts of energy.  Operators often leave control setpoints unchanged for long periods because exploring new settings manually is risky.  This project demonstrates how to minimise energy usage while respecting safe operating envelopes by automatically recommending setpoint adjustments.

## Data
Inputs include historical energy consumption (e.g. MMBtu, kWh), control setpoints (temperatures, pressures, flows), ambient conditions and other process variables.  For demonstration we use a synthetic dataset; real deployments should extract these tags from the historian.

## Method
We use **safe Bayesian optimisation** to explore the trade‑off between energy consumption and safety limits:
1. Estimate a baseline consumption curve using STL decomposition.
2. Define safe envelopes based on operating manuals or control room limits.
3. Use Ax/BoTorch to propose new setpoints that reduce energy within the envelope.
4. Update the model with observed outcomes and iterate.

## Metrics
- **Energy intensity reduction (%)** relative to the baseline.
- **Cost savings (SAR/year)** from reduced fuel or electricity.
- **CO₂e avoided** using published conversion factors.

## Ops
The training script logs experiments to MLflow.  The optimiser can be served via an API that suggests next setpoints.  A sample Grafana dashboard tracks energy consumption, suggested versus actual setpoints and cumulative savings.  See `requirements.txt` for dependencies; the `conda.yaml` file has been removed in favour of pip.

## Cyber
Only read access to process data is required.  Any setpoint recommendations must go through operator approval and should not be applied automatically.  Adhere to process safety standards and Management of Change procedures.

## Value
Even modest efficiency improvements (2–5 %) translate to significant cost savings and lower emissions when scaled across a gas plant or company.
