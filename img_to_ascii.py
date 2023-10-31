import click
import math
import numpy as np
from PIL import Image, ImageOps


def get_grayscale_char(gray_scale: int, map: str) -> str:
    return map[math.ceil((len(map) - 1) * gray_scale / 255)]


# fmt: off
@click.command()
@click.option("-f", "--file",   type=click.Path(dir_okay=False, writable=True), help="the text file to write to")
@click.option("-w", "--width",  type=int,                                       help="the width of the output in characters")
@click.option("-h", "--height", type=int,                                       help="the height of the output in characters")
@click.option("-m", "--map",    type=str, default="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. ", help="the height of the output in characters")
@click.option("-r", "--ratio",  type=float, default=9.633331298828125 / 19,     help="ratio of the monospace font (width / height)")
@click.option("-i", "--invert", is_flag=True, show_default=True, default=False, help="invert the image before processing")
@click.argument("image_file",   type=click.Path(dir_okay=False))
# fmt: on
def img_to_ascii(
    file: str | None,
    width: int | None,
    height: int | None,
    map: str,
    ratio: float,
    invert: bool,
    image_file: str,
) -> None:
    # perform checks
    if width is None and height is None:
        raise ValueError("either 'width' or 'height' must be defined")

    # open and rescale image
    image = Image.open(image_file).convert("L")

    if width is None:
        width = int(image.width / image.height * height / ratio)
    elif height is None:
        height = int(image.height / image.width * width * ratio)

    resized = image.resize((width, height))

    # optionally invert image
    if invert:
        resized = ImageOps.invert(resized)

    # get pixels and convert them to ascii strings
    pixels = np.array(resized)
    ascii_image = ""
    for row in pixels:
        for pixel in row:
            ascii_image += get_grayscale_char(pixel, map)
        ascii_image += "\n"

    if file is None:
        print(ascii_image)
    else:
        with open(file, "w+") as f:
            f.write(ascii_image)


if __name__ == "__main__":
    img_to_ascii()
