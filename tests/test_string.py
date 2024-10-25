
import pytest
from vendor.descriptors import String


def test_string_instantiation_succeeds_for_string_value():
    class C:
        attr = String()
        def __init__(self, attr):
            self.attr = attr
    instance = C("asfd")
    assert instance.attr == "asfd"


def test_string_instantiation_fails_for_non_string_value():
    class C:
        attr = String()
        def __init__(self, attr):
            self.attr = attr
    with pytest.raises(TypeError):
        C(None)


def test_accessing_string_with_predicate_upper_gets_upper_case_string():
    class C:
        attr = String(predicate=str.upper)
    instance = C()
    instance.attr = "bla"
    assert instance.attr == "BLA"


def test_accessing_string_with_predicate_title_gets_title_string():
    class C:
        attr = String(predicate=str.title)
    instance = C()
    instance.attr = "It's time to DUEL!"
    assert instance.attr == "It'S Time To Duel!"
