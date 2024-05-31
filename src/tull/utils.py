import matplotlib.colors as mcolors
import numpy as np
import re


def get_color(user_input: str | tuple[int, int, int] | int) -> np.ndarray:
    """Convert a color input to an RGB array (3,) in range [0,1]."""

    # Check if the input is a color name
    if isinstance(user_input, str):
        if user_input.startswith("#"):  # Hex code
            color = np.array(mcolors.hex2color(user_input))
        elif re.match(r"\d{1,3},\d{1,3},\d{1,3}", user_input):
            color = get_color(tuple(map(int, user_input.split(","))))
        elif re.match(r"\d{1,3}", user_input):
            color = get_color(int(user_input))
        elif user_input.lower() in mcolors.CSS4_COLORS:  # CSS4 color name
            try:
                c = mcolors.to_rgb(user_input)
            except ValueError:
                raise ValueError(f"Invalid color name: {user_input}")
            color = np.array(c)
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

    elif isinstance(user_input, np.ndarray):
        color = user_input

    else:
        raise ValueError(f"Invalid color input: {user_input}")

    return color
