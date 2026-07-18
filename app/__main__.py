import logging
import sys

from app.runner import run_simulation
from app.utils.environment import EnvironmentManager

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        with EnvironmentManager(log_level=logging.INFO) as env_manager:
            config = env_manager.config
            run_simulation(config)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
