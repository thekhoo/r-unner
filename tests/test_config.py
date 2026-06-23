from pathlib import Path

import pytest

from app.config import SimulationConfig, load_entrypoint


def test_simulation_config_reads_runner_prefixed_env(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    monkeypatch.setenv("RUNNER_INPUTS_PATH", "custom/inputs")
    monkeypatch.setenv("RUNNER_OUTPUTS_PATH", "custom/outputs")
    config = SimulationConfig()
    assert config.entrypoint == Path("example_model/simulate.R")
    assert config.inputs_path == Path("custom/inputs")
    assert config.outputs_path == Path("custom/outputs")


def test_simulation_config_has_default_paths(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    monkeypatch.delenv("RUNNER_INPUTS_PATH", raising=False)
    monkeypatch.delenv("RUNNER_OUTPUTS_PATH", raising=False)
    config = SimulationConfig()
    assert config.inputs_path == Path("data/inputs")
    assert config.outputs_path == Path("data/outputs")


def test_load_entrypoint_builds_config_from_env(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    config = load_entrypoint()
    assert isinstance(config, SimulationConfig)
    assert config.entrypoint == Path("example_model/simulate.R")


def test_load_entrypoint_raises_when_unset(monkeypatch):
    monkeypatch.delenv("RUNNER_ENTRYPOINT", raising=False)
    with pytest.raises(RuntimeError, match="RUNNER_ENTRYPOINT"):
        load_entrypoint()


def test_load_entrypoint_raises_when_blank(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "  ")
    with pytest.raises(RuntimeError, match="RUNNER_ENTRYPOINT"):
        load_entrypoint()
