from unittest.mock import patch

import app.utils.config as conf


@patch.dict(
    "os.environ",
    {
        "RUNNER_INPUTS_S3_URI": "s3://test-inputs-bucket/test-inputs-prefix",
        "RUNNER_OUTPUTS_S3_URI": "s3://test-outputs-bucket/test-outputs-prefix",
        "RUNNER_ENTRYPOINT": "path/to/entrypoint.R",
    },
)
class TestRunnerConfig:
    def test_runner_config_returns_s3_environment_variables_in_config(self):
        config = conf.RunnerConfig()
        assert config.inputs_s3_uri == "s3://test-inputs-bucket/test-inputs-prefix"
        assert config.outputs_s3_uri == "s3://test-outputs-bucket/test-outputs-prefix"

    def test_runner_config_returns_entrypoint_environment_variable_in_config(self):
        config = conf.RunnerConfig()
        assert config.entrypoint == "path/to/entrypoint.R"
