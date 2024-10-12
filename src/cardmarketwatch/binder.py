
import pandas as pd
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
    def from_excel(cls, filepath, name=None):
        singles = (
            Single(**row.to_dict())
            for _, row in pd.read_excel(filepath).iterrows()
        )
        return cls(singles)

    def to_excel(self, filepath):
        """Save singles in binder to excel, and add columns for offers."""
