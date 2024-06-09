import matplotlib.colors as mcolors
import numpy as np
import re
from enum import Enum, auto

from .cases import classcase


def get_color(user_input: str | tuple[int, int, int] | int) -> np.ndarray:
    """Convert a color input to an RGB array (3,) in range [0,1]."""

    # Check if the input is a color name

    if isinstance(user_input, np.ndarray):
        color = user_input
    elif isinstance(user_input, str):
        if user_input.startswith("#"):  # Hex code
            color = np.array(mcolors.hex2color(user_input))
        elif re.match(r"\d{1,3},\d{1,3},\d{1,3}", user_input):
            color = get_color(tuple(map(int, user_input.split(","))))
        elif re.match(r"\d{1,3}", user_input):
            color = get_color(int(user_input))
        elif user_input.lower() in mcolors.CSS4_COLORS:  # CSS4 color name
            try:
                c = mcolors.to_rgb(user_input.lower())
            except ValueError:
                raise ValueError(f"Invalid color name: {user_input}")
            color = np.array(c)

        elif (jhu_color := JHU.get(user_input)) is not None:
            color = jhu_color

        else:
            raise ValueError(f"Invalid color name: {user_input}")
    # Check if the input is an RGB tuple
    elif isinstance(user_input, tuple) and len(user_input) == 3:
        if all(isinstance(x, int) for x in user_input):
            color = np.array([x / 255 for x in user_input])
        else:
            color = np.array(user_input)  # Assuming it's already in RGB format

    # Check if the input is a grayscale value
    elif isinstance(user_input, int):
        color = np.array([user_input / 255] * 3)

    elif isinstance(float(user_input), float):
        color = np.array([user_input] * 3)
    else:
        raise ValueError(f"Invalid color input: {user_input}")

    return color


class JHU:
    HeritageBlue = np.array([0, 45, 114]) / 255
    SpiritBlue = np.array([114, 172, 229]) / 255
    PRIMARIES = np.array([HeritageBlue, SpiritBlue])

    SecondaryOrange = np.array([255, 158, 27]) / 255
    SecondaryGreen = np.array([0, 155, 119]) / 255
    SecondaryBlue = np.array([0, 114, 206]) / 255
    SecondaryYellow = np.array([241, 196, 0]) / 255
    SECONDARIES = np.array(
        [SecondaryOrange, SecondaryGreen, SecondaryBlue, SecondaryYellow]
    )

    ACCENTS = (
        np.array(
            [
                [203, 160, 82],
                [255, 105, 0],
                [158, 83, 48],
                [79, 44, 29],
                [232, 146, 124],
                [207, 69, 32],
                [166, 25, 46],
                [118, 35, 47],
                [81, 40, 79],
                [161, 90, 149],
                [161, 146, 178],
                [65, 143, 222],
                [134, 200, 188],
                [40, 97, 64],
                [113, 153, 73],
            ]
        )
    ) / 255

    Sable = np.array([49, 38, 29]) / 255
    White = np.array([255, 255, 255]) / 255
    DoubleBlack = np.array([0, 0, 0]) / 255

    @classmethod
    def grayscale(cls, value: float) -> np.ndarray:
        """Interpolate between Sable and White."""
        return cls.Sable * (1 - value) + cls.White * value

    Colors: dict[str, np.ndarray] = {
        "HeritageBlue": HeritageBlue,
        "SpiritBlue": SpiritBlue,
        "SecondaryOrange": SecondaryOrange,
        "SecondaryGreen": SecondaryGreen,
        "SecondaryBlue": SecondaryBlue,
        "SecondaryYellow": SecondaryYellow,
        "Accent0": ACCENTS[0],
        "Accent1": ACCENTS[1],
        "Accent2": ACCENTS[2],
        "Accent3": ACCENTS[3],
        "Accent4": ACCENTS[4],
        "Accent5": ACCENTS[5],
        "Accent6": ACCENTS[6],
        "Accent7": ACCENTS[7],
        "Accent8": ACCENTS[8],
        "Accent9": ACCENTS[9],
        "Accent10": ACCENTS[10],
        "Accent11": ACCENTS[11],
        "Accent12": ACCENTS[12],
        "Accent13": ACCENTS[13],
        "Accent14": ACCENTS[14],
        "Sable": Sable,
        "White": White,
        "DoubleBlack": DoubleBlack,
    }

    @classmethod
    def get(cls, name: str) -> np.ndarray | None:
        if (upname := classcase(name)) in cls.Colors:
            return cls.Colors[upname].copy()

        elif name.startswith("primary"):
            index = int(name.split("-")[1])
            return cls.PRIMARIES[index].copy()

        elif name.startswith("secondary"):
            index = int(name.split("-")[1])
            return cls.SECONDARIES[index].copy()

        elif name.startswith("accent"):
            index = int(name.split("-")[1])
            return cls.ACCENTS[index].copy()

        elif name.startswith("gray"):
            value = float(name.split("-")[1])
            return cls.grayscale(value)

        else:
            return None

    @classmethod
    def primary(cls, index: int) -> np.ndarray:
        return cls.PRIMARIES[index].copy()

    @classmethod
    def blue(cls) -> np.ndarray:
        return cls.HeritageBlue.copy()

    def spirit_blue(cls) -> np.ndarray:
        return cls.SpiritBlue.copy()

    @classmethod
    def secondary(cls, index: int) -> np.ndarray:
        return cls.SECONDARIES[index].copy()

    @classmethod
    def accent(cls, index: int) -> np.ndarray:
        return cls.ACCENTS[index].copy()

    @classmethod
    def random_accent(cls) -> np.ndarray:
        return cls.ACCENTS[np.random.randint(len(cls.ACCENTS))].copy()

    @classmethod
    def double_black(cls) -> np.ndarray:
        return cls.DoubleBlack.copy()

    TWO_COLORS = np.array(
        [
            [[35, 53, 112], [0, 153, 117]],
            [[35, 53, 112], [36, 11, 183]],
            [[110, 169, 219], [121, 34, 46]],
            [[110, 169, 219], [35, 53, 112]],
        ]
    )

    THREE_COLORS = np.array(
        [
            [[35, 53, 112], [205, 161, 84], [110, 169, 219]],
        ]
    )

    @classmethod
    def palette(cls, num_colors: int, index: int = 0) -> np.ndarray:
        """Get a JHU color palette.

        Returns:
            np.ndarray: An array of RGB colors with shape (num_colors, 3).
        """
        raise NotImplementedError

    @classmethod
    def full_palette(cls) -> dict[str, np.ndarray]:
        """Get the full JHU color palette. Does not include white."""
        return {
            "HeritageBlue": cls.HeritageBlue,
            "SpiritBlue": cls.SpiritBlue,
            "SecondaryOrange": cls.SecondaryOrange,
            "SecondaryGreen": cls.SecondaryGreen,
            "SecondaryBlue": cls.SecondaryBlue,
            "SecondaryYellow": cls.SecondaryYellow,
            "Accent0": cls.ACCENTS[0],
            "Accent1": cls.ACCENTS[1],
            "Accent2": cls.ACCENTS[2],
            "Accent3": cls.ACCENTS[3],
            "Accent4": cls.ACCENTS[4],
            "Accent5": cls.ACCENTS[5],
            "Accent6": cls.ACCENTS[6],
            "Accent7": cls.ACCENTS[7],
            "Accent8": cls.ACCENTS[8],
            "Accent9": cls.ACCENTS[9],
            "Accent10": cls.ACCENTS[10],
            "Accent11": cls.ACCENTS[11],
            "Accent12": cls.ACCENTS[12],
            "Accent13": cls.ACCENTS[13],
            "Accent14": cls.ACCENTS[14],
            "White": cls.White,
            "Gray10": cls.grayscale(0.1),
            "Gray20": cls.grayscale(0.2),
            "Gray30": cls.grayscale(0.3),
            "Gray40": cls.grayscale(0.4),
            "Gray50": cls.grayscale(0.5),
            "Gray60": cls.grayscale(0.6),
            "Gray70": cls.grayscale(0.7),
            "Gray80": cls.grayscale(0.8),
            "Gray90": cls.grayscale(0.9),
            "Sable": cls.Sable,
            "DoubleBlack": cls.DoubleBlack,
        }
