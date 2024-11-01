
class _SENTINEL: pass
MISSING = _SENTINEL()


class String():
    def __init__(
        self, *, predicate=lambda x: x, allow_none=False, default=MISSING
    ):
        assert sum([
            default is MISSING,
            isinstance(default, str),
            default is None and allow_none is True,
        ]) == 1
        self.predicate = predicate
        self.allow_none = allow_none
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        self.public_name = name

    def __set__(self, obj, value):
        if isinstance(value, str):
            pass
        elif value is None and self.allow_none is True:
            pass
        else:
            msg = (
                f"argument '{self.public_name}' must be of type 'str', "
                f"got type '{type(value).__name__}' instead"
            )
            if self.allow_none is True:
                msg = (
                    f"argument '{self.public_name}' must be of type 'str', "
                    f"or None, got type '{type(value).__name__}' instead"
                )
            raise TypeError(msg)
        obj.__dict__[self.private_name] = value

    def __get__(self, obj, objtype):
        if obj is None and self.default is not MISSING:
            return self.default
        if self.default is MISSING:
            args = obj, self.private_name
        else:
            args = obj, self.private_name, self.default
        value = getattr(*args)
        if isinstance(value, str):
            value = self.predicate(value)
        return value
