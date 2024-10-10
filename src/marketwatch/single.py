
class Single:
    LANGUAGE_CODE_SETS = [
        "LOB",
        "MRD",
        "MRL",
        "SRL",
    ]

    def __init__(
        self,
        name,
        *,
        set=None,
        rarity=None,
        language=None,
        condition=None,
        edition=None,
        version=None,
        signed=False,
        altered=False,
        article=None,
        offers=None,
    ):
        self.name = name
        self.set = set
        self.rarity = rarity
        self.language = language
        self.condition = condition
        self.edition = edition
        self.version = version
        self.signed = signed,
        self.altered = altered,
        self.article = article
        self.offers = offers

    @property
    def set_is_duelist_league(self):
        return self.set is not None and self.set.startswith("DL")

    @property
    def set_requires_language_code(self):
        return self.set in self.LANGUAGE_CODE_SETS

    @property
    def has_attributes_required_for_evaluation(self):
        if self.set is None:
            return False

        if self.version is None and (
            self.set_is_duelist_league or self.set_requires_language_code
        ):
            return False

        other_required_attrs = [
            self.rarity,
            self.language,
            self.condition,
            self.edition,
        ]
        return not any(attr is None for attr in other_required_attrs)
