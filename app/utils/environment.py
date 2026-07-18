import logging
from contextlib import ContextDecorator

from app.utils.config import RunnerConfig
from app.utils.logger import configure_logging

logger = logging.getLogger(__name__)


class EnvironmentManager(ContextDecorator):
    def __init__(self, log_level: int = logging.INFO):
        self.config = RunnerConfig()
        self.log_level = log_level

    def __enter__(self):

        configure_logging(level=self.log_level)
        logger.info(f"logger configured with level: {self.log_level}")

        # dump all our env vars from the config
        self.config.log_contents()

        return self

    def __exit__(self, *exc):
        logger.info("performing environment cleanup")
        return False
