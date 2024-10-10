
import pytest
from fixtures.price_bot import price_bot, binder
from marketwatch import PriceBot, Single
from marketwatch.exceptions import ArticleNotFoundError


def test_update_binder_with_offers(price_bot, binder):
    with pytest.raises(ArticleNotFoundError):
        price_bot.update_binder_with_offers(binder)
