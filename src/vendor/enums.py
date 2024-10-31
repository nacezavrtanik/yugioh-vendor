
from enum import StrEnum


class SingleAttribute(StrEnum):
    NAME = "name"
    SET = "set"
    LANGUAGE = "language"
    CONDITION = "condition"
    FIRST_EDITION = "first_edition"
    SIGNED = "signed"
    ALTERED = "altered"
    VERSION = "version"
    RARITY = "rarity"
    RARE_COLOR = "rare_color"
    LANGUAGE_CODE = "language_code"
    ARTICLE_PAGE = "article_page"

    @property
    def is_string(self):
        return self in [
            self.NAME,
            self.SET,
            self.LANGUAGE,
            self.CONDITION,
            self.RARITY,
            self.RARE_COLOR,
            self.LANGUAGE_CODE,
            self.ARTICLE_PAGE,
        ]

    @property
    def is_integer(self):
        return self in [self.VERSION]

    @property
    def is_boolean(self):
        return self in [self.FIRST_EDITION, self.SIGNED, self.ALTERED]


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
    COMMON = "Common"
    RARE = "Rare"
    SUPER_RARE = "Super Rare"
    ULTRA_RARE = "Ultra Rare"
    ULTIMATE_RARE = "Ultimate Rare"
    SECRET_RARE = "Secret Rare"
    STARLIGHT_RARE = "Starlight Rare"
    GHOST_RARE = "Ghost Rare"
    SPECIAL = "Special"

    @classmethod
    def _get_aliases(cls):
        return {
            cls.COMMON: ["c"],
            cls.RARE: ["r"],
            cls.SUPER_RARE: ["sr"],
            cls.ULTRA_RARE: ["ur"],
            cls.ULTIMATE_RARE: ["utr"],
            cls.SECRET_RARE: ["scr"],
            cls.STARLIGHT_RARE: ["slr"],
            cls.GHOST_RARE: ["gr"],
        }


class RareColor(AliasedStrEnum):
    BLUE = "blue"
    GREEN = "green"
    GOLD = "gold"
    SILVER = "silver"

    @classmethod
    def _get_aliases(cls):
        return {}


class LanguageCode(AliasedStrEnum):
    A = "-A"
    E = "-E"
    EN = "-EN"
    F = "-F"
    G = "-G"
    NONE = "-"

    @classmethod
    def _get_aliases(cls):
        return {
            cls.A: ["australian", "a"],
            cls.EN: ["english", "en"],
            cls.E: ["spanish", "e"],
            cls.G: ["german", "g"],
            cls.F: ["french", "f"],
            cls.NONE: ["american", "none"],
        }
