from PIL import Image, ImageDraw, ImageFont
from .utils import generate_random_string, resize_image, draw_quote
import os


class MemeEngine:
    """Class for generating memes."""

    def __init__(self, dir: str) -> None:
        """Init method for MemeEngine.

        :param dir: the directory to save memes in.
        """
        self.dir = dir

        try:
            os.mkdir(self.dir)
        except FileExistsError:
            print(f"{self.dir} already exists, no need to create new.")

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
        img_resized = resize_image(img)

        # add quote
        draw_quote(img_resized, text, author)

        # save
        randstring = generate_random_string()
        filename = self.dir + '/' + randstring

        try:
            img_resized.save(filename + '.jpg')
        except OSError:
            print(f"File {filename + '.jpg'} could not be saved.")

        return filename+'.jpg'
