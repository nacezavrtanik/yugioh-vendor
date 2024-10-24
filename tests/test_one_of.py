
import enum
import pytest
from cardmarketwatch.descriptors import OneOf


def test_instantiation_works_for_string_value():
    class Letter(enum.StrEnum):
        A = "a"
        B = "b"
        C = "c"
    class C:
        letter = OneOf(Letter, default=Letter.A)
        def __init__(self, letter):
            self.letter = letter
    instance = C("b")
    assert instance.letter is Letter.B


def test_instantiation_works_for_none_value():
    class Letter(enum.StrEnum):
        A = "a"
        B = "b"
        C = "c"
    class C:
        letter = OneOf(Letter, default=Letter.A)
        def __init__(self, letter):
            self.letter = letter
    instance = C(None)
    assert instance.letter is None


def test_one_of_works_for_multiple_attribute_assignments():
    class Letter(enum.StrEnum):
        A = "a"
        B = "b"
        C = "c"
    class C:
        letter = OneOf(Letter, default=Letter.A)
    instance = C()
    assert instance.letter is Letter.A
    instance.letter = None
    assert instance.letter is None
    instance.letter = "b"
    assert instance.letter is Letter.B


def test_one_of_fails_when_assigned_invalid_string():
    class Letter(enum.StrEnum):
        A = "a"
        B = "b"
        C = "c"
    class C:
        letter = OneOf(Letter, default=Letter.A)
    instance = C()
    with pytest.raises(ValueError):
        instance.letter = "d"
