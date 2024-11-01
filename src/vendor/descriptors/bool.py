
class Bool():
    def __init__(self, *, default):
        assert isinstance(default, bool)
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        self.public_name = name

    def __set__(self, obj, value):
        if not isinstance(value, bool):
            raise TypeError(
                f"argument '{self.public_name}' must be of type 'bool', "
                f"got type '{type(value).__name__}' instead"
            )
        obj.__dict__[self.private_name] = value

    def __get__(self, obj, objtype):
        return getattr(obj, self.private_name, self.default)
