from dataclasses import dataclass
from pathlib import Path

@dataclass
class Paths:
    root: Path = Path(__file__).resolve().parents[2]
    data: Path = root / "data"
    outputs: Path = root / "outputs"
    recon: Path = outputs / "reconstructions"
    analysis: Path = outputs / "analysis"
    figures: Path = outputs / "figures"
    bonus: Path = outputs / "bonus"

paths = Paths()
for d in (paths.outputs, paths.recon, paths.analysis, paths.figures, paths.bonus):
    d.mkdir(parents=True, exist_ok=True)
