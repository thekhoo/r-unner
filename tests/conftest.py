import pytest


@pytest.fixture(autouse=True)
def runner_entrypoint(monkeypatch):
    """Point ``RUNNER_ENTRYPOINT`` at the bundled example model for the suite.

    The real model is supplied at runtime and lives outside this repo, so any
    code path that reads the environment directly resolves to a real script.
    Tests that need a different value override it with their own monkeypatch.
    """
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
