from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SimulationConfig:
    script: Path
    inputs_path: Path = field(default_factory=lambda: Path("data/inputs"))
    outputs_path: Path = field(default_factory=lambda: Path("data/outputs"))
    params: dict[str, str] = field(default_factory=dict)
