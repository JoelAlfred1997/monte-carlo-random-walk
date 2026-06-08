"""Tests for the analysis functions."""

import numpy as np

from src.analysis import calculate_success_probability, summarize_endpoints

EXPECTED_SUMMARY_KEYS = {
    "number_of_simulations",
    "target_step",
    "mean_endpoint",
    "median_endpoint",
    "min_endpoint",
    "max_endpoint",
    "standard_deviation",
    "success_count",
    "success_probability_percent",
    "failure_probability_percent",
    "percentile_5",
    "percentile_25",
    "percentile_75",
    "percentile_95",
}


def test_success_probability_is_correct():
    endpoints = np.array([60, 70, 50, 60])  # 3 of 4 reach >= 60
    assert calculate_success_probability(endpoints, 60) == 75.0


def test_success_probability_handles_all_success():
    endpoints = np.array([100, 100])
    assert calculate_success_probability(endpoints, 60) == 100.0


def test_summary_contains_all_expected_keys():
    summary = summarize_endpoints(np.array([10, 20, 60, 80, 100]), 60)
    assert EXPECTED_SUMMARY_KEYS.issubset(summary.keys())


def test_success_count_is_correct():
    endpoints = np.array([10, 60, 61, 59, 200])  # 60, 61, 200 reach the target
    summary = summarize_endpoints(endpoints, 60)
    assert summary["success_count"] == 3


def test_failure_equals_100_minus_success():
    summary = summarize_endpoints(np.array([10, 60, 61, 59, 200]), 60)
    assert summary["failure_probability_percent"] == round(
        100 - summary["success_probability_percent"], 2
    )
