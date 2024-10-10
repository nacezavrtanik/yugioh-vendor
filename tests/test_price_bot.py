
import pytest
from fixtures.price_bot import firefox_driver, price_bot, binder
from fixtures.singles import core_tatsunoko, lob_dark_magician, dl_krebons
from marketwatch import PriceBot, Single
from marketwatch.exceptions import ArticleNotFoundError


def test_get_search_url_for_single_default_site(price_bot, core_tatsunoko):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Tatsunoko&site=1"
    assert price_bot._get_search_url_for_single(core_tatsunoko) == expected


def test_get_search_url_for_single_site_number_3(price_bot, lob_dark_magician):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Dark+Magician&site=3"
    assert price_bot._get_search_url_for_single(
        lob_dark_magician, site_number=3
    ) == expected


def test_set_article_attribute_for_single_only_one_version(
    firefox_driver, price_bot, core_tatsunoko
):
    with firefox_driver() as driver:
        price_bot._set_article_attribute_for_single(driver, core_tatsunoko)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Clash-of-Rebellions/Tatsunoko"
    assert core_tatsunoko.article == expected


@pytest.mark.skip("figure out how to store version info")
def test_set_article_attribute_for_single_duelist_league(
    firefox_driver, price_bot, dl_krebons
):
    with firefox_driver() as driver:
        price_bot._set_article_attribute_for_single(driver, dl_krebons)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V2-Rare"
    assert dl_krebons.article == expected


@pytest.mark.skip("cannot implement correctly until I understand the logic")
def test_set_article_attribute_for_single_with_language_code(
    firefox_driver, price_bot, lob_dark_magician
):
    with firefox_driver() as driver:
        price_bot._set_article_attribute_for_single(driver, lob_dark_magician)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Legend-of-Blue-Eyes-White-Dragon/Dark-Magician-V4-Ultra-Rare"
    assert lob_dark_magician.article == expected


@pytest.mark.skip("always fails")
def test_update_single_with_offers(price_bot, core_tatsunoko):
    assert False


@pytest.mark.skip("takes too long")
def test_update_binder_with_offers(price_bot, binder):
    with pytest.raises(ArticleNotFoundError):
        price_bot.update_binder_with_offers(binder)
