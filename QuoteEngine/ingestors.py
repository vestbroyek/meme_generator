from abc import ABC, abstractmethod
from typing import List
from .quote_model import QuoteModel
from csv import reader
from docx import Document
import subprocess

class IngestorInterface(ABC):
    """
    Abstract ingestor interface to be realised by concrete classes for different filetypes.
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        ext = path.split('.')[1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass

class CSVIngestor(IngestorInterface):
    """
    Class for ingesting .csvs containing quotes. Realises IngestorInterface.
    """
    
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        # check if allowed filetype
        if not cls.can_ingest(path):
            ext = path.split('.')[1]
            raise Exception(f'cannot ingest filetype {ext}')

        # if so, parse line by line and return list of quotes
        quotes = []
        with open(path, 'r') as f:
            lines = reader(f, delimiter=',', quotechar='"')
            # Skip header
            next(lines)
            for line in lines:
                quotes.append(QuoteModel(line[0], line[1]))

        
        return quotes

class DOCXIngestor(IngestorInterface):
    """
    Class for ingesting .docx files. Realises IngestorInterface
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        # check if allowed filetype
        if not cls.can_ingest(path):
            ext = path.split('.')[1]
            raise Exception(f'cannot ingest filetype {ext}') 

        # parse
        quotes = []
        document = Document(path)
        for para in document.paragraphs:
            if len(para.text) > 0:
                # split on - and remove spaces and quotes
                body = para.text.split('-')[0].strip().replace('"', '')
                author = para.text.split('-')[1].strip().replace('"', '')
                quotes.append(QuoteModel(body, author))

class PDFIngestor(IngestorInterface):
    """
    Class for ingesting .pdf files. Realises IngestorInterface.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        # check if allowed filetype
        if not cls.can_ingest(path):
            ext = path.split('.')[1]
            raise Exception(f'cannot ingest filetype {ext}') 

        
        # parse into txt
        quotes = []
        text = subprocess.run(['pdftotext', '-layout', f'{path}', 'outfile'])
        with open('outfile', 'r') as f:
            for line in f:
                if '-' in line:
                    body = line.split('-')[0].replace('\n', '').strip()
                    author = line.split('-')[1].replace('\n', '').strip() 
                    quotes.append(QuoteModel(body, author))

        # rm outfile
        subprocess.run(['rm', 'outfile'])

        return quotes

class TXTIngestor(IngestorInterface):
    """
    Class for ingesting .txt files. Realises IngestorInterface.
    """
    
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        # check if allowed filetype
        if not cls.can_ingest(path):
            ext = path.split('.')[1]
            raise Exception(f'cannot ingest filetype {ext}') 

        quotes = []
        with open(path, 'r') as f:
            for line in f:
                # no headers here, just split on - and read
                line = line.replace('\n', '')
                quotes.append(QuoteModel(line.split('-')[0].strip(), line.split('-')[1].strip()))

        return quotes

class Ingestor(IngestorInterface):
    """
    Class encapsulating all ingestor concrete classes.
    """

    ingestors = [CSVIngestor, TXTIngestor, DOCXIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path):
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)