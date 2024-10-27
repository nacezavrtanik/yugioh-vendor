
from dataclasses import dataclass, KW_ONLY, asdict
from vendor.enums import (
    Language, Condition, Rarity, RareColor, LanguageCode
)
from vendor.descriptors import Version, OneOf, Bool, String


@dataclass(frozen=True)
class Single:
    name: String = String(predicate=str.title)
    set: String = String(predicate=str.upper)
    _: KW_ONLY
    language: OneOf = OneOf(Language, default=Language.ENGLISH)
    condition: OneOf = OneOf(Condition, default=Condition.NEAR_MINT)
    first_edition: Bool = Bool(default=False)
    signed: Bool = Bool(default=False)
    altered: Bool = Bool(default=False)
    version: Version = Version()
    rarity: OneOf = OneOf(Rarity, default=None)
    rare_color: OneOf = OneOf(RareColor, default=None)
    language_code: OneOf = OneOf(LanguageCode, default=None)
    article_page: String = String(allow_none=True, default=None)

    def __repr__(self):
        # We want the repr to eval into an instance equal to self.
        # This requires us to surround values for certain attributes with
        # quotes, depending on whether they are strings or None.
        rarity_string = f"{self.rarity}" if self.rarity is None else f"'{self.rarity}'"
        rare_color_string = f"{self.rare_color}" if self.rare_color is None else f"'{self.rare_color}'"
        language_code_string = f"{self.language_code}" if self.language_code is None else f"'{self.language_code}'"
        repr_string = (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"set='{self.set}', "
            f"language='{self.language}', "
            f"condition='{self.condition}', "
            f"first_edition={self.first_edition}, "
            f"signed={self.signed}, "
            f"altered={self.altered}, "
            f"version={self.version}, "
            f"rarity={rarity_string}, "
            f"rare_color={rare_color_string}, "
            f"language_code={language_code_string}, "
            f"article_page={self.article_page})"
        )
        return repr_string

    def __str__(self):
        return f"{self.name} ({self.set})"

    @property
    def filtered_article_page(self):
        if self.article_page is None:
            return None

        language_filter = f"language={self.language.cardmarket_id}"
        filters = [language_filter]
        if self.condition is not Condition.POOR:
            condition_filter = f"minCondition={self.condition.cardmarket_id}"
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
        return self.article_page + f"?{"&".join(filters)}"

    def to_dict(self):
       return asdict(self)
