import logging
import sys

from memray import Tracker

from app.runner import run_simulation
from app.utils.environment import EnvironmentManager

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        with (
            EnvironmentManager(log_level=logging.INFO) as env_manager,
            Tracker(
                file_name="memory_profile.bin",
                native_traces=True,
                trace_python_allocators=True,
            ) as tracker,
        ):
            config = env_manager.config
            run_simulation(config, tracker)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
