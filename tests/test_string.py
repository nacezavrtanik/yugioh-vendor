
import pytest
from vendor.descriptors import String, UpperString, StringOrNone


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


def test_upper_string_access_gets_upper_case_string():
    class C:
        attr = UpperString()
    instance = C()
    instance.attr = "bla"
    assert instance.attr == "BLA"


def test_string_or_none_instantiation_succeeds_for_string_value():
    class C:
        attr = StringOrNone(default=None)
        def __init__(self, attr):
            self.attr = attr
    instance = C("asfd")
    assert instance.attr == "asfd"


def test_string_or_none_instantiation_succeeds_for_none_value():
    class C:
        attr = StringOrNone(default="jojojo")
        def __init__(self, attr):
            self.attr = attr
    instance = C(None)
    assert instance.attr is None
