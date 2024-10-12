
import pytest
from fixtures.marketwatch import firefox_driver, marketwatch, binder
from fixtures.singles import core_tatsunoko, lob_dark_magician, dl_krebons
from cardmarketwatch import Marketwatch, Single


def test_generate_search_url_for_single_default_site(marketwatch, core_tatsunoko):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Tatsunoko&site=1"
    assert marketwatch._generate_search_url_for_single(core_tatsunoko) == expected


def test_generate_search_url_for_single_site_number_3(marketwatch, lob_dark_magician):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Dark+Magician&site=3"
    assert marketwatch._generate_search_url_for_single(
        lob_dark_magician, site_number=3
    ) == expected


def test_get_single_name_for_version_only_one_version(
    marketwatch, core_tatsunoko
):
    expected = "Tatsunoko"
    assert marketwatch._get_single_name_for_version(core_tatsunoko) == expected


def test_get_single_name_for_version_duelist_league(marketwatch, dl_krebons):
    expected = "Krebons (V.2 - Rare)"
    assert marketwatch._get_single_name_for_version(dl_krebons) == expected


@pytest.mark.skip("cannot implement correctly until I understand the logic")
def test_get_single_name_for_version_with_language_code(
    marketwatch, lob_dark_magician
):
    expected = "Dark Magician (V.4 - Ultra Rare)"
    assert marketwatch._get_single_name_for_version(lob_dark_magician) == expected


@pytest.mark.slow
def test_lookup_url_for_single_only_one_version(
    firefox_driver, marketwatch, core_tatsunoko
):
    with firefox_driver() as driver:
        marketwatch._lookup_url_for_single(driver, core_tatsunoko)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Clash-of-Rebellions/Tatsunoko"
    assert core_tatsunoko.url == expected


@pytest.mark.slow
def test_lookup_url_for_single_duelist_league(
    firefox_driver, marketwatch, dl_krebons
):
    with firefox_driver() as driver:
        marketwatch._lookup_url_for_single(driver, dl_krebons)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V2-Rare"
    assert dl_krebons.url == expected


@pytest.mark.skip("cannot implement correctly until I understand the logic")
def test_lookup_url_for_single_with_language_code(
    firefox_driver, marketwatch, lob_dark_magician
):
    with firefox_driver() as driver:
        marketwatch._lookup_url_for_single(driver, lob_dark_magician)
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Singles/Legend-of-Blue-Eyes-White-Dragon/Dark-Magician-V4-Ultra-Rare"
    assert lob_dark_magician.url == expected
