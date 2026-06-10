import logging
import subprocess

from app.config import SimulationConfig

logger = logging.getLogger(__name__)


def run_simulation(config: SimulationConfig) -> subprocess.CompletedProcess:
    cmd = [
        "Rscript",
        str(config.script),
        "--inputs", str(config.inputs_path),
        "--outputs", str(config.outputs_path),
        *[f"--{k}={v}" for k, v in config.params.items()],
    ]
    logger.info("Running simulation: %s", config.script)
    logger.debug("Command: %s", cmd)
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    logger.info("Simulation complete: %s", config.script)
    return result
