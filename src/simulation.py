"""The Monte Carlo random walk simulation engine.

This module knows *one* thing: how to play the dice-driven staircase game.
Everything else (statistics, charts, the dashboard) builds on top of it.
"""

from __future__ import annotations

import numpy as np


def simulate_single_walk(
    number_of_rolls: int = 100,
    random_seed: int | None = None,
    fall_probability: float = 0.0,
) -> list[int]:
    """Simulate one random walk and return the full path of step positions.

    Args:
        number_of_rolls: How many times the dice is thrown.
        random_seed: Optional seed for reproducible results. ``None`` means
            the walk is different every time it is run.
        fall_probability: Optional per-roll chance (0.0-1.0) of slipping back
            to step 0. ``0.0`` disables the fall risk entirely.

    Returns:
        A list of step positions of length ``number_of_rolls + 1``. The first
        value is always 0 (the starting line) and no value is ever below 0.
    """
    rng = np.random.default_rng(random_seed)
    step = 0
    walk = [step]
    for _ in range(number_of_rolls):
        dice = int(rng.integers(1, 7))  # an integer from 1 to 6 inclusive
        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step = step + 1
        else:
            step = step + int(rng.integers(1, 7))
        if fall_probability > 0 and rng.random() < fall_probability:
            step = 0
        walk.append(step)
    return walk


def simulate_multiple_walks(
    number_of_walks: int = 500,
    number_of_rolls: int = 100,
    random_seed: int | None = 123,
    fall_probability: float = 0.0,
) -> np.ndarray:
    """Simulate many random walks at once using fast vectorized NumPy.

    A single random-number generator is created **once** and shared across all
    walks. This makes the whole batch reproducible from ``random_seed`` while
    keeping every individual walk different from the others.

    Args:
        number_of_walks: How many independent walks to simulate (the rows).
        number_of_rolls: Dice throws per walk (drives the number of columns).
        random_seed: Seed for reproducibility. The same seed always produces
            the same set of walks.
        fall_probability: Optional per-roll chance of slipping back to step 0.

    Returns:
        A NumPy array of shape ``(number_of_walks, number_of_rolls + 1)`` where
        each row is one walk and column 0 is always 0.
    """
    rng = np.random.default_rng(random_seed)
    walks = np.zeros((number_of_walks, number_of_rolls + 1), dtype=int)
    step = np.zeros(number_of_walks, dtype=int)
    for roll in range(1, number_of_rolls + 1):
        dice = rng.integers(1, 7, size=number_of_walks)
        six_bonus = rng.integers(1, 7, size=number_of_walks)
        delta = np.where(
            dice <= 2, -1,
            np.where(dice <= 5, 1, np.where(dice == 6, six_bonus, 0)),
        )
        step = np.maximum(step + delta, 0)  # clamp: never below 0
        if fall_probability > 0:
            fell = rng.random(number_of_walks) < fall_probability
            step = np.where(fell, 0, step)
        walks[:, roll] = step
    return walks


def get_endpoints(walks: np.ndarray) -> np.ndarray:
    """Return the final position of every walk.

    Args:
        walks: Array of shape ``(number_of_walks, number_of_rolls + 1)``.

    Returns:
        A 1-D array with the last column of ``walks`` - one endpoint per walk.
    """
    return walks[:, -1]
