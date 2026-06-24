from unittest.mock import MagicMock, patch

import pytest

import app.__main__ as main_module


def test_main_exits_with_code_1_when_entrypoint_missing():
    with (
        patch.object(main_module, "configure_logging"),
        patch.object(
            main_module, "load_config", side_effect=RuntimeError("not set")
        ),
    ):
        with pytest.raises(SystemExit) as exc_info:
            main_module.main()
    assert exc_info.value.code == 1


def test_main_runs_simulation_when_entrypoint_present():
    config = MagicMock()
    with (
        patch.object(main_module, "configure_logging"),
        patch.object(main_module, "load_config", return_value=config),
        patch.object(main_module, "run_simulation") as mock_run,
    ):
        main_module.main()
    mock_run.assert_called_once_with(config)
