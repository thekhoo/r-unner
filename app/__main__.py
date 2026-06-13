import logging

from app.config import load_entrypoint
from app.runner import run_simulation
from app.utils.logger import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging(level=logging.INFO)
    config = load_entrypoint()
    logger.info("Running entrypoint simulation: %s", config.script)
    run_simulation(config)
    logger.info("Simulation complete")


if __name__ == "__main__":
    main()
