import argparse
import json
import os
import numpy as np
import yaml


def simulate_energy_function(setpoint: float, noise_std: float = 0.02) -> float:
    """
    Synthetic energy consumption function for a single setpoint.

    We model the energy intensity as a convex parabola around an optimal
    operating point.  The returned value represents relative energy use
    (e.g. MMBtu/hr) and includes a small amount of random noise.

    Parameters
    ----------
    setpoint : float
        The control setpoint to evaluate (0.0–1.0).  Values outside this
        interval will be clipped.
    noise_std : float, optional
        Standard deviation of the additive Gaussian noise, by default 0.02.

    Returns
    -------
    float
        The simulated energy intensity.
    """
    # Clip setpoint to the allowed range
    x = np.clip(setpoint, 0.0, 1.0)
    # Define the energy curve: minimum at x=0.6 with curvature
    base = 1.0  # baseline consumption
    curvature = 4.0  # larger values make the parabola sharper
    optimum = 0.6
    energy = base + curvature * (x - optimum) ** 2
    # Additive noise to simulate measurement variability
    noise = np.random.normal(0.0, noise_std)
    return energy + noise


def optimise_setpoint(max_iter: int = 20, initial: float = 0.5) -> dict:
    """
    Perform a simple optimisation loop to discover a lower‑energy setpoint.

    We perform random sampling within the [0,1] interval and keep track of
    the best (lowest energy) point found.  This simple approach
    approximates more advanced safe optimisation routines but avoids heavy
    dependencies.  The function returns the best setpoint discovered along
    with energy measurements.

    Parameters
    ----------
    max_iter : int
        Number of random evaluations to perform.
    initial : float
        Initial safe setpoint used to compute the baseline energy.

    Returns
    -------
    dict
        A dictionary containing the baseline and best energy values and
        corresponding setpoints.
    """
    # Baseline energy at the provided initial setpoint
    baseline_energy = simulate_energy_function(initial)
    best_energy = baseline_energy
    best_point = initial

    # Random search: propose candidate setpoints uniformly on [0,1]
    for _ in range(max_iter):
        candidate = np.random.uniform(0.0, 1.0)
        energy = simulate_energy_function(candidate)
        if energy < best_energy:
            best_energy = energy
            best_point = candidate

    return {
        "baseline_setpoint": initial,
        "baseline_energy": baseline_energy,
        "best_setpoint": best_point,
        "best_energy": best_energy,
    }


def main():
    parser = argparse.ArgumentParser(description="Train a simple energy optimisation model.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config.yaml",
        help="Path to configuration YAML file.",
    )
    args = parser.parse_args()

    # Load configuration
    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    # Extract optimiser settings
    max_iter = cfg.get("optimizer", {}).get("max_iter", 20)
    # Safe optimiser: use initial safe point if provided
    safe_cfg = cfg.get("optimizer", {}).get("safe", {})
    initial_point = 0.5
    if safe_cfg and safe_cfg.get("enable", False):
        # Accept a list or float for the initial safe point
        isp = safe_cfg.get("initial_safe_point")
        if isp is not None:
            if isinstance(isp, list) and len(isp) > 0:
                initial_point = float(isp[0])
            elif isinstance(isp, (int, float)):
                initial_point = float(isp)

    # Optimise the setpoint
    result = optimise_setpoint(max_iter=max_iter, initial=initial_point)

    # Compute metrics relative to baseline
    baseline_energy = result["baseline_energy"]
    best_energy = result["best_energy"]
    reduction = (baseline_energy - best_energy) / baseline_energy if baseline_energy > 0 else 0.0
    metrics = {
        "energy_intensity_reduction_percent": reduction * 100.0,
        # Assume 8 000 operating hours per year and SAR 200 per MMBtu equivalent unit
        "cost_savings_SAR_per_year": reduction * baseline_energy * 200 * 8000,
        # Assume 0.2 tonnes CO₂e per energy unit
        "co2e_avoided_tonnes_per_year": reduction * baseline_energy * 0.2 * 8000,
    }

    # Persist metrics and best setpoint
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    os.makedirs("models", exist_ok=True)
    with open("models/best_setpoint.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Optimisation complete. Metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()