
from collections import namedtuple
import pandas as pd
from config import EXCEL


class Card(namedtuple("Card", ["name", "set", "rarity", "language", "condition", "edition"])):
    __slots__ = ()
    SEARCH_URL_TEMPLATE = (
        "https://www.cardmarket.com/en/YuGiOh/Products/Search"
        "?searchString={search_term}"
        "&site={site_number}"
    )

    @classmethod
    def from_series(cls, series):
        required_columns = [
            "Card name",
            "Set",
            "Rarity",
            "Language",
            "Condition",
            "Edition",
        ]
        for column in required_columns:
            if column not in series.index:
                raise ValueError(f"column {column} not in index")
        instance = cls(
            name=series["Card name"],
            set=series["Set"],
            rarity=series["Rarity"],
            language=series["Language"],
            condition=series["Condition"],
            edition=series["Edition"],
            )
        return instance

    def get_search_url(self, site_number=1):
        return self.SEARCH_URL_TEMPLATE.format(
            search_term=self.name.replace(" ", "+"),
            site_number=site_number,
            )

    def __repr__(self):
        return f"Card('{self.name}', '{self.set}', '{self.rarity}', '{self.language}', '{self.condition}', '{self.edition}')"

    def __str__(self):
        return self.name


def read_cards_from_excel(filepath):
    excel = pd.read_excel(filepath)
    for _, row in excel.iterrows():
        card = Card.from_series(row)
        yield card


class Binder(list):
    @classmethod
    def from_excel(cls, filepath):
        return cls(Card.from_series(row) for _, row in pd.read_excel(filepath).iterrows())
