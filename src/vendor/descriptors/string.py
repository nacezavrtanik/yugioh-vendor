
class String():
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError
        obj.__dict__[self.private_name] = value

    def __get__(self, obj, objtype):
        return getattr(obj, self.private_name)


class UpperString(String):
    def __get__(self, obj, objtype):
        value = getattr(obj, self.private_name)
        return value.upper()


class StringOrNone:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if (value is not None) and (not isinstance(value, str)):
            raise TypeError
        obj.__dict__[self.private_name] = value

    def __get__(self, obj, objtype):
        if obj is None:
            return
        return getattr(obj, self.private_name, self.default)

    def __init__(self, *, default):
        self.default = default
