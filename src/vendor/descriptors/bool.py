
class Bool():
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if not isinstance(value, bool):
            raise TypeError
        setattr(obj, self.private_name, value)

    def __get__(self, obj, objtype):
        return getattr(obj, self.private_name, self.default)

    def __init__(self, *, default):
        self.default = default
