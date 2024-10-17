
import pytest
from cardmarketwatch.descriptors import UpperString


def test_upper_string_fails_when_assigned_non_string():
    class C:
        string = UpperString()
    instance = C()
    with pytest.raises(TypeError):
        instance.string = 123


def test_upper_string_gives_uppercase_string():
    class C:
        string = UpperString()
    instance = C()
    instance.string = "it's time to duel!"
    expected = "IT'S TIME TO DUEL!"
    assert instance.string == expected


def test_upper_string_works_for_multiple_attribute_assignments():
    class C:
        string = UpperString()
    instance = C()
    instance.string = "monsuta caado"
    instance.string = "card games on motorcycles"
    instance.string = "leather pants"
    expected = "LEATHER PANTS"
    assert instance.string == expected
