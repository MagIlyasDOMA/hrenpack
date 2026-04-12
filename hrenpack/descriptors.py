from typing import Any, Union, Self, Callable, Optional
from pathlib import Path
from pathlike_typing import PathLike
from typeguard import check_type
from hrenpack.encapsulation import getattr_plus, getattr_strict
from hrenpack.no_default import no_default
from hrenpack.typings import GetterFunc, SetterFunc


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
    def __init__(self, attr_name: str, default=no_default):
        self.attr_name = attr_name
        self.default = default

    def __get__(self, instance, owner=None):
        try: return getattr_strict(getattr(instance, self.name), self.attr_name)
        except AttributeError as error:
            if self.default is no_default: raise error
            return self.default


class CachedProperty(BaseDescriptor):
    def __init__(self, method: Callable):
        self.method = method

    def __get__(self, instance, owner):
        if instance is None: return self
        if not self.is_cached(instance):
            self.set_cache(instance, self.method(instance))
        return self.get_cache(instance)

    @staticmethod
    def cached_flag_attr_name(name: str): return f'__{name}__cached'

    @staticmethod
    def cache_attr_name(name: str): return f'__{name}__cache'

    def is_cached(self, instance) -> bool:
        return getattr(instance, self.cached_flag_attr_name(self.name), False)

    def get_cache(self, instance):
        return getattr(instance, self.cache_attr_name(self.name))

    def set_cache(self, instance, value):
        setattr(instance, self.cache_attr_name(self.name), value)
        setattr(self, self.cached_flag_attr_name(self.name), True)


class UncacheProperty(BaseDescriptor):
    def __init__(self, *cached_properties: str,
                 fget: Optional[GetterFunc] = None,
                 fset: Optional[SetterFunc] = None,
                 setable: bool = True):
        self.cached_properties = cached_properties
        if fget is None and fset is not None: setable = False
        self.fget = fget
        self.fset = fset
        self.setable = setable

    def __get__(self, instance, owner):
        if instance is None: return self
        if self.fget is not None: return self.fget()
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not self.setable: raise AttributeError(f'Cannot set attribute \'{self.name}\'')
        for name in self.cached_properties:
            setattr(instance, CachedProperty.cached_flag_attr_name(name), False)
        if self.fset is not None: self.fset(value)
        instance.__dict__[self.name] = value

    def __call__(self, fget: GetterFunc):
        if self.fset is not None: self.setable = False
        self.fget = fget
        return self

    def setter(self, fset: SetterFunc):
        self.setable = True
        self.fset = fset
        return self

