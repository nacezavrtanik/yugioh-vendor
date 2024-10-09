
class Card:
    SEARCH_URL_TEMPLATE = (
        "https://www.cardmarket.com/en/YuGiOh/Products/Search"
        "?searchString={search_term}"
        "&site={site_number}"
    )

    def __init__(
        self,
        name,
        set_,
        rarity,
        language,
        condition,
        edition,
        offers=None,
    ):
        self.name = name
        self.set_ = set_
        self.rarity = rarity
        self.language = language
        self.condition = condition
        self.edition = edition
        self.offers = offers

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
            set_=series["Set"],
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
        return f"Card('{self.name}', '{self.set_}', '{self.rarity}', '{self.language}', '{self.condition}', '{self.edition}')"

    def __str__(self):
        return self.name
