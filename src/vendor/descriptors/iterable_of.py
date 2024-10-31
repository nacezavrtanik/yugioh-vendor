
import collections


class IterableOf:
    def __init__(self, type_):
        self.type = type_

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __set__(self, instance, value):
        value = list(self.validate(value))
        setattr(instance, self.private_name, value)

    def validate(self, iterable):
        if not isinstance(iterable, collections.abc.Iterable):
            raise TypeError
        for item in iterable:
            if not isinstance(item, self.type):
                raise TypeError
            yield item

    def __get__(self, instance, cls):
        return getattr(instance, self.private_name)
