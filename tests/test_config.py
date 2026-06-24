from pathlib import Path

import pytest

from app.config import RunnerConfig, load_config


def test_runner_config_reads_runner_prefixed_env(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    monkeypatch.setenv("RUNNER_INPUTS_PATH", "custom/inputs")
    monkeypatch.setenv("RUNNER_OUTPUTS_PATH", "custom/outputs")
    config = RunnerConfig()
    assert config.entrypoint == Path("example_model/simulate.R")
    assert config.inputs_path == Path("custom/inputs")
    assert config.outputs_path == Path("custom/outputs")


def test_runner_config_has_default_paths(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    monkeypatch.delenv("RUNNER_INPUTS_PATH", raising=False)
    monkeypatch.delenv("RUNNER_OUTPUTS_PATH", raising=False)
    config = RunnerConfig()
    assert config.inputs_path == Path("data/inputs")
    assert config.outputs_path == Path("data/outputs")


def test_load_config_builds_config_from_env(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    config = load_config()
    assert isinstance(config, RunnerConfig)
    assert config.entrypoint == Path("example_model/simulate.R")


def test_load_config_raises_when_unset(monkeypatch):
    monkeypatch.delenv("RUNNER_ENTRYPOINT", raising=False)
    with pytest.raises(RuntimeError, match="RUNNER_ENTRYPOINT"):
        load_config()


def test_load_config_raises_when_blank(monkeypatch):
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "  ")
    with pytest.raises(RuntimeError, match="RUNNER_ENTRYPOINT"):
        load_config()
