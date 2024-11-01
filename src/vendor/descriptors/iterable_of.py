
import collections


class IterableOf:
    def __init__(self, type_):
        self.type_ = type_

    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        self.public_name = name

    def __set__(self, instance, value):
        value = list(self.validate(value))
        setattr(instance, self.private_name, value)

    def validate(self, iterable):
        if not isinstance(iterable, collections.abc.Iterable):
            msg = (
                f"argument '{self.public_name}' must be an iterable "
                f"of '{self.type_.__name__}' instances"
            )
            type_error = TypeError(msg)
            type_error.add_note(f"Got type: {type(iterable).__name__}")
            type_error.add_note(f"Got value: {iterable!r}")
            raise type_error
        for i, item in enumerate(iterable):
            if not isinstance(item, self.type_):
                msg = (
                    f"all items in the '{self.public_name}' iterable "
                    f"must be instances of type '{self.type_.__name__}'"
                )
                type_error = TypeError(msg)
                type_error.add_note(
                    f"Got item type: {type(item).__name__} (at index {i})"
                )
                type_error.add_note(f"Got item value: {item!r}")
                raise type_error
            yield item

    def __get__(self, instance, cls):
        return getattr(instance, self.private_name)
