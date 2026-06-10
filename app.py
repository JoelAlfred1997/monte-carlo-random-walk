"""Streamlit dashboard for the Monte Carlo random walk project.

Run with:  streamlit run app.py
All heavy lifting is delegated to the reusable functions in ``src/``; this file
only wires controls, metrics, and charts together.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src import config
from src.analysis import run_sensitivity_analysis, summarize_endpoints
from src.simulation import get_endpoints, simulate_multiple_walks
from src.visualization import (
    create_plotly_endpoint_histogram,
    create_plotly_sensitivity_chart,
    create_plotly_walks_chart,
)

st.set_page_config(
    page_title="Monte Carlo Random Walk", page_icon="🎲", layout="wide"
)


# Caching means an unchanged set of inputs reuses the previous result instead of
# re-running the simulation on every interaction — the app stays snappy.
@st.cache_data(show_spinner=False)
def cached_walks(number_of_walks, number_of_rolls, random_seed, fall_probability):
    return simulate_multiple_walks(
        number_of_walks, number_of_rolls, random_seed, fall_probability
    )


@st.cache_data(show_spinner=False)
def cached_sensitivity(counts, number_of_rolls, target_step, random_seed, fall_probability):
    return run_sensitivity_analysis(
        list(counts), number_of_rolls, target_step, random_seed, fall_probability
    )


# --- Section 1: Project overview -------------------------------------------
st.title("🎲 Monte Carlo Simulation of Random Walk Outcomes")
st.markdown(
    """
**Monte Carlo simulation** estimates the probability of an uncertain outcome by
running the same random experiment many thousands of times and counting how often
each result occurs.

A **random walk** here is a person on a staircase who starts at step 0 and, for
each of 100 dice throws, moves according to simple rules. Sometimes they step
down, usually they step up, and occasionally they make a big jump.

**The question this project answers:** *What is the probability of reaching at
least the target step after all the dice throws?* There is no simple formula for
this, which is exactly when simulation shines — we let the computer play the game
tens of thousands of times and read the answer off the results.
    """
)

# --- Section 2: Simulation controls (sidebar) ------------------------------
st.sidebar.header("Simulation controls")
number_of_walks = st.sidebar.slider(
    "Number of random walks", 100, 50_000, config.DEFAULT_NUMBER_OF_WALKS, step=100
)
number_of_rolls = st.sidebar.slider(
    "Number of dice throws", 50, 500, config.DEFAULT_NUMBER_OF_ROLLS, step=10
)
target_step = st.sidebar.slider(
    "Target step", 10, 200, config.DEFAULT_TARGET_STEP, step=5
)
random_seed = st.sidebar.number_input(
    "Random seed", value=config.DEFAULT_RANDOM_SEED, step=1
)
enable_fall_risk = st.sidebar.checkbox("Enable fall risk", value=False)
fall_probability = st.sidebar.slider(
    "Fall probability", 0.0, 0.05, config.DEFAULT_FALL_PROBABILITY,
    step=0.001, format="%.3f", disabled=not enable_fall_risk,
)
sample_walks_to_display = st.sidebar.slider(
    "Number of sample walks to display", 5, 100, 20, step=5
)

effective_fall = fall_probability if enable_fall_risk else 0.0

# Run the simulation (cached) and compute statistics.
walks = cached_walks(
    number_of_walks, number_of_rolls, int(random_seed), float(effective_fall)
)
endpoints = get_endpoints(walks)
summary = summarize_endpoints(endpoints, target_step)

# --- Section 3: Key metrics -------------------------------------------------
st.subheader("Key metrics")
row1 = st.columns(4)
row1[0].metric("Success probability", f"{summary['success_probability_percent']:.1f}%")
row1[1].metric("Failure probability", f"{summary['failure_probability_percent']:.1f}%")
row1[2].metric("Average final step", f"{summary['mean_endpoint']:.1f}")
row1[3].metric("Median final step", f"{summary['median_endpoint']:.1f}")
row2 = st.columns(4)
row2[0].metric("Standard deviation", f"{summary['standard_deviation']:.1f}")
row2[1].metric("Best endpoint", summary["max_endpoint"])
row2[2].metric("Worst endpoint", summary["min_endpoint"])

# --- Section 4: Random walk visualization ----------------------------------
st.subheader("Random walk visualization")
st.plotly_chart(
    create_plotly_walks_chart(walks, sample_walks_to_display),
    use_container_width=True,
)

# --- Section 5: Endpoint distribution --------------------------------------
st.subheader("Endpoint distribution")
st.plotly_chart(
    create_plotly_endpoint_histogram(endpoints, target_step),
    use_container_width=True,
)

# --- Section 6: Sensitivity analysis ---------------------------------------
st.subheader("Sensitivity analysis")
st.caption(
    "How the probability estimate stabilizes as the number of simulations grows."
)
sensitivity_df = cached_sensitivity(
    tuple(config.DEFAULT_SENSITIVITY_COUNTS),
    number_of_rolls, target_step, int(random_seed), float(effective_fall),
)
st.dataframe(sensitivity_df, use_container_width=True)
st.plotly_chart(
    create_plotly_sensitivity_chart(sensitivity_df), use_container_width=True
)

# --- Section 7: Insights (auto-generated) ----------------------------------
st.subheader("Insights")
insight = (
    f"Based on {summary['number_of_simulations']:,} simulated walks, the "
    f"probability of reaching at least {target_step} steps is approximately "
    f"{summary['success_probability_percent']:.1f}%. The average final position "
    f"was {summary['mean_endpoint']:.1f} steps, with a standard deviation of "
    f"{summary['standard_deviation']:.1f}. "
)
if summary["success_probability_percent"] >= 50:
    insight += (
        "This suggests the target is achievable under the current dice rules, "
        "although individual walks vary significantly."
    )
else:
    insight += (
        "This suggests the target is difficult to reach under the current dice "
        "rules, and most walks fall short."
    )
st.info(insight)

# --- Section 8: Download results -------------------------------------------
st.subheader("Download results")
summary_csv = pd.DataFrame([summary]).to_csv(index=False)
sensitivity_csv = sensitivity_df.to_csv(index=False)
col_a, col_b = st.columns(2)
col_a.download_button(
    "Download endpoint summary (CSV)", summary_csv,
    file_name="endpoint_summary.csv", mime="text/csv",
)
col_b.download_button(
    "Download sensitivity analysis (CSV)", sensitivity_csv,
    file_name="sensitivity_analysis.csv", mime="text/csv",
)
