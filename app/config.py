from pathlib import Path

from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Environment variable pointing at the R script the runner should execute.
# The model itself lives outside this repo; only the path is supplied here.
RUNNER_ENTRYPOINT_ENV = "RUNNER_ENTRYPOINT"


class SimulationConfig(BaseSettings):
    """Simulation config loaded from ``RUNNER_``-prefixed environment variables.

    Each field maps to ``RUNNER_<FIELD>``: ``RUNNER_ENTRYPOINT``,
    ``RUNNER_INPUTS_PATH`` and ``RUNNER_OUTPUTS_PATH``.
    """

    model_config = SettingsConfigDict(env_prefix="RUNNER_", extra="ignore")

    entrypoint: Path
    inputs_path: Path = Path("data/inputs")
    outputs_path: Path = Path("data/outputs")

    @field_validator("entrypoint", mode="before")
    @classmethod
    def _reject_blank_entrypoint(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            raise ValueError("must point at the R entrypoint script")
        return value


def load_entrypoint() -> SimulationConfig:
    """Build the simulation config from ``RUNNER_``-prefixed env vars.

    The model is supplied at runtime rather than living in this repo, so the
    entrypoint R script is read from the environment. Raises ``RuntimeError``
    with a clear message when ``RUNNER_ENTRYPOINT`` is missing or blank.
    """
    try:
        return SimulationConfig()
    except ValidationError as exc:
        raise RuntimeError(
            f"{RUNNER_ENTRYPOINT_ENV} is not set. Point it at the R entrypoint "
            "script to execute, e.g. RUNNER_ENTRYPOINT=example_model/simulate.R"
        ) from exc
