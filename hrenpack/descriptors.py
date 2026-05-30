"""
Custom descriptors for attribute management.

Provides Constant, ObjectConstant, TypedDescriptor, PathLikeDescriptor,
CachedProperty, and other descriptor classes.

Пользовательские дескрипторы для управления атрибутами.

Предоставляет классы дескрипторов Constant, ObjectConstant, TypedDescriptor,
PathLikeDescriptor, CachedProperty и другие.
"""

from typing import Any, Union, Self, Callable, Optional
from pathlib import Path
from pathlike_typing import PathLike
from pyundefined import undefined
from typeguard import check_type
from hrenpack.encapsulation import getattr_strict
from hrenpack.typings import GetterFunc, SetterFunc


class BaseDescriptor:
    """
    Base class for descriptors that sets the attribute name.

    Базовый класс для дескрипторов, устанавливающий имя атрибута.
    """

    def __set_name__(self, owner, name):
        self.name = name


class Constant:
    """
    Descriptor that returns a constant value.

    Дескриптор, возвращающий постоянное значение.

    Args:
        value: Constant value to return / Постоянное значение для возврата
    """

    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.value


class ObjectConstant(BaseDescriptor):
    """
    Descriptor that lazily creates an object using a factory function or type.

    Дескриптор, лениво создающий объект с помощью фабричной функции или типа.

    Args:
        func_or_type (Union[Callable, type]): Factory function or type / Фабричная функция или тип
        send_instance (bool): Pass instance as first argument, default False / Передать экземпляр первым аргументом
        *args: Positional arguments for factory / Позиционные аргументы для фабрики
        **kwargs: Keyword arguments for factory / Ключевые аргументы для фабрики
    """

    def __init__(self, func_or_type: Union[Callable, type], send_instance: bool = False, *args, **kwargs):
        self.func_or_type = func_or_type
        self.send_instance = send_instance
        self.args = args
        self.kwargs = kwargs

    def _create_object(self, instance):
        if self.send_instance:
            args = (instance, *self.args)
        else:
            args = self.args
        return self.func_or_type(*args, **self.kwargs)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self._create_object(instance)
        return instance.__dict__[self.name]


class TypedDescriptor(BaseDescriptor):
    """
    Descriptor with type checking and optional default value.

    Дескриптор с проверкой типа и опциональным значением по умолчанию.

    Args:
        typing (Any): Expected type or type hint / Ожидаемый тип или подсказка типа
        default (Any): Default value, default undefined / Значение по умолчанию

    Raises:
        AttributeError: If attribute doesn't exist and no default / Если атрибут не существует и нет значения по умолчанию
    """

    def __init__(self, typing: Any = Any, default: Any = undefined):
        self.typing = typing
        self.default = default

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        value = instance.__dict__.get(self.name, self.default)
        if value is undefined:
            raise AttributeError('Attribute \'{}\' does not exist'.format(self.name))
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = check_type(value, self.typing)


class PathLikeDescriptor(BaseDescriptor):
    """
    Descriptor for PathLike objects with existence checking.

    Дескриптор для PathLike объектов с проверкой существования.

    Args:
        missing_ok (bool): Allow non-existent paths, default False / Разрешить несуществующие пути

    Raises:
        FileNotFoundError: If path doesn't exist and missing_ok is False / Если путь не существует и missing_ok=False
        TypeError: If value is not PathLike / Если значение не PathLike
    """

    def __init__(self, missing_ok: bool = False):
        self.missing_ok = missing_ok

    def __get__(self, instance, owner=None) -> Union[Path, Self, None]:
        if instance is None:
            return self
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
    """
    Descriptor for boolean values with default False.

    Дескриптор для булевых значений со значением по умолчанию False.

    Args:
        default (bool): Default value, default False / Значение по умолчанию
    """

    def __init__(self, default: bool = False):
        super().__init__(bool, default)

    def __get__(self, instance, owner=None) -> bool:
        return super().__get__(instance, owner)

    def __set__(self, instance, value: bool):
        super().__set__(instance, value)


class SubAttribute(BaseDescriptor):
    """
    Descriptor that accesses a sub-attribute of another attribute.

    Дескриптор, обращающийся к под-атрибуту другого атрибута.

    Args:
        attr_name (str): Name of the sub-attribute to access / Имя под-атрибута
        default: Default value if sub-attribute doesn't exist / Значение по умолчанию
    """

    def __init__(self, attr_name: str, default=undefined):
        self.attr_name = attr_name
        self.default = default

    def __get__(self, instance, owner=None):
        try:
            return getattr_strict(getattr(instance, self.name), self.attr_name)
        except AttributeError as error:
            if self.default is undefined:
                raise error
            return self.default


class CachedProperty(BaseDescriptor):
    """
    Property that caches its value after first computation.

    Свойство, кэширующее свое значение после первого вычисления.

    Args:
        method (Callable): Method that computes the value / Метод, вычисляющий значение
    """

    def __init__(self, method: Callable):
        self.method = method

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not self.is_cached(instance):
            self.set_cache(instance, self.method(instance))
        return self.get_cache(instance)

    @staticmethod
    def cached_flag_attr_name(name: str):
        """Generate name for cached flag attribute."""
        return f'__{name}__cached'

    @staticmethod
    def cache_attr_name(name: str):
        """Generate name for cache attribute."""
        return f'__{name}__cache'

    def is_cached(self, instance) -> bool:
        """Check if value is cached."""
        return getattr(instance, self.cached_flag_attr_name(self.name), False)

    def get_cache(self, instance):
        """Get cached value."""
        return getattr(instance, self.cache_attr_name(self.name))

    def set_cache(self, instance, value):
        """Set cached value."""
        setattr(instance, self.cache_attr_name(self.name), value)
        setattr(self, self.cached_flag_attr_name(self.name), True)


class UncacheProperty(BaseDescriptor):
    """
    Property that invalidates cached properties when set.

    Свойство, аннулирующее кэшированные свойства при установке.

    Args:
        *cached_properties: Names of cached properties to invalidate / Имена кэшированных свойств
        fget (Optional[GetterFunc]): Getter function / Функция геттера
        fset (Optional[SetterFunc]): Setter function / Функция сеттера
        setable (bool): Whether property can be set, default True / Можно ли устанавливать свойство
    """

    def __init__(self, *cached_properties: str,
                 fget: Optional[GetterFunc] = None,
                 fset: Optional[SetterFunc] = None,
                 setable: bool = True):
        self.cached_properties = cached_properties
        if fget is None and fset is not None:
            setable = False
        self.fget = fget
        self.fset = fset
        self.setable = setable

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is not None:
            return self.fget()
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not self.setable:
            raise AttributeError(f'Cannot set attribute \'{self.name}\'')
        for name in self.cached_properties:
            setattr(instance, CachedProperty.cached_flag_attr_name(name), False)
        if self.fset is not None:
            self.fset(value)
        instance.__dict__[self.name] = value

    def __call__(self, fget: GetterFunc):
        """
        Allow use as a decorator for getter.

        Позволяет использовать как декоратор для геттера.
        """
        if self.fset is not None:
            self.setable = False
        self.fget = fget
        return self

    def setter(self, fset: SetterFunc):
        """
        Set the setter method.

        Устанавливает метод сеттера.
        """
        self.setable = True
        self.fset = fset
        return self
