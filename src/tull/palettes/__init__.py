from .palette import Palette
from pathlib import Path

TUM = Palette.from_gpl(Path(__file__).parent / "TUM.gpl")
JHU = Palette.from_txt(Path(__file__).parent / "JHU.txt")

__all__ = ["TUM", "JHU", "Palette"]
