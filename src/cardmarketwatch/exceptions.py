
class CardmarketwatchError(Exception):
    """Base exception for the cardmarketwatch library"""


class CSVProcessingError(CardmarketwatchError):
    pass


class ProductPageNotFoundError(CardmarketwatchError):
    pass
