
import pytest
from fixtures.price_bot import (
    firefox_driver, price_bot, tatsunoko, dark_magician, binder
)
from marketwatch import PriceBot, Single
from marketwatch.exceptions import ArticleNotFoundError


def test_get_search_url_for_single_default_site(price_bot, tatsunoko):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Tatsunoko&site=1"
    assert price_bot._get_search_url_for_single(tatsunoko) == expected


def test_get_search_url_for_single_site_number_3(price_bot, dark_magician):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Dark+Magician&site=3"
    assert price_bot._get_search_url_for_single(dark_magician, site_number=3) == expected


def test_set_article_attribute_for_single_only_one_version(
    firefox_driver, price_bot, tatsunoko
):
    with firefox_driver() as driver:
        price_bot._set_article_attribute_for_single(driver, tatsunoko)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Clash-of-Rebellions/Tatsunoko"
    assert tatsunoko.article == expected


@pytest.mark.skip("figure out how to store version info")
def test_set_article_attribute_for_single_duelist_league(
    firefox_driver, price_bot, dl_krebons
):
    with firefox_driver() as driver:
        price_bot._set_article_attribute_for_single(driver, dl_krebons)
    expected = ""
    assert dl_krebons.article == expected


@pytest.mark.skip("cannot implement correctly until I understand the logic")
def test_set_article_attribute_for_single_with_language_code(
    firefox_driver, price_bot, dark_magician
):
    with firefox_driver() as driver:
        price_bot._set_article_attribute_for_single(driver, dark_magician)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Legend-of-Blue-Eyes-White-Dragon/Dark-Magician-V4-Ultra-Rare"
    assert dark_magician.article == expected


@pytest.mark.skip("always fails")
def test_update_single_with_offers(price_bot, tatsunoko):
    assert False


@pytest.mark.skip("takes too long")
def test_update_binder_with_offers(price_bot, binder):
    with pytest.raises(ArticleNotFoundError):
        price_bot.update_binder_with_offers(binder)
