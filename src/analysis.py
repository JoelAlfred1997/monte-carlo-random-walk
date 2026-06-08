"""Statistical analysis of random walk endpoints.

Takes the raw output of the simulation engine and turns it into the numbers a
human actually cares about: the probability of hitting the target, summary
statistics, and a sensitivity table.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.simulation import get_endpoints, simulate_multiple_walks


def calculate_success_probability(
    endpoints: np.ndarray,
    target_step: int = 60,
) -> float:
    """Return the percentage of walks that reached at least ``target_step``.

    Args:
        endpoints: Final positions of the walks.
        target_step: The step level we are testing against.

    Returns:
        A percentage rounded to 2 decimals. For example, ``78.4`` means 78.4%.
    """
    endpoints = np.asarray(endpoints)
    if endpoints.size == 0:
        return 0.0
    success = int(np.count_nonzero(endpoints >= target_step))
    return round(100.0 * success / endpoints.size, 2)


def summarize_endpoints(
    endpoints: np.ndarray,
    target_step: int = 60,
) -> dict:
    """Build a dictionary of summary statistics for a set of endpoints.

    Args:
        endpoints: Final positions of the walks.
        target_step: The step level used for the success/failure split.

    Returns:
        A dictionary with counts, averages, spread, the success probability,
        and key percentiles.
    """
    endpoints = np.asarray(endpoints)
    probability = calculate_success_probability(endpoints, target_step)
    return {
        "number_of_simulations": int(endpoints.size),
        "target_step": int(target_step),
        "mean_endpoint": round(float(np.mean(endpoints)), 2),
        "median_endpoint": round(float(np.median(endpoints)), 2),
        "min_endpoint": int(np.min(endpoints)),
        "max_endpoint": int(np.max(endpoints)),
        "standard_deviation": round(float(np.std(endpoints)), 2),
        "success_count": int(np.count_nonzero(endpoints >= target_step)),
        "success_probability_percent": probability,
        "failure_probability_percent": round(100.0 - probability, 2),
        "percentile_5": round(float(np.percentile(endpoints, 5)), 2),
        "percentile_25": round(float(np.percentile(endpoints, 25)), 2),
        "percentile_75": round(float(np.percentile(endpoints, 75)), 2),
        "percentile_95": round(float(np.percentile(endpoints, 95)), 2),
    }


def run_sensitivity_analysis(
    simulation_counts: list[int],
    number_of_rolls: int,
    target_step: int,
    random_seed: int,
    fall_probability: float,
) -> pd.DataFrame:
    """Re-run the simulation at several sizes to show the estimate stabilizing.

    A small simulation gives a noisy probability estimate; a large one gives a
    stable estimate. Running several sizes side by side demonstrates the core
    idea of Monte Carlo: more trials means more confidence.

    Args:
        simulation_counts: List of walk counts to try, e.g. ``[100, 1000, 10000]``.
        number_of_rolls: Dice throws per walk.
        target_step: Step level for the success test.
        random_seed: Seed for reproducibility.
        fall_probability: Per-roll fall chance (0.0 disables it).

    Returns:
        A DataFrame with one row per simulation count and the columns
        ``simulation_count``, ``success_probability_percent``,
        ``mean_endpoint`` and ``standard_deviation``.
    """
    rows = []
    for count in simulation_counts:
        walks = simulate_multiple_walks(
            number_of_walks=count,
            number_of_rolls=number_of_rolls,
            random_seed=random_seed,
            fall_probability=fall_probability,
        )
        endpoints = get_endpoints(walks)
        rows.append(
            {
                "simulation_count": int(count),
                "success_probability_percent": calculate_success_probability(
                    endpoints, target_step
                ),
                "mean_endpoint": round(float(np.mean(endpoints)), 2),
                "standard_deviation": round(float(np.std(endpoints)), 2),
            }
        )
    return pd.DataFrame(rows)
