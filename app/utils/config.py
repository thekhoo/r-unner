import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class RunnerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RUNNER_", extra="ignore")

    inputs_s3_uri: str
    outputs_s3_uri: str
    entrypoint: str

    def log_contents(self) -> None:
        """Log the environment variables used to configure the runner."""
        for key, value in self.model_dump().items():
            logger.info("RUNNER_%s: %s", key.upper(), value)
