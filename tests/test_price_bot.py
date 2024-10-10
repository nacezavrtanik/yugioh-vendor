
import pytest
from fixtures.price_bot import price_bot, tatsunoko, dark_magician, binder
from marketwatch import PriceBot, Single
from marketwatch.exceptions import ArticleNotFoundError


def test_get_search_url_for_single_default_site(price_bot, tatsunoko):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Tatsunoko&site=1"
    assert price_bot._get_search_url_for_single(tatsunoko) == expected


def test_get_search_url_for_single_site_number_3(price_bot, dark_magician):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Dark+Magician&site=3"
    assert price_bot._get_search_url_for_single(dark_magician, site_number=3) == expected


def test_update_single_with_offers(price_bot, tatsunoko):
    assert False


@pytest.mark.skip("takes too long")
def test_update_binder_with_offers(price_bot, binder):
    with pytest.raises(ArticleNotFoundError):
        price_bot.update_binder_with_offers(binder)
