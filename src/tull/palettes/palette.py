from __future__ import annotations
import numpy as np
from pathlib import Path


class Palette:
    def __init__(self, colors: np.ndarray, names: list[str] | None = None):
        """A color palette.

        Args:
            colors (np.ndarray): An array of rgb colors with shape (N, 3), with values in [0, 1].
            names (list[str] | None): Optional list of color names.

        """
        self.colors = np.array(colors)
        assert self.colors.ndim == 2 and self.colors.shape[1] == 3

        if names is None:
            self.names = [f"color-{i}" for i in range(len(colors))]
        else:
            assert len(names) == self.colors.shape[0]
            self.names = names

        self._name_to_index = {name: i for i, name in enumerate(self.names)}
        self._index_to_name = {i: name for i, name in enumerate(self.names)}

    def __len__(self):
        return len(self.colors)

    def __getitem__(self, index: int | str) -> np.ndarray:
        if isinstance(index, int):
            return self.colors[index]
        elif isinstance(index, str):
            idx = self._name_to_index[index]
            return self.colors[idx]
        else:
            raise TypeError("Index must be an int or str.")

    def __iter__(self):
        for color in self.colors:
            yield color

    def __contains__(self, name: str) -> bool:
        return name in self._name_to_index

    def get(self, name: str) -> np.ndarray | None:
        """Get a color by name.

        Args:
            name (str): The name of the color.

        Returns:
            np.ndarray | None: The color as an array of shape (3,), or None if not found.
        """
        if name in self._name_to_index:
            idx = self._name_to_index[name]
            return self.colors[idx]
        else:
            return None

    def items(self):
        for name, color in zip(self.names, self.colors):
            yield name, color

    @classmethod
    def from_txt(cls, filepath: str | Path) -> Palette:
        """Load a palette from a text file.

        The text file should have one color per line, in the format:
        name R G B
        where R, G, B are in the range [0, 255].

        Args:
            filepath (str | Path): Path to the text file.

        Returns:
            Palette: The loaded palette.
        """
        colors = []
        names = []
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split()
                name = parts[3]
                r, g, b = map(int, parts[0:3])
                colors.append([r / 255, g / 255, b / 255])
                names.append(name)
        return cls(np.array(colors), names)

    @classmethod
    def from_gpl(cls, filepath: str | Path) -> Palette:
        """Load a palette from a GIMP palette file.

        Args:
            filepath (str | Path): Path to the GIMP palette file.

        Returns:
            Palette: The loaded palette.
        """
        colors = []
        names = []
        with open(filepath, "r") as f:
            for line in f:
                if (
                    line.startswith("#")
                    or line.startswith("GIMP")
                    or line.startswith("Name")
                ):
                    continue
                parts = line.strip().split()
                if len(parts) < 4:
                    continue
                r, g, b = map(int, parts[0:3])
                name = " ".join(parts[3:])
                colors.append([r / 255, g / 255, b / 255])
                names.append(name)
        return cls(np.array(colors), names)
