
from dataclasses import dataclass, KW_ONLY
from cardmarketwatch.article import Article
from cardmarketwatch.enums import Language, Condition, Rarity, RareColor
from cardmarketwatch.descriptors import UpperString


@dataclass
class Single:
    name: str
    set: UpperString
    _: KW_ONLY
    language: Language = Language.ENGLISH
    condition: Condition = Condition.NEAR_MINT
    first_edition: bool = False
    signed: bool = False
    altered: bool = False
    version: int = None
    rarity: Rarity = None
    rare_color: RareColor = None
    product_page: str = None
    articles: list[Article] = None

    LANGUAGE_CODE_SETS = [
        "LOB",
        "MRD",
        "MRL",
        "SRL",
    ]
    LANGUAGE_NUMBERS = {
        Language.ENGLISH: 1,
        Language.FRENCH: 2,
        Language.GERMAN: 3,
        Language.SPANISH: 4,
        Language.ITALIAN: 5,
    }
    CONDITION_NUMBERS = {
        Condition.MINT: 1,
        Condition.NEAR_MINT: 2,
        Condition.EXCELLENT: 3,
        Condition.GOOD: 4,
        Condition.LIGHT_PLAYED: 5,
        Condition.PLAYED: 6,
        Condition.POOR: None,
    }

    def __str__(self):
        return f"{self.name} ({self.set})"

    @property
    def filtered_product_page(self):
        if self.product_page is None:
            return self.product_page

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

        return self.product_page + f"?{"&".join(filters)}"

    @property
    def url(self):
        return self.product_page

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
