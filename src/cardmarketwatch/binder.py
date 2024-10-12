
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


class Binder(list):
    def __init__(self, iterable):
        super().__init__(_validate(iterable))

    @classmethod
    def from_csv(cls, filepath):
        with open(filepath, newline="") as file:
            return cls(Single(**row) for row in csv.DictReader(file))

    def to_csv(self, filepath):
        """Save singles in binder to CSV, account for articles."""
