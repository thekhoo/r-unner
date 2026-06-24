from pathlib import Path
from unittest.mock import MagicMock, patch

from app.config import RunnerConfig
from app.runner import run_simulation


def test_run_simulation_invokes_rscript_with_correct_args():
    config = RunnerConfig(
        entrypoint=Path("r/simulate.R"),
        inputs_path=Path("data/inputs"),
        outputs_path=Path("data/outputs"),
    )
    with patch("app.runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_simulation(config)
    mock_run.assert_called_once_with(
        [
            "Rscript",
            "r/simulate.R",
            "--inputs", "data/inputs",
            "--outputs", "data/outputs",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def test_run_simulation_uses_custom_paths():
    config = RunnerConfig(
        entrypoint=Path("r/simulate.R"),
        inputs_path=Path("custom/inputs"),
        outputs_path=Path("custom/outputs"),
    )
    with patch("app.runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_simulation(config)
    mock_run.assert_called_once_with(
        [
            "Rscript",
            "r/simulate.R",
            "--inputs", "custom/inputs",
            "--outputs", "custom/outputs",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
