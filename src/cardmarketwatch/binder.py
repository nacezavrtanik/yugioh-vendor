
import csv
from cardmarketwatch.single import Single


def _validate(iterable):
    for item in iterable:
        if isinstance(item, Single):
            yield item
        else:
            raise TypeError(
                "direct instantiation of Binder requires "
                "iterable of Single objects"
            )


def _process(row):
    boolean_columns = ["first_edition", "signed", "altered"]
    integer_columns = ["version"]

    processed_row = {}
    for key, value in row.items():
        if key in boolean_columns:
            processed_row[key] = False if value == "" else True
        elif key in integer_columns:
            if value != "":
                processed_row[key] = int(value)
        else:
            if value != "":
                processed_row[key] = value

    return processed_row


class Binder(list):
    def __init__(self, iterable):
        super().__init__(_validate(iterable))

    @staticmethod
    def create_csv_template(filepath):
        content = (
            "name,set,language,condition,first_edition,signed,altered,version,rarity,rare_color,url\n"
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
