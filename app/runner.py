import logging
import time

import memray

from app.utils.config import RunnerConfig

logger = logging.getLogger(__name__)


def make_blob(size_mb: int):
    return bytearray(size_mb * 1024 * 1024)


def run_simulation(config: RunnerConfig, tracker: memray.Tracker) -> None:
    cmd = [
        "Rscript",
        config.entrypoint,
        "--inputs",
        config.inputs_s3_uri,
        "--outputs",
        config.outputs_s3_uri,
    ]
    logger.info("Running simulation: %s", config.entrypoint)
    logger.debug("Command: %s", cmd)
    # result = subprocess.run(cmd, check=True, capture_output=True, text=True)

    for i in range(10):
        logger.info("Simulating work... %d/10", i + 1)
        blob = make_blob(10)  # Simulate creating a 10 MB blob
        logger.debug("Created a blob of size: %d bytes", len(blob))
        time.sleep(10)  # Simulate time taken for processing

    logger.info("Simulation complete: %s", config.entrypoint)
    return None
