
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
    rarity: OneOf = OneOf(Rarity, allow_none=True, default=None)
    rare_color: OneOf = OneOf(RareColor, allow_none=True, default=None)
    language_code: OneOf = OneOf(LanguageCode, allow_none=True, default=None)
    article_page: String = String(allow_none=True, default=None)

    def __repr__(self):
        repr_string = (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, "
            f"set={self.set!r}, "
            f"language={str(self.language)!r}, "
            f"condition={str(self.condition)!r}, "
            f"first_edition={self.first_edition!r}, "
            f"signed={self.signed!r}, "
            f"altered={self.altered!r}, "
            f"version={self.version!r}, "
            f"rarity={str(self.rarity or "") or None!r}, "
            f"rare_color={str(self.rare_color or "") or None!r}, "
            f"language_code={str(self.language_code or "") or None!r}, "
            f"article_page={str(self.article_page or "") or None!r})"
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
