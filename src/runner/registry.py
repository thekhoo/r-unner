from pathlib import Path

from runner.config import SimulationConfig

SIMULATIONS: list[SimulationConfig] = [
    SimulationConfig(script=Path("r/simulate.R")),
]
