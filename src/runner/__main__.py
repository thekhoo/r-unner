import logging

from runner.registry import SIMULATIONS
from runner.runner import run_simulation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting runner with %d simulation(s)", len(SIMULATIONS))
    for config in SIMULATIONS:
        run_simulation(config)
    logger.info("All simulations complete")


if __name__ == "__main__":
    main()
