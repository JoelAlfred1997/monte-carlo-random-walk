"""Plotting helpers for the random walk project.

matplotlib functions create static charts that can be saved to disk.
plotly functions return interactive figures for the Streamlit dashboard.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_sample_walks(
    walks: np.ndarray,
    max_walks_to_plot: int = 20,
    save_path: str | None = None,
) -> plt.Figure:
    """Plot a subset of random walks as a static matplotlib line chart."""
    count = min(max_walks_to_plot, walks.shape[0])
    x_axis = np.arange(walks.shape[1])
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(count):
        ax.plot(x_axis, walks[i], alpha=0.6, linewidth=1)
    ax.set_title(f"Sample of {count} Random Walks")
    ax.set_xlabel("Dice throw number")
    ax.set_ylabel("Step position")
    ax.grid(True, alpha=0.3)
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_endpoint_histogram(
    endpoints: np.ndarray,
    target_step: int = 60,
    save_path: str | None = None,
) -> plt.Figure:
    """Plot a static histogram of final positions with a target marker line."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(endpoints, bins=30, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax.axvline(
        target_step, color="red", linestyle="--", linewidth=2,
        label=f"Target = {target_step}",
    )
    ax.set_title("Distribution of Final Step Positions")
    ax.set_xlabel("Final step position")
    ax.set_ylabel("Number of walks")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def create_plotly_walks_chart(
    walks: np.ndarray,
    max_walks_to_plot: int = 20,
) -> go.Figure:
    """Return an interactive Plotly line chart of sample walks."""
    count = min(max_walks_to_plot, walks.shape[0])
    x_axis = list(range(walks.shape[1]))
    fig = go.Figure()
    for i in range(count):
        fig.add_trace(
            go.Scatter(
                x=x_axis, y=walks[i], mode="lines",
                line=dict(width=1), opacity=0.6, showlegend=False,
            )
        )
    fig.update_layout(
        title=f"Sample of {count} Random Walks",
        xaxis_title="Dice throw number",
        yaxis_title="Step position",
        template="plotly_white",
    )
    return fig


def create_plotly_endpoint_histogram(
    endpoints: np.ndarray,
    target_step: int = 60,
) -> go.Figure:
    """Return an interactive Plotly histogram with a clear target marker."""
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(x=endpoints, nbinsx=30, marker_color="#4C72B0",
                     name="Final positions")
    )
    fig.add_vline(
        x=target_step, line_dash="dash", line_color="red",
        annotation_text=f"Target = {target_step}", annotation_position="top",
    )
    fig.update_layout(
        title="Distribution of Final Step Positions",
        xaxis_title="Final step position",
        yaxis_title="Number of walks",
        template="plotly_white",
    )
    return fig


def create_plotly_sensitivity_chart(sensitivity_df: pd.DataFrame) -> go.Figure:
    """Return a Plotly line chart of probability vs number of simulations."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=sensitivity_df["simulation_count"],
            y=sensitivity_df["success_probability_percent"],
            mode="lines+markers",
        )
    )
    fig.update_layout(
        title="Probability Estimate vs Number of Simulations",
        xaxis_title="Number of simulations (log scale)",
        yaxis_title="Success probability (%)",
        template="plotly_white",
    )
    fig.update_xaxes(type="log")
    return fig
