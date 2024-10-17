
class UpperString:
    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError
        setattr(obj, self._name, value)

    def __get__(self, obj, obj_type):
        value = getattr(obj, self._name)
        return value.upper()

