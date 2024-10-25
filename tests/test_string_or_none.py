
from vendor.descriptors import StringOrNone


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
