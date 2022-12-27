from PIL import Image, ImageDraw, ImageFont
from .utils import generate_random_string
import subprocess
from random import randint
import os


class MemeEngine:
    """Class for generating memes."""

    def __init__(self, dir: str) -> None:
        """Init method for MemeEngine.

        :param dir: the directory to save memes in."""

        self.dir = dir

        subprocess.run(["mkdir", f"{dir}"])

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
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            print(f"File {img_path} could not be found.")
            raise

        # resize
        ratio = 500/img.width
        (width, height) = (500, int(ratio*img.height))
        img_resized = img.resize((width, height))

        #  create canvas
        draw = ImageDraw.Draw(img_resized)
        #  get font
        try:
            fontpath = os.environ.get('FONTPATH')
            font = ImageFont.truetype(fontpath, size=randint(25, 40))
        except OSError:
            print("Could not open font file.")
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
        filename = self.dir + '/' + randstring
        try:
            img_resized.save(filename + '.jpg')
        except OSError:
            print(f"File {filename + '.jpg'} could not be saved.")

        return filename+'.jpg'
