import logging
import sys

from app.config import load_config
from app.runner import run_simulation
from app.utils.logger import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging(level=logging.INFO)
    try:
        config = load_config()
    except RuntimeError as exc:
        logger.error("%s", exc)
        sys.exit(1)
    logger.info("Running entrypoint simulation: %s", config.entrypoint)
    run_simulation(config)
    logger.info("Simulation complete")


if __name__ == "__main__":
    main()
