
class CardmarketBotError(Exception):
    """Base exception for the cardmarket-bot library"""


class ArticleNotFoundError(CardmarketBotError):
    pass
