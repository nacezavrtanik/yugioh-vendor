
import pytest
from vendor.descriptors import IterableOf


@pytest.mark.parametrize(("type_", "iterable"), [
    (int, [1, 2, 4, 7]),
    (bool, (True, False, True)),
    (str, "ahsdgj"),
])
def test_class_instantiation_succeeds_for_iterable_of_type(type_, iterable):
    class C:
        attr = IterableOf(type_)
        def __init__(self, attr):
            self.attr = attr
    instance = C(iterable)
    assert instance.attr == list(iterable)


@pytest.mark.parametrize("non_iterable", [888, True, None])
def test_class_instantiation_fails_for_non_iterable(non_iterable):
    class C:
        attr = IterableOf(object)
        def __init__(self, attr):
            self.attr = attr
    with pytest.raises(TypeError):
        C(non_iterable)


@pytest.mark.parametrize(("type_", "iterable"), [
    (int, [1, 2, "4", 7]),
    (bool, (None, False, True)),
    (str, range(10)),
])
def test_class_instantiation_fails_for_iterable_of_wrong_type(type_, iterable):
    class C:
        attr = IterableOf(type_)
        def __init__(self, attr):
            self.attr = attr
    with pytest.raises(TypeError):
        C(iterable)


def test_assignment_succeeds_for_iterable_of_type():
    class C():
        attr = IterableOf(int)
    instance = C()
    instance.attr = range(3)
    assert instance.attr == [0, 1, 2]


def test_assignment_fails_for_non_iterable():
    class C():
        attr = IterableOf(int)
    instance = C()
    with pytest.raises(TypeError):
        instance.attr = 15


def test_assignment_fails_for_iterable_of_wrong_type():
    class C():
        attr = IterableOf(int)
    instance = C()
    with pytest.raises(TypeError):
        instance.attr = "kjdfnod"
