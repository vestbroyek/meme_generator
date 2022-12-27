from flask import Flask, render_template, request
from QuoteEngine import Ingestor
from MemeEngine import MemeEngine
import os 
from random import choice
import requests
import subprocess
import shutil
from meme import generate_meme


app = Flask(__name__)

meme = MemeEngine('./static')

def setup():
    """Load all resources"""

    cwd = os.getcwd()
    quote_files = [cwd+'/_data/DogQuotes/DogQuotesTXT.txt',
                   cwd+'/_data/DogQuotes/DogQuotesDOCX.docx',
                   cwd+'/_data/DogQuotes/DogQuotesPDF.pdf',
                   cwd+'/_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = cwd+"/_data/photos/dog/"

    imgs = [images_path+file for file in os.listdir(images_path) if file.split('.')[1] == 'jpg']

    return quotes, imgs


@app.route('/')
def meme_rand():
    """Generate a random meme"""

    quotes, imgs = setup()

    img = choice(imgs)
    quote = choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information"""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme"""

    # fetch user params
    url, body, author = [request.form.get(param) for param in ['image_url', 'body', 'author']]

    # save img to temp file
    response = requests.get(url, stream=True)
    with open('tempfile.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    cwd = os.getcwd()
    path = generate_meme(cwd+"/"+"tempfile.jpg", author, body)
    # abs path
    path = os.path.basename(path)
    subprocess.run(['rm', 'tempfile.jpg'])

    return render_template('meme.html', path='./static/'+path)


if __name__ == "__main__":
    app.run()
