# Model Card – P4 Energy & Setpoint Optimization

## Model Details
- **Model type**: Safe Bayesian optimisation (e.g. SafeOpt).
- **Objective**: Minimise energy intensity while keeping control variables within safe envelopes.
- **Inputs**: Historical process variables, energy consumption, ambient conditions.
- **Outputs**: Next recommended setpoint and expected energy saving.

## Intended Use
Recommend setpoint adjustments that operators can review and implement.  The optimiser should not directly write to control systems.

## Training Data
Synthetic data is used in this reference implementation.  Real deployments require historical setpoint, energy and ambient data aggregated at consistent intervals.

## Performance
Example results on synthetic data:
- Energy intensity reduction: 3 %
- SAR savings: 1.2 M SAR/year (scaled)
- CO₂e avoided: 8 kt/year (estimate)

## Limitations
- Optimiser suggestions are only as good as the baseline model and safe envelopes.
- Exogenous factors (upstream process changes, equipment fouling) can affect energy.

## Ethical & Safety Considerations
Recommendations must stay within safe operating limits and require operator approval.  Involve process engineers and apply Management of Change processes.
