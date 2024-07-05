import click
from pathlib import Path
import numpy as np
from rich.logging import RichHandler
from PIL import Image
import cv2
import logging
import matplotlib.pyplot as plt
from stringcase import spinalcase, camelcase
import shutil
from rich.progress import track

from .utils.colors import JHU
from .utils import make_sprite
from .utils import filenamecase

log = logging.getLogger("tull")

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


@click.group()
@click.option("--verbose", "-v", is_flag=True)
@click.option("--debug", "-d", is_flag=True)
def cli(verbose, debug):
    if verbose:
        log.setLevel(logging.INFO)
    if debug:
        log.setLevel(logging.DEBUG)


@cli.command(help="Process the image into a graphic with a transparent background.")
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default=None)
@click.option(
    "--background",
    "-b",
    type=str,
    default="white",
    help='Background color to turn transparent. Can be a color name, hex code, or RGB list e.g. "255,255,255". If the image already has some transparency, this has no effect. Default is "white".',
)
@click.option(
    "--foreground",
    "-f",
    type=str,
    default=None,
    help="Change all foreground pixels to this csolor.",
)
@click.option(
    "-e",
    "--edge",
    default=None,
    help="Color to use for the edge.",
)
@click.option(
    "--edge-thickness",
    default=3,
    help="Thickness of the edge in pixels.",
)
@click.option(
    "--fuzz/--no-fuzz",
    default=True,
    help="Handle edges by setting alpha values to the difference between the pixel intensity and the background intensity.",
)
@click.option(
    "--crop/--no-crop",
    default=True,
    help="Crop the image to the bounding box of the non-background pixels.",
)
def sprite(input, output, background, foreground, edge, edge_thickness, fuzz, crop):
    input_path = Path(input)
    output_path = (
        (input_path.parent / f"{input_path.stem}_sprite.png")
        if output is None
        else Path(output)
    )

    make_sprite(
        input_path,
        output_path,
        background,
        foreground,
        edge=edge,
        edge_thickness=edge_thickness,
        fuzz=fuzz,
        crop=crop,
    )


@cli.command(help="Run sprite on an image, but over the whole JHU color palette.")
@click.argument("input", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Directory to place the resulting sprites.",
)
@click.option(
    "--background",
    "-b",
    type=str,
    default="white",
    help='Background color to turn transparent. Can be a color name, hex code, or RGB list e.g. "255,255,255". If the image already has some transparency, this has no effect. Default is "white".',
)
@click.option(
    "--fuzz/--no-fuzz",
    default=True,
    help="Handle edges by setting alpha values to the difference between the pixel intensity and the background intensity.",
)
@click.option(
    "--crop/--no-crop",
    default=True,
    help="Crop the image to the bounding box of the non-background pixels.",
)
def jhu(input, output, background, fuzz, crop):
    input_path = Path(input)
    output_dir = (
        Path(output)
        if output is not None
        else input_path.parent / f"{input_path.stem}_sprites"
    )
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    palette = JHU.full_palette()
    for color_name, color in track(
        palette.items(), description="Creating sprites...", total=len(palette)
    ):
        if color_name.startswith("_"):
            continue
        output_path = output_dir / f"{input_path.stem}_{filenamecase(color_name)}.png"
        make_sprite(input_path, output_path, background, color, fuzz=fuzz, crop=crop)
