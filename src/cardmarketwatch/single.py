
from dataclasses import dataclass, KW_ONLY
from cardmarketwatch.article import Article
from cardmarketwatch.enums import (
    Language, Condition, Rarity, RareColor, LanguageCode
)
from cardmarketwatch.descriptors import (
    Version, OneOf, Bool, String, UpperString, StringOrNone
)


@dataclass
class Single:
    name: String = String()
    set: UpperString = UpperString()
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
    article_page: StringOrNone = StringOrNone(default=None)
    articles: list[Article] = None

    def __str__(self):
        return f"{self.name} ({self.set})"

    @property
    def url(self):
        return self.article_page

    @property
    def filtered_article_page(self):
        if self.article_page is None:
            return self.article_page

        language_filter = f"language={self.language.cardmarket_id}"
        filters = [language_filter]
        if self.condition != "PO":
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
