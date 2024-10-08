
from collections.abc import Sequence
import os
import pandas as pd
from cards import Card


class Binder(Sequence):
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    @classmethod
    def from_excel(cls, filepath, name=None):
        if name is None:
            basename = os.path.basename(filepath)
            name = os.path.splitext(basename)[0]
        cards = [
            Card.from_series(row)
            for _, row in pd.read_excel(filepath).iterrows()
        ]
        return cls(name, cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __repr__(self):
        cards_repr = self.cards
        if len(self) > 3:
            cards_repr = f"[{repr(self.cards[0])}, ..., {repr(self.cards[-1])}]"
        return f"Binder(name='{self.name}', cards={cards_repr})"

    def __str__(self):
        return self.name
