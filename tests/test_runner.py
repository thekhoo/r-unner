from unittest.mock import MagicMock, patch

from app.runner import run_simulation
from app.utils.environment import RunnerConfig


def test_run_simulation_invokes_rscript_with_correct_args():
    config = RunnerConfig()
    with patch("app.runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_simulation(config)
    mock_run.assert_called_once_with(
        [
            "Rscript",
            "example_model/simulate.R",
            "--inputs",
            "s3://test-inputs-bucket/test-inputs-prefix",
            "--outputs",
            "s3://test-outputs-bucket/test-outputs-prefix",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
