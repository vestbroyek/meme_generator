import os
from pathlib import Path
import random
from MemeEngine import MemeEngine
from QuoteEngine import QuoteModel, Ingestor
import argparse


def generate_meme(path: str = None, body: str = None, author: str = None):
    """Generate a meme given a path and a quote.

    :param path:    A path to a file
    :param body:    A quote
    :param author:  The quote's author
    :returns str:   The path to the generated meme.
    """
    cwd = os.getcwd()
    quote = None

    if path is None:
        images = cwd + "/_data/photos/dog"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [cwd+'/_data/DogQuotes/DogQuotesTXT.txt',
                       cwd+'/_data/DogQuotes/DogQuotesDOCX.docx',
                       cwd+'/_data/DogQuotes/DogQuotesPDF.pdf',
                       cwd+'/_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author required if body is used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./static/')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a meme.')

    # add args
    parser.add_argument('--body', type=str, help='The quote body')
    parser.add_argument('--author', type=str, help='The quote\'s author')
    parser.add_argument('--path', type=str, help='Path to an image')
    args = parser.parse_args()

    # execute
    generate_meme(args.path, args.body, args.author)
