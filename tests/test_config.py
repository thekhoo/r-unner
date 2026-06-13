from pathlib import Path

import pytest

from app.config import RUNNER_ENTRYPOINT_ENV, SimulationConfig, load_entrypoint


def test_load_entrypoint_builds_config_from_env():
    env = {RUNNER_ENTRYPOINT_ENV: "example_model/simulate.R"}
    config = load_entrypoint(env)
    assert isinstance(config, SimulationConfig)
    assert config.script == Path("example_model/simulate.R")
    assert config.inputs_path == Path("data/inputs")
    assert config.outputs_path == Path("data/outputs")


def test_load_entrypoint_raises_when_unset():
    with pytest.raises(RuntimeError, match=RUNNER_ENTRYPOINT_ENV):
        load_entrypoint({})


def test_load_entrypoint_raises_when_empty():
    with pytest.raises(RuntimeError, match=RUNNER_ENTRYPOINT_ENV):
        load_entrypoint({RUNNER_ENTRYPOINT_ENV: "  "})
