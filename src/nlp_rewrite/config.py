from dataclasses import dataclass
from pathlib import Path

@dataclass
class Paths:
    root: Path = Path(__file__).resolve().parents[2]
    data: Path = root / "data"
    outputs: Path = root / "outputs"
    recon: Path = outputs / "reconstructions"

paths = Paths()
paths.outputs.mkdir(parents=True, exist_ok=True)
paths.recon.mkdir(parents=True, exist_ok=True)
