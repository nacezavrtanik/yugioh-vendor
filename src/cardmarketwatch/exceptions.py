
class CardmarketwatchError(Exception):
    """Base exception for the cardmarketwatch library"""


class CSVProcessingError(CardmarketwatchError):
    pass


class ArticlePageNotFoundError(CardmarketwatchError):
    pass
