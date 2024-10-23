
class UpperString:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError
        setattr(obj, self.private_name, value)

    def __get__(self, obj, obj_type):
        value = getattr(obj, self.private_name)
        return value.upper()


class OneOf:
    def __init__(self, str_enum, *, default):
        self.str_enum = str_enum
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if value is None:
            setattr(obj, self.private_name, None)
        else:
            enum_instance = self.str_enum(value)
            setattr(obj, self.private_name, enum_instance)

    def __get__(self, obj, obj_type):
        if obj is None:
            return self.default
        return getattr(obj, self.private_name, self.default)


class EnforcedType:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, obj_type=None):
        if (obj is None) and (self.default is None):
            # Dataclasses determine whether a descriptor field does or does
            # not have a default value by calling the __get__ method on the
            # class, like so: descriptor.__get__(obj=None, obj_type=cls)
            # We raise an AttributeError here, to let a potential dataclass
            # know that there is no default value.
            # Note that this prevents the actual value None from being a
            # valid default.
            raise AttributeError
        return getattr(obj, self.private_name, self.default)

    def __set__(self, obj, value):
        if (value is None) and (self.allow_none is True):
            setattr(obj, self.private_name, value)
            return
        if isinstance(value, self.enforced_type):
            setattr(obj, self.private_name, value)
            return
        raise TypeError

    def __init__(self, enforced_type, *, default=None, allow_none=False):
        self.enforced_type = enforced_type
        self.default = default
        self.allow_none = allow_none

    def __repr__(self):
        return f"{self.__class__.__name__}({self.enforced_type.__name__})"
