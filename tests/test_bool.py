
import pytest
from vendor.descriptors.bool import Bool


def test_instantiation_succeeds_for_boolean_value():
    class C:
        attr = Bool(default=True)
        def __init__(self, attr):
            self.attr = attr
    instance = C(False)
    assert instance.attr is False


def test_instantiation_succeeds_for_non_boolean_value():
    class C:
        attr = Bool(default=True)
        def __init__(self, attr):
            self.attr = attr
    with pytest.raises(TypeError):
        instance = C(123)


def test_assignment_succeeds_for_boolean_value():
    class C:
        attr = Bool(default=True)
    instance = C()
    instance.attr = False
    assert instance.attr is False


def test_assignment_fails_for_non_boolean_value():
    class C:
        attr = Bool(default=True)
    instance = C()
    with pytest.raises(TypeError):
        instance.attr = "asd"
