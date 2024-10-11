
import pytest
from marketwatch.price import Price


def test_instantiation_succeeds_for_float_and_unit():
    Price(39.99, "USD")


def test_instantiation_fails_for_missing_unit():
    with pytest.raises(TypeError):
        Price(39.99)


def test_repr():
    price = Price(9.99, "EUR")
    expected = "Price(value=9.99, unit='EUR')"
    assert repr(price) == expected


def test_str():
    price = Price(0.49, "BPD")
    expected = "0.49 BPD"
    assert str(price) == expected
