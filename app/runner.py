import logging
import subprocess

from app.config import RunnerConfig

logger = logging.getLogger(__name__)


def run_simulation(config: RunnerConfig) -> subprocess.CompletedProcess:
    cmd = [
        "Rscript",
        str(config.entrypoint),
        "--inputs", str(config.inputs_path),
        "--outputs", str(config.outputs_path),
    ]
    logger.info("Running simulation: %s", config.entrypoint)
    logger.debug("Command: %s", cmd)
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    logger.info("Simulation complete: %s", config.entrypoint)
    return result
