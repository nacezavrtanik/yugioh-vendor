
import pytest
from vendor.descriptors import String


def test_string_instantiation_succeeds_for_string_default_value():
    string = String(default="abc")
    assert string.default == "abc"


def test_string_instantiation_fails_for_none_default_value():
    with pytest.raises(ValueError):
        String(default=None)


def test_string_instantiation_succeeds_for_none_default_value():
    string = String(allow_none=True, default=None)
    assert string.default is None


@pytest.mark.parametrize("value", [123, -9999, True, ("dfg", None)])
def test_string_instantiation_fails_for_non_string_non_none_default(value):
    with pytest.raises(ValueError):
        String(default=value)


def test_class_instantiation_succeeds_for_string_value():
    class C:
        attr = String()
        def __init__(self, attr):
            self.attr = attr
    instance = C("asfd")
    assert instance.attr == "asfd"


def test_class_instantiation_fails_for_none_value():
    class C:
        attr = String()
        def __init__(self, attr):
            self.attr = attr
    with pytest.raises(TypeError):
        C(None)


def test_class_instantiation_succeeds_for_none_value():
    class C:
        attr = String(allow_none=True)
        def __init__(self, attr):
            self.attr = attr
    instance = C(None)
    assert instance.attr is None


@pytest.mark.parametrize("value", [1234, False, (None, "jhg")])
def test_class_instantiation_fails_for_non_string_non_none_value(value):
    class C:
        attr = String()
        def __init__(self, attr):
            self.attr = attr
    with pytest.raises(TypeError):
        C(value)


def test_class_instantiation_succeeds_for_none_default_value():
    class C:
        attr = String(allow_none=True, default=None)
    instance = C()
    assert instance.attr is None


def test_class_instantiation_succeeds_for_string_default_value():
    class C:
        attr = String(default="jojojo")
    instance = C()
    assert instance.attr == "jojojo"


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


def test_accessing_string_succeeds_for_default_and_predicate():
    class C:
        attr = String(predicate=str.lower, allow_none=True, default="HOHOHO")
    instance = C()
    assert instance.attr == "hohoho"
    instance.attr = None
    assert instance.attr is None
    instance.attr = "goGOgo"
    assert instance.attr == "gogogo"
