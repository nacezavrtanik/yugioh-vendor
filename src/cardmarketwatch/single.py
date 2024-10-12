
class Single:
    LANGUAGE_CODE_SETS = [
        "LOB",
        "MRD",
        "MRL",
        "SRL",
    ]
    LANGUAGE_NUMBERS = {
        "English": 1,
        "French": 2,
        "German": 3,
        "Spanish": 4,
        "Italian": 5,
    }
    CONDITION_NUMBERS = {
        "M": 1,
        "NM": 2,
        "EX": 3,
        "GD": 4,
        "LP": 5,
        "PL": 6,
        "PO": None,
    }

    def __init__(
        self,
        name,
        set,
        *,
        language="English",
        condition="NM",
        first_edition=False,
        signed=False,
        altered=False,
        version=None,
        rarity=None,
        rare_color=None,
        url=None,
        articles=None,
    ):
        self.name = name
        self.set = set
        self.language = language if language != "" else "English"
        self.condition = condition if condition != "" else "NM"
        self.first_edition = first_edition if first_edition != "" else False
        self.signed = signed if signed != "" else False
        self.altered = altered if altered != "" else False
        self.version = version if version != "" else None
        self.rarity = rarity if rarity != "" else None
        self.rare_color = rare_color if rare_color != "" else None
        self.url = url if url != "" else None
        self.articles = articles if articles != "" else None

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.set}')"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Single):
            return NotImplemented
        return all([
            self.name == other.name,
            self.set == other.set,
            self.language == other.language,
            self.condition == other.condition,
            self.first_edition is other.first_edition,
            self.signed is other.signed,
            self.altered is other.altered,
            self.version == other.version,
            self.rarity == other.rarity,
            self.rare_color == other.rare_color,
            self.url == other.url,
            self.articles == other.articles,
        ])

    @property
    def filtered_url(self):
        if self.url is None:
            return self.url

        language_filter = f"language={self.LANGUAGE_NUMBERS.get(self.language)}"
        filters = [language_filter]
        if self.condition != "PO":
            condition_number = self.CONDITION_NUMBERS.get(self.condition)
            condition_filter = f"minCondition={condition_number}"
            filters.append(condition_filter)
        if self.signed is True:
            signed_filter = "isSigned=Y"
            filters.append(signed_filter)
        if self.first_edition is True:
            first_edition_filter = "isFirstEd=Y"
            filters.append(first_edition_filter)
        if self.altered is True:
            altered_filter = "isAltered=Y"
            filters.append(altered_filter)

        return self.url + f"?{"&".join(filters)}"

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
            self.first_edition,
        ]
        return not any(attr is None for attr in other_required_attrs)
