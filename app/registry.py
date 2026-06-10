from pathlib import Path

from app.config import SimulationConfig

SIMULATIONS: list[SimulationConfig] = [
    SimulationConfig(script=Path("model/simulate.R")),
]
