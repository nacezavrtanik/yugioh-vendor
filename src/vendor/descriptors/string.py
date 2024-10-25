
class String():
    def __init__(self, *, predicate=lambda x: x):
        self.predicate = predicate

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError
        obj.__dict__[self.private_name] = value

    def __get__(self, obj, objtype):
        value = getattr(obj, self.private_name)
        return self.predicate(value)
