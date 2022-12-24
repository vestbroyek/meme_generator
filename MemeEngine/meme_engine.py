from PIL import Image, ImageDraw, ImageFont
import os
from random import randint, choice
import string

class MemeEngine:
    def __init__(self):
        pass

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        # initialise image
        img = Image.open(img_path)
        # resize
        ratio = 500/img.width
        (width, height) = (500, ratio*img.height)
        img_resized = img.resize((width, height))

        ### add quote 
        # create canvas
        draw = ImageDraw.Draw(img)
        # get font
        fontpath = '/Users/maurits/training/vscode/udacity-intermediate-python/git/meme_generator/MemeEngine/fonts/LDFComicSans.ttf'
        font = ImageFont.truetype(fontpath, size=randint(25, 40))
        # add text at random coordinates, random font size (between 25 and 40), and random colour
        draw.text((
            randint(0, 400), randint(0, 400)), 
            f"{text} - {author}", 
            font=font,
            fill=(randint(0, 255), randint(0,255), randint(0,255), randint(0,255)))
        # save 
        randstring = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(5))
        filename = img_path.split('.')[0] + randstring
        img.save(filename+'.jpg')

        return filename+'.jpg' 


    