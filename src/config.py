"""Central configuration for the Monte Carlo random walk project.

All default parameters and output locations live here so that the
simulation, analysis, visualization, notebook, and dashboard layers
never hardcode magic numbers or paths of their own.
"""

from __future__ import annotations

from pathlib import Path

# --- Default simulation parameters -----------------------------------------
DEFAULT_NUMBER_OF_WALKS: int = 500
DEFAULT_NUMBER_OF_ROLLS: int = 100
DEFAULT_TARGET_STEP: int = 60
DEFAULT_RANDOM_SEED: int = 123
DEFAULT_FALL_PROBABILITY: float = 0.001

# Simulation counts used by the sensitivity analysis. Defining this here keeps
# the dashboard and notebook in sync without repeating the list.
DEFAULT_SENSITIVITY_COUNTS: list[int] = [100, 500, 1000, 5000, 10000]

# --- Project paths (resolved relative to the repository root) ---------------
BASE_DIR: Path = Path(__file__).resolve().parent.parent
OUTPUTS_DIR: Path = BASE_DIR / "outputs"
CHARTS_DIR: Path = OUTPUTS_DIR / "charts"
RESULTS_DIR: Path = OUTPUTS_DIR / "results"


def ensure_output_dirs() -> None:
    """Create the output directories if they do not already exist.

    Useful before saving charts or CSV results so callers never have to
    worry about missing folders.
    """
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
