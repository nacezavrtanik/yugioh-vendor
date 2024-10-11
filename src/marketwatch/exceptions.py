
class MarketwatchError(Exception):
    """Base exception for the marketwatch library"""


class ProductPageNotFoundError(MarketwatchError):
    pass
