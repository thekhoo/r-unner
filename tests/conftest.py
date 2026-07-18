import pytest


@pytest.fixture(autouse=True)
def runner_entrypoint(monkeypatch):
    """Point ``RUNNER_ENTRYPOINT`` at the bundled example model for the suite.

    The real model is supplied at runtime and lives outside this repo, so any
    code path that reads the environment directly resolves to a real script.
    Tests that need a different value override it with their own monkeypatch.
    """
    monkeypatch.setenv("RUNNER_ENTRYPOINT", "example_model/simulate.R")
    monkeypatch.setenv(
        "RUNNER_INPUTS_S3_URI", "s3://test-inputs-bucket/test-inputs-prefix"
    )
    monkeypatch.setenv(
        "RUNNER_OUTPUTS_S3_URI", "s3://test-outputs-bucket/test-outputs-prefix"
    )
