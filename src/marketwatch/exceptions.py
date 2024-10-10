
class MarketwatchError(Exception):
    """Base exception for the marketwatch library"""


class ArticleNotFoundError(MarketwatchError):
    pass
