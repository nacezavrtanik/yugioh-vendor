
import enum
import csv
from cardmarketwatch.single import Single


class CSVField(enum.StrEnum):
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


def _process(row):
    processed_row = {}
    for key, value in row.items():
        try:
            field = CSVField(key)
        except ValueError:
            continue

        if field.is_string:
            if value != "":
                processed_row[field.as_arg()] = value
        elif field.is_integer:
            if value != "":
                processed_row[field.as_arg()] = int(value)
        elif field.is_boolean:
            processed_row[field.as_arg()] = False if value == "" else True

    return processed_row


def _validate(iterable):
    for item in iterable:
        if isinstance(item, Single):
            yield item
        else:
            raise TypeError(
                "direct instantiation of Binder requires "
                "iterable of Single objects"
            )


class Binder(list):
    def __init__(self, iterable):
        super().__init__(_validate(iterable))

    @staticmethod
    def create_csv_template(filepath):
        content = (
            "Name,Set,Language,Condition,First Edition,Signed,Altered,Version,Rarity,Rare Color,Product Page\n"
            "Tatsunoko,CORE,English,NM,yes,,,,,,\n"
            "Krebons,DL09,,GD,,yes,,1,R,blue,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Duelist-League-09/Krebons-V1-Rare\n"
            '"Brionac, Dragon of the Ice Barrier",HA01,French,,,,yes,,ScR,,https://www.cardmarket.com/en/YuGiOh/Products/Singles/Hidden-Arsenal/Brionac-Dragon-of-the-Ice-Barrier\n'
        )
        with open(filepath, "w") as file:
            file.write(content)

    @classmethod
    def from_csv(cls, filepath):
        with open(filepath, newline="") as file:
            return cls(Single(**_process(row)) for row in csv.DictReader(file))

    def to_csv(self, filepath):
        """Save singles in binder to CSV, account for articles."""
