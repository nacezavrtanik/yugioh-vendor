
import pytest
from fixtures import (
    firefox_driver, marketwatch, core_tatsunoko, lob_dark_magician, dl_krebons
)


def test_get_search_url_for_single_default_site(marketwatch, core_tatsunoko):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Tatsunoko&site=1"
    assert marketwatch._get_search_url_for_single(core_tatsunoko) == expected


def test_get_search_url_for_single_site_number_3(marketwatch, lob_dark_magician):
    expected = "https://www.cardmarket.com/en/YuGiOh/Products/Search?searchString=Dark+Magician&site=3"
    assert marketwatch._get_search_url_for_single(
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
