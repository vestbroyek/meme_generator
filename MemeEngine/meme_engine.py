from PIL import Image, ImageDraw, ImageFont
from .utils import generate_random_string
from random import randint
import os


class MemeEngine:
    """Class for generating memes."""

    def __init__(self):
        """Init method for MemeEngine. Does not take arguments."""
        pass

    def make_meme(
            self,
            img_path: str,
            text: str,
            author: str,
            width: int = 500) -> str:
        """
        Instance method for generating memes.

        :param img_path:        An image path use as a base for the meme
        :param text:            A quote to put on the meme
        :param author:          The author of the quote
        :param width:           The width in pixels, 500 by default
        :returns str:           A path where the generated meme is located

        """
        # initialise image
        img = Image.open(img_path)
        # resize
        ratio = 500/img.width
        (width, height) = (500, ratio*img.height)
        img_resized = img.resize((width, height))

        #  create canvas
        draw = ImageDraw.Draw(img_resized)
        #  get font
        fontpath = os.environ.get('FONTPATH')
        font = ImageFont.truetype(fontpath, size=randint(25, 40))
        #  add text at: random coordinates, random font size and random colour
        draw.text((
            randint(0, 200), randint(0, 200)),
            f"{text} - {author}",
            font=font,
            fill=(
                randint(0, 255),
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)))
        # save
        randstring = generate_random_string()
        filename = img_path.split('.')[0] + randstring
        img_resized.save(filename+'.jpg')

        return filename+'.jpg'
