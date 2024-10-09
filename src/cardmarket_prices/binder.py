
import pandas as pd
from card import Card


def _validate(iterable):
    for item in iterable:
        if isinstance(item, Card):
            yield item
        else:
            raise TypeError(
                "direct instantiation of Binder requires "
                "iterable of Card objects"
            )


class Binder(list):
    def __init__(self, iterable):
        super().__init__(_validate(iterable))

    @classmethod
    def from_excel(cls, filepath, name=None):
        cards = (
            Card(**row.to_dict())
            for _, row in pd.read_excel(filepath).iterrows()
        )
        return cls(cards)

    def to_excel(self, filepath):
        """Save cards in binder to excel, and add columns for offers."""
