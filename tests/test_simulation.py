"""Tests for the simulation engine."""

import numpy as np

from src.simulation import (
    get_endpoints,
    simulate_multiple_walks,
    simulate_single_walk,
)


def test_single_walk_has_correct_length():
    walk = simulate_single_walk(number_of_rolls=100, random_seed=1)
    assert len(walk) == 101


def test_single_walk_starts_at_zero():
    walk = simulate_single_walk(number_of_rolls=50, random_seed=1)
    assert walk[0] == 0


def test_single_walk_never_goes_below_zero():
    walk = simulate_single_walk(number_of_rolls=300, random_seed=7)
    assert min(walk) >= 0


def test_multiple_walks_has_correct_shape():
    walks = simulate_multiple_walks(
        number_of_walks=10, number_of_rolls=100, random_seed=123
    )
    assert walks.shape == (10, 101)


def test_multiple_walks_is_reproducible():
    first = simulate_multiple_walks(20, 50, random_seed=123)
    second = simulate_multiple_walks(20, 50, random_seed=123)
    assert np.array_equal(first, second)


def test_multiple_walks_are_not_all_identical():
    walks = simulate_multiple_walks(50, 100, random_seed=123)
    assert not np.all(walks == walks[0])


def test_get_endpoints_returns_final_column():
    walks = simulate_multiple_walks(10, 100, random_seed=123)
    endpoints = get_endpoints(walks)
    assert np.array_equal(endpoints, walks[:, -1])
    assert endpoints.shape == (10,)
