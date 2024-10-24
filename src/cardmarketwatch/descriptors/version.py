
from cardmarketwatch.enums import RareColor


class Version:
    DUELIST_LEAGUE_VERSION_MAPPING = {
        RareColor.BLUE: 1,
        RareColor.GREEN: 2,
        RareColor.GOLD: 3,
        RareColor.SILVER: 4,
    }
    LANGUAGE_CODE_SETS = [
        "LOB",
        "MRD",
        "MRL",
        "SRL",
    ]

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, single, value):
        if (value is not None) and (not isinstance(value, int)):
            raise TypeError(
                f"expected type 'int' or None, got '{type(value)}' instead"
            )
        if value is not None and value <= 0:
            raise ValueError("version must be positive")
        setattr(single, self.private_name, value)

    def __get__(self, single, obj_type):
        if single is None:
            return None
        version = getattr(single, self.private_name, None)
        if version is None:
            version = self.infer_from_single(single)
        return version

    def infer_from_single(self, single):
        if self._set_is_duelist_league(single):
            return self.DUELIST_LEAGUE_VERSION_MAPPING.get(single.rare_color)
        return None

    def _set_requires_language_code(self, single):
        return single.set in self.LANGUAGE_CODE_SETS

    def _set_is_duelist_league(self, single):
        return single.set is not None and single.set.startswith("DL")
