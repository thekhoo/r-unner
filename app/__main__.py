import logging

from app.registry import SIMULATIONS
from app.runner import run_simulation
from app.utils.logger import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging(level=logging.INFO)
    logger.info("Starting runner with %d simulation(s)", len(SIMULATIONS))
    for config in SIMULATIONS:
        run_simulation(config)
    logger.info("All simulations complete")


if __name__ == "__main__":
    main()
