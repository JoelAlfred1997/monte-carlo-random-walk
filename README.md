# Monte Carlo Simulation of Random Walk Outcomes

A clean, portfolio-ready Monte Carlo simulation that estimates the probability of
reaching a target step level in a dice-driven random walk, with an interactive
Streamlit dashboard.

> This project demonstrates core data science skills including simulation,
> probability estimation, statistical summarization, sensitivity analysis, data
> visualization, and interactive dashboard development.

## Project summary

A person starts at step 0 and throws a dice 100 times. Simple rules decide
whether they step down, step up, or jump forward. This project simulates the game
thousands of times to estimate the probability of reaching a target step — an
answer that has no clean closed-form formula.

## Business / statistical question

**What is the probability of reaching at least 60 steps after 100 dice throws?**

## Why this project matters

It demonstrates how Monte Carlo simulation answers probability questions that are
awkward to solve analytically, using nothing more than clear, reusable code and
repeated random trials. The same pattern — simulate many times, then measure —
applies to risk modelling, forecasting, and decision-making under uncertainty.

## Simulation rules

For each of the dice throws, the current step changes as follows:

- **Dice 1–2** → step down 1 (never below 0): `step = max(0, step - 1)`
- **Dice 3–5** → step up 1: `step = step + 1`
- **Dice 6** → step up by a random 1–6: `step = step + randint(1, 7)`
- **Optional fall risk** → a small per-throw chance of slipping back to step 0

Every walk starts at step 0, has length `number_of_rolls + 1`, and never goes
below zero.

## Tech stack

Python 3.11+, NumPy, pandas, matplotlib, plotly, Streamlit, pytest.

## Repository structure

```
monte-carlo-random-walk/
├── README.md
├── requirements.txt
├── app.py                      # Streamlit dashboard (UI only)
├── notebooks/
│   └── 01_random_walk_analysis.ipynb
├── src/
│   ├── config.py               # default parameters and paths
│   ├── simulation.py           # the simulation engine
│   ├── analysis.py             # probability, summary stats, sensitivity
│   └── visualization.py        # matplotlib + plotly charts
├── tests/
│   ├── test_simulation.py
│   └── test_analysis.py
├── outputs/                    # saved charts and CSV results
└── data/                       # placeholder (project is simulation-driven)
```

All business logic lives in `src/`; the dashboard and notebook only call into it.

## Dashboard features

- Adjustable number of walks, dice throws, target step, random seed and fall risk
- Live key metrics (success/failure probability, mean, median, spread, best/worst)
- Interactive walk paths and an endpoint histogram with a clear target marker
- Sensitivity analysis showing the estimate stabilizing as simulations increase
- Auto-generated written insight and CSV downloads of the results

## How to run locally

```bash
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Example commands

```bash
pytest -q                 # run the test suite
streamlit run app.py      # launch the interactive dashboard
jupyter notebook          # open notebooks/01_random_walk_analysis.ipynb
```

## Key outputs

- An interactive dashboard of probabilities and distributions
- Saved charts in `outputs/charts/` and CSV summaries in `outputs/results/`
- A narrative notebook walking through the analysis end to end

## Portfolio value

A focused mini-project that cleanly shows:

- **Python fundamentals** and a clean, testable project structure
- **Probability and simulation** thinking (Monte Carlo, law of large numbers)
- **Data visualization** with both static and interactive charts
- **Dashboarding** with Streamlit

It is presented honestly as a simulation and statistics project — not machine
learning — and is not intended to replace a full ML project.

## Future improvements

- Confidence intervals around the probability estimate
- Configurable dice rules directly from the dashboard
- Side-by-side comparison of multiple rule sets

## Author note

Built as a focused mini-project to practise simulation, probability, and
dashboarding, with reusable tested code and a reproducible workflow.
