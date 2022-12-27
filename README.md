# Meme generator project

## Overview
This project allows you to serve a meme generator web app. A "meme" consists of a quote overlaid on a picture. Users can choose whether to generate a random meme or submit their own. 

The app is written purely in Python. The web app uses Flask. 

## How to use
To use this project, 

1. clone the repo
2. install dependencies with `pip3 install -r requirements.txt`
3. run the app with `python3 app.py`
4. open the app at the URL shown, likely something like `http://127.0.0.1:5000`

## How it works
Running `python3 app.py` will run a local Flask server. (`app.py` contains the app's definition.) To set up, a few default photos and quotes will be loaded from the `_data` directory. These can be used to generate random memes.

The app generates memes, either random or user-defined. 

When a *random* meme is generated, the app will pick a random quote and picture and show it to the user. 

When the user generates a meme, the app will download the picture in question and overlay the quote.

For more detail, read the below section.

## Project structure and code definitions
### Root folder
The root of the project contains the following files:

`.env`

The `.env` file lets you set environment variables. In this case, the only environment variable is the path to the font you want to use. I've included Comic Sans here, but feel free to change it. 

`app.py`

Defines the Flask app. It defines 

* how setup is to proceeed (i.e. read default images and quotes into memory to allow the creation of random memes)
* the homepage (`/`), which generates random memes
* the creation functionality (`/create`), which allows users to create and view their own memes.

`meme.py`

Generate a meme given a path, quote body, and author, or, lacking those, a random meme. 

The code will parse these three arguments and call the `generate_meme` function, which will in turn instantiate a `MemeEngine` object and call its `make_meme()` method with an image, quote, and author. This functionality is used for meme creation in the app. 

### Data folder
The `_data` folder is used for storing base pictures and files in a variety of formats (currently `.csv`, `.docx`, `.pdf`, `.txt`, which can be parsed for quotes.)

### MemeEngine module
This module contains the necessary functionality for generating memes.

`fonts`

The `fonts` folder contains .ttf font files which you can add to and refer to in `.env`. 

`__init__.py`

This file tells Python how to initialise the module. In this case, it simplifies the import of the `MemeEngine` class and also makes the `dotenv` library available, for working with the `.env` file.

`meme_engine.py`

Contains the `MemeEngine` class. You initialise a `MemeEngine` object like `meme = MemeEngine('/folder')`, where `/folder` is a path to store memes in. By default, `./static` is used.

The `make_meme()` method takes a path to an image, text, an author, and an image width of a meme and returns a path to the resulting meme. This function is used on the landing page of the Flask app to serve users a random meme. 

`utils.py`

This file stores helper functions, in this case only a function for generating random strings, used for creating temporary filenames.

### QuoteEngine module
This module contains the code for ingesting and structuring quotes.

`__init__.py`

This file tells Python how to initialise the module. In this case, it simplifies the import of the `QuoteModel` class and also makes the `dotenv` library available, for working with the `.env` file.

`ingestors.py`

Defines a wrapper class for different file ingestion methods. At the moment, `.csv`, `.docx`, `.pdf`, and `.txt` are supported.

Each ingestor class inherits from an abstract base class, `IngestorInterface`. The base class defines a class method, `can_ingest()`, which checks whether the file extension matches the ingestor. Additionally, it defines an abstract class method `parse()`, which each concrete child class needs to realise - i.e. implement its own logic for parsing files of its own type.

From this interface, several concrete child classes are realised, for ingesting CSVs, Docx documents, PDFs, and TXT files. Each has its own parsing logic.

Finally, a wrapper class, `Ingestor`, is defined which encapsulates all the individual ingestors. The idea is to create one accessible interface for the functionality of each ingestor class. In this way, it becomes possible to simply call `Ingestor.parse('somefile.pdf')`, and the Ingestor will check the extension, use the correct Ingestor (in this case `PDFIngestor`), and parse the data in it. 

`quote_model.py`

Defines a simple class, `QuoteModel`, for containing a quote, specifically, a quote `body` and its `author`. You can do `quote = QuoteModel('some quote', 'some author')` and access the attributes like `quote.body`. 


### Templates
Contains .html templates (with Jinja) to render in the webapp. 

### tmp and static
These are folders for temporarily saving memes.
