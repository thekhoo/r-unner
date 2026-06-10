from pathlib import Path
from unittest.mock import MagicMock, patch

from runner.config import SimulationConfig
from runner.runner import run_simulation


def test_simulation_config_has_default_paths():
    config = SimulationConfig(script=Path("r/simulate.R"))
    assert config.inputs_path == Path("data/inputs")
    assert config.outputs_path == Path("data/outputs")
    assert config.params == {}


def test_simulation_config_accepts_custom_paths():
    config = SimulationConfig(
        script=Path("r/simulate.R"),
        inputs_path=Path("custom/inputs"),
        outputs_path=Path("custom/outputs"),
        params={"seed": "42"},
    )
    assert config.inputs_path == Path("custom/inputs")
    assert config.outputs_path == Path("custom/outputs")
    assert config.params == {"seed": "42"}


def test_run_simulation_invokes_rscript_with_correct_args():
    config = SimulationConfig(
        script=Path("r/simulate.R"),
        inputs_path=Path("data/inputs"),
        outputs_path=Path("data/outputs"),
        params={"seed": "42"},
    )
    with patch("runner.runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        run_simulation(config)
    mock_run.assert_called_once_with(
        [
            "Rscript",
            "r/simulate.R",
            "--inputs", "data/inputs",
            "--outputs", "data/outputs",
            "--seed=42",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def test_run_simulation_with_no_params():
    config = SimulationConfig(script=Path("r/simulate.R"))
    with patch("runner.runner.subprocess.run") as mock_run:
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
