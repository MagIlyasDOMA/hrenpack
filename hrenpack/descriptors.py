from typing import Any, Union, Self, Callable
from pathlib import Path
from pathlike_typing import PathLike
from typeguard import check_type
from hrenpack.encapsulation import getattr_plus, getattr_strict
from hrenpack.no_default import no_default


class BaseDescriptor:
    def __set_name__(self, owner, name):
        self.name = name


class Constant:
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner=None):
        if instance is None: return self
        return self.value


class ObjectConstant(BaseDescriptor):
    def __init__(self, func_or_type: Union[Callable, type], send_instance: bool = False, *args, **kwargs):
        self.func_or_type = func_or_type
        self.send_instance = send_instance
        self.args = args
        self.kwargs = kwargs

    def _create_object(self, instance):
        if self.send_instance: args = (instance, *self.args)
        else: args = self.args
        return self.func_or_type(*args, **self.kwargs)

    def __get__(self, instance, owner=None):
        if instance is None: return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self._create_object(instance)
        return instance.__dict__[self.name]


class TypedDescriptor(BaseDescriptor):
    def __init__(self, typing: Any = Any, default: Any = no_default):
        self.typing = typing
        self.default = default

    def __get__(self, instance, owner=None):
        if instance is None: return self
        value = instance.__dict__.get(self.name, self.default)
        if value is no_default: raise AttributeError('Attribute \'{}\' does not exist'.format(self.name))
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = check_type(value, self.typing)


class PathLikeDescriptor(BaseDescriptor):
    def __init__(self, missing_ok: bool = False):
        self.missing_ok = missing_ok

    def __get__(self, instance, owner=None) -> Union[Path, Self, None]:
        if instance is None: return self
        value = instance.__dict__.get(self.name, None)
        return Path(value) if value is not None else None

    def __set__(self, instance, value: PathLike):
        if isinstance(value, PathLike):
            value = Path(value)
            if self.missing_ok or value.exists():
                instance.__dict__[self.name] = value
            raise FileNotFoundError(f'Path \'{value}\' does not exist')
        raise TypeError('value must be a Path or str')


class Boolean(TypedDescriptor):
    def __init__(self, default: bool = False):
        super().__init__(bool, default)

    def __get__(self, instance, owner=None) -> bool:
        return super().__get__(instance, owner)

    def __set__(self, instance, value: bool):
        super().__set__(instance, value)


class SubAttribute(BaseDescriptor):
    def __init__(self, attr_name: str, absolute: bool = False, default: Any = no_default):
        self.attr_name = attr_name
        self.absolute = absolute
        self.default = default

    def __get__(self, instance, owner=None):
        try:
            value = getattr_plus(instance, self.attr_name, self.default, catch_errors=False)
        except AttributeError as error:
            value = self.default
            if value is no_default: raise error
        return value if self.absolute else getattr_strict(value, self.name)