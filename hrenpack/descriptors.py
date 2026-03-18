from typing import Any
from typeguard import check_type
from pyundefined import UndefinedType

no_default = UndefinedType()


class Constant:
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner=None):
        if instance is None: return self
        return self.value


class TypedDescriptor:
    def __init__(self, typing: Any = Any, default: Any = no_default):
        self.typing = typing
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None: return self
        value = instance.__dict__.get(self.name, self.default)
        if value is no_default: raise AttributeError('Attribute \'{}\' does not exist'.format(self.name))
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = check_type(value, self.typing)
