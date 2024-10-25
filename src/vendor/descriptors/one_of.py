
class OneOf:
    def __init__(self, str_enum, *, default):
        self.str_enum = str_enum
        self.default = default

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if value is None:
            obj.__dict__[self.private_name] = value
        else:
            enum_instance = self.str_enum(value)
            obj.__dict__[self.private_name] = enum_instance

    def __get__(self, obj, obj_type):
        if obj is None:
            return self.default
        return getattr(obj, self.private_name, self.default)
