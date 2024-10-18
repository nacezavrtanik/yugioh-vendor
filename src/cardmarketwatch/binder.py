
import csv
from cardmarketwatch.single import Single
from cardmarketwatch.enums import CSVField
from cardmarketwatch.exceptions import CSVProcessingError


def _process(row):
    processed_row = {}
    for key, value in row.items():
        if value == "":
            continue
        try:
            field = CSVField(key)
        except ValueError:
            continue

        if field.is_string:
            processed_value = value
        elif field.is_integer:
            try:
                processed_value = int(value)
            except ValueError:
                csv_error = CSVProcessingError(
                    f"invalid value '{value}' for field '{field}'; "
                    f"must be integer or empty",
                )
                raise csv_error from None
        elif field.is_boolean:
            if value.lower() == "yes":
                processed_value = True
            elif value.lower() == "no":
                processed_value = False
            else:
                csv_error = CSVProcessingError(
                    f"invalid value '{value}' for field '{field}'; "
                    f"must be 'yes', 'no', or empty",
                )
                raise csv_error from None
        processed_row[field.as_arg()] = processed_value

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
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

    @classmethod
    def from_csv(cls, filepath):
        with open(filepath, "r", newline="") as file:
            return cls(Single(**_process(row)) for row in csv.DictReader(file))

    def to_csv(self, filepath):
        """Save singles in binder to CSV, account for articles."""
