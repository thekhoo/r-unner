import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

# Environment variable pointing at the R script the Wrapper should execute.
# The model itself lives outside this repo; only the path is supplied here.
RUNNER_ENTRYPOINT_ENV = "RUNNER_ENTRYPOINT"


@dataclass
class SimulationConfig:
    script: Path
    inputs_path: Path = field(default_factory=lambda: Path("data/inputs"))
    outputs_path: Path = field(default_factory=lambda: Path("data/outputs"))
    params: dict[str, str] = field(default_factory=dict)


def load_entrypoint(env: Mapping[str, str] = os.environ) -> SimulationConfig:
    """Build the simulation config from the ``RUNNER_ENTRYPOINT`` env var.

    The model is supplied at runtime rather than living in this repo, so the
    entrypoint R script is read from the environment. Raises ``RuntimeError``
    with a clear message when the variable is missing or blank.
    """
    raw = env.get(RUNNER_ENTRYPOINT_ENV, "").strip()
    if not raw:
        raise RuntimeError(
            f"{RUNNER_ENTRYPOINT_ENV} is not set. Point it at the R entrypoint "
            "script to execute, e.g. RUNNER_ENTRYPOINT=example_model/simulate.R"
        )
    return SimulationConfig(script=Path(raw))
