
from enum import StrEnum, auto


class CSVField(StrEnum):
    NAME = "Name"
    SET = "Set"
    LANGUAGE = "Language"
    CONDITION = "Condition"
    FIRST_EDITION = "First Edition"
    SIGNED = "Signed"
    ALTERED = "Altered"
    VERSION = "Version"
    RARITY = "Rarity"
    RARE_COLOR = "Rare Color"
    PRODUCT_PAGE = "Product Page"

    @property
    def is_string(self):
        return self in [
            self.NAME,
            self.SET,
            self.LANGUAGE,
            self.CONDITION,
            self.RARITY,
            self.RARE_COLOR,
            self.PRODUCT_PAGE,
        ]

    @property
    def is_integer(self):
        return self in [self.VERSION]

    @property
    def is_boolean(self):
        return self in [self.FIRST_EDITION, self.SIGNED, self.ALTERED]

    def as_arg(self):
        return self.lower().replace(" ", "_")


class AliasedStrEnum(StrEnum):
    @classmethod
    def _get_aliases(cls):
        raise NotImplementedError(
            "subclasses of AliasedStrEnum must override _get_aliases"
        )

    @classmethod
    def _missing_(cls, string):
        if string is None:
            return None
        if not isinstance(string, str):
            raise TypeError

        aliases = cls._get_aliases()
        aliases = {
            instance: aliases.get(instance, []) + [instance.lower()]
            for instance in cls
        }
        string = string.lower()
        for instance, alias_list  in aliases.items():
            if string in alias_list:
                return instance
        return None


class Language(AliasedStrEnum):
    ENGLISH = "English"
    FRENCH = "French"
    GERMAN = "German"
    SPANISH = "Spanish"
    ITALIAN = "Italian"
    PORTUGUESE = "Portuguese"
    JAPANESE = "Japanese"
    KOREAN = "Korean"

    @classmethod
    def _get_aliases(cls):
        return {
            cls.ENGLISH: ["en", "eng"],
            cls.FRENCH: ["fr", "fra", "fre"],
            cls.GERMAN: ["de", "deu", "ger"],
            cls.SPANISH: ["es", "spa"],
            cls.ITALIAN: ["it", "ita"],
            cls.PORTUGUESE: ["pt", "por"],
            cls.JAPANESE: ["ja", "jpn"],
            cls.KOREAN: ["ko", "kor"],
        }

    @property
    def cardmarket_id(self):
        ids = {
            Language.ENGLISH: 1,
            Language.FRENCH: 2,
            Language.GERMAN: 3,
            Language.SPANISH: 4,
            Language.ITALIAN: 5,
        }
        return ids.get(self)


class Condition(AliasedStrEnum):
    MINT = "M"
    NEAR_MINT = "NM"
    EXCELLENT = "EX"
    GOOD = "GD"
    LIGHT_PLAYED = "LP"
    PLAYED = "PL"
    POOR = "PO"

    @classmethod
    def _get_aliases(cls):
        return {
            cls.MINT: ["mint"],
            cls.NEAR_MINT: ["near mint"],
            cls.EXCELLENT: ["excellent"],
            cls.GOOD: ["good"],
            cls.LIGHT_PLAYED: ["light played"],
            cls.PLAYED: ["played"],
            cls.POOR: ["poor"],
        }

    @property
    def cardmarket_id(self):
        ids = {
            Condition.MINT: 1,
            Condition.NEAR_MINT: 2,
            Condition.EXCELLENT: 3,
            Condition.GOOD: 4,
            Condition.LIGHT_PLAYED: 5,
            Condition.PLAYED: 6,
            Condition.POOR: None,
        }
        return ids.get(self)


class Rarity(AliasedStrEnum):
    COMMON = "C"
    RARE = "R"
    SUPER_RARE = "SR"
    ULTRA_RARE = "UR"
    ULTIMATE_RARE = "UtR"
    SECRET_RARE = "ScR"
    STARLIGHT_RARE = "SLR"
    GHOST_RARE = "GR"
    SPECIAL = "Special"

    @classmethod
    def _get_aliases(cls):
        return {
            cls.COMMON: ["common"],
            cls.RARE: ["rare"],
            cls.SUPER_RARE: ["super rare"],
            cls.ULTRA_RARE: ["ultra rare"],
            cls.ULTIMATE_RARE: ["ultimate rare"],
            cls.SECRET_RARE: ["secret rare"],
            cls.STARLIGHT_RARE: ["starlight rare"],
            cls.GHOST_RARE: ["ghost rare"],
        }


class RareColor(AliasedStrEnum):
    BLUE = "blue"
    GREEN = "green"
    GOLD = "gold"
    SILVER = "silver"

    @classmethod
    def _get_aliases(cls):
        return {}
