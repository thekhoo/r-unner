import logging
import subprocess

from app.utils.environment import RunnerConfig

logger = logging.getLogger(__name__)


def run_simulation(config: RunnerConfig) -> subprocess.CompletedProcess:
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
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    logger.info("Simulation complete: %s", config.entrypoint)
    return result
