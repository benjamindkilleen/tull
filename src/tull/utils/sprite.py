from pathlib import Path
import logging
import numpy as np
from PIL import Image

from .colors import get_color

log = logging.getLogger(__name__)


def make_sprite(
    input_path: Path,
    output_path: Path,
    background: str,
    foreground: str | None,
    fuzz: bool = True,
    crop: bool = True,
):
    log.info(f"Processing {input_path} into {output_path}.")

    image = np.array(Image.open(input_path).convert("RGBA"))
    # Convert to float in range [0, 1]
    image = image.astype(np.float32) / 255

    alpha = image[:, :, 3]
    intensity: np.ndarray = image[:, :, :3].mean(axis=2)

    bg_color = get_color(background)
    bg_intensity: float = bg_color.mean()

    # Set the alpha channel to the difference between the pixel intensity and the background intensity
    if not np.all(alpha == 1):
        log.info("Image already has transparency. Skipping.")
    elif fuzz:
        log.debug("Setting alpha channel with fuzz.")
        alpha: np.ndarray = np.abs(image[:, :, :3] - bg_color).mean(axis=2)
        # plt.imshow(alpha)
        # plt.show()
        # log.info(f"alpha: {alpha.shape}, {alpha.min()}, {alpha.max()}")
        # Scale alpha to the range [0, 1]
        alpha_min = 0.05
        alpha_max = 0.8
        alpha = np.clip(alpha, alpha_min, alpha_max)
        alpha = (alpha - alpha_min) / (alpha_max - alpha_min)
    else:
        log.debug("Setting alpha channel without fuzz.")
        alpha = (np.abs(intensity - bg_intensity) < 0.05).astype(np.float32)

    # Set the foreground color
    log.debug("Setting foreground color.")
    if foreground is not None:
        log.debug(f"Foreground color: {foreground}")
        fg_color = get_color(foreground)
        fg_image = np.full_like(image[:, :, :3], fg_color)
        output_image = np.dstack([fg_image, alpha])

    else:
        log.debug(
            "No foreground color specified. Keeping original image with new alpha."
        )
        output_image = image
        output_image[:, :, 3] = alpha

    # Crop the image to the bounding box of the non-background pixels
    if crop:
        log.debug("Cropping image.")
        mask = alpha > 0
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        log.info(f"Cropping to rows {rmin}:{rmax} and cols {cmin}:{cmax}.")
        output_image = output_image[rmin:rmax, cmin:cmax]

    # Save the image
    log.debug("Saving image.")
    Image.fromarray((output_image * 255).astype(np.uint8)).save(output_path)
