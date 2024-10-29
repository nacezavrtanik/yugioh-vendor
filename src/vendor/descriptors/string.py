
class String():

    # This is a dummy value representing a missing default.
    # It is intentionally a non-string and is not None.
    # This allows for both any string and None to be actual
    # values of String.default instance attributes.
    _MISSING = -9999

    def __init__(
        self, *, predicate=lambda x: x, allow_none=False, default=_MISSING
    ):
        if default is not self._MISSING:
            if isinstance(default, str):
                pass
            elif default is None and allow_none is True:
                pass
            else:
                raise ValueError(
                    "kwarg 'default' must be a str, "
                    "or None (requires allow_none=True)"
                )
        self.predicate = predicate
        self.allow_none = allow_none
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if isinstance(value, str):
            pass
        elif value is None and self.allow_none is True:
            pass
        else:
            raise TypeError(
                "a value of the String descriptor can only be a string, "
                "or None (requires allow_none=True)"
            )
        obj.__dict__[self.private_name] = value

    def __get__(self, obj, objtype):
        if obj is None:
            return
        if self.default is self._MISSING:
            args = obj, self.private_name
        else:
            args = obj, self.private_name, self.default
        value = getattr(*args)
        if isinstance(value, str):
            value = self.predicate(value)
        return value
