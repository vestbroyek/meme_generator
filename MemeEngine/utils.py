from random import choice
from string import ascii_uppercase, digits
from PIL import Image, ImageDraw, ImageFont
from random import randint
import textwrap


def generate_random_string(length: int = 5) -> str:
    """
    Generate a random string of uppercase numbers and digits.

    :param length:  the length of the desired string
    :returns str:   a random string
    """
    return ''.join(choice(ascii_uppercase + digits) for _ in range(length))


def resize_image(img: Image, width: int = 500) -> Image:
    """
    Resize an image based on a specified width, 500 by default.

    :param img:     A PIL Image
    :param width:   The width, in pixels, to use
    """
    ratio = width/img.width
    (width, height) = (width, int(ratio*img.height))
    img_resized = img.resize((width, height))

    return img_resized


def draw_quote(
        img: Image,
        text: str,
        author: str,
        fontpath: str = "./MemeEngine/fonts/LDFComicSans.ttf"):
    """
    Write a given quote onto an image object.

    :param img:         A PIL Image object to draw on
    :param text:        The quote
    :param author:      The quote's author
    :param fontpath:    A path to a font to use
    """
    # create canvas
    draw = ImageDraw.Draw(img)

    # get font
    font = load_font(fontpath)

    # wrap text
    quote = textwrap.fill(text=f"{text} - {author}", width=20)

    # add text at: random coordinates, random font size and random colour
    draw.text((
        randint(50, 120), randint(50, 120)),
        quote,
        font=font,
        fill=(
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)))


def load_font(fontpath: str) -> ImageFont:
    """
    Load a font file.

    :param fontpath: the path to the font
    """
    try:
        return ImageFont.truetype(fontpath, size=randint(25, 40))
    except OSError:
        print("Could not open font file.")
