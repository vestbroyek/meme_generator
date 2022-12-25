class QuoteModel:
    """Class for containing quotes."""

    def __init__(self, body: str, author: str) -> None:
        """
        Init method for class for containing quotes.
        
        :param body:    The quote content, like "Some quote" in "Some quote" - Author 
        :param author:  The quote's "author", like Author in "Some quote" - Author
        """
        self.body = body
        self.author = author