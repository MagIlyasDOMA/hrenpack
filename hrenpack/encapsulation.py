"""
Encapsulation and attribute access utilities.

Provides functions for safe attribute access, method decoration,
and descriptor discovery.

Утилиты для инкапсуляции и доступа к атрибутам.

Предоставляет функции для безопасного доступа к атрибутам, декорирования методов
и поиска дескрипторов.
"""

import functools, inspect
from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from typing import Sequence
from typeguard import check_type as check_type_strict, TypeCheckError
from hrenpack.functionwork import empty_function
from hrenpack.listwork import get_from_dict


class EncapsulationError(Exception):
    """Exception raised for encapsulation-related errors."""
    pass


def count_inheritance_levels(cls):
    """
    Count number of inheritance levels (excluding object).

    Подсчитывает количество уровней наследования (исключая object).

    Args:
        cls: Class to analyze / Класс для анализа

    Returns:
        int: Number of inheritance levels / Количество уровней наследования
    """
    mro = cls.__mro__
    count = 0
    for c in mro:
        if c is object:
            count += 1
    return count - 2


def check_method_in_parent(cls, name, debug_mode: bool = False):
    """
    Check if a method exists in any parent class.

    Проверяет, существует ли метод в любом родительском классе.

    Args:
        cls: Class to check / Класс для проверки
        name (str): Method name / Имя метода
        debug_mode (bool): Print debug information, default False / Выводить отладочную информацию

    Returns:
        bool: True if method exists in parent / True если метод существует в родителе
    """
    bases = cls.__bases__
    if debug_mode:
        print(bases)
    for base in bases:
        if hasattr(base, name):
            if debug_mode:
                print(base.__name__)
            return True
    return False


def supermethod(method):
    """
    Decorator that calls parent method before the child method.

    Декоратор, вызывающий родительский метод перед дочерним.

    Args:
        method: Method to decorate / Метод для декорирования

    Returns:
        callable: Wrapped method / Обернутый метод
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        getattr(super(type(self), self), method.__name__, empty_function)(*args, **kwargs)
        return method(self, *args, **kwargs)

    return wrapper


def supermethod_post(method):
    """
    Decorator that calls parent method after the child method.

    Декоратор, вызывающий родительский метод после дочернего.

    Args:
        method: Method to decorate / Метод для декорирования

    Returns:
        callable: Wrapped method / Обернутый метод
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        output = method(self, *args, **kwargs)
        getattr(super(type(self), self), method.__name__, empty_function)(*args, **kwargs)
        return output

    return wrapper


def superonlymethod(method):
    """
    Decorator that calls only parent method (child method is ignored).

    Декоратор, вызывающий только родительский метод (дочерний игнорируется).

    Args:
        method: Method to decorate / Метод для декорирования

    Returns:
        callable: Wrapped method / Обернутый метод
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return getattr(super(type(self), self), method.__name__, empty_function)(*args, **kwargs)

    return wrapper


def addattr(instance, attr_name, value):
    """
    Add attribute only if it doesn't exist.

    Добавляет атрибут, только если он не существует.

    Args:
        instance: Object instance / Экземпляр объекта
        attr_name (str): Attribute name / Имя атрибута
        value: Value to set / Значение для установки
    """
    if not hasattr(instance, attr_name):
        setattr(instance, attr_name, value)


def update_attrs_from_dict(instance, **attrs):
    """
    Update multiple attributes from keyword arguments.

    Обновляет несколько атрибутов из ключевых аргументов.

    Args:
        instance: Object instance / Экземпляр объекта
        **attrs: Attribute-value pairs / Пары атрибут-значение
    """
    for attr_name, value in attrs.items():
        setattr(instance, attr_name, value)


def add_attrs_from_dict(instance, **attrs):
    """
    Add multiple attributes only if they don't exist.

    Добавляет несколько атрибутов, только если они не существуют.

    Args:
        instance: Object instance / Экземпляр объекта
        **attrs: Attribute-value pairs / Пары атрибут-значение
    """
    for attr_name, value in attrs.items():
        addattr(instance, attr_name, value)


def setattr_if_is_none(instance, attr_name, value):
    """
    Set attribute only if current value is None.

    Устанавливает атрибут, только если текущее значение None.

    Args:
        instance: Object instance / Экземпляр объекта
        attr_name (str): Attribute name / Имя атрибута
        value: Value to set / Значение для установки
    """
    if getattr(instance, attr_name, None) is None:
        addattr(instance, attr_name, value)


def set_attrs_if_is_none(instance, **attrs):
    """
    Set multiple attributes only if current values are None.

    Устанавливает несколько атрибутов, только если текущие значения None.

    Args:
        instance: Object instance / Экземпляр объекта
        **attrs: Attribute-value pairs / Пары атрибут-значение
    """
    for attr_name, value in attrs.items():
        setattr_if_is_none(instance, attr_name, value)


def getattrs(instance, *attr_names, only_values: bool = False, is_tuple: bool = False, default=None):
    """
    Get multiple attributes as dictionary or tuple.

    Получает несколько атрибутов в виде словаря или кортежа.

    Args:
        instance: Object instance / Экземпляр объекта
        *attr_names: Attribute names to get / Имена атрибутов для получения
        only_values (bool): Return only values, default False / Возвращать только значения
        is_tuple (bool): Return tuple instead of list, default False / Возвращать кортеж вместо списка
        default: Default value for missing attributes / Значение по умолчанию

    Returns:
        Union[dict, list, tuple]: Retrieved attributes / Полученные атрибуты
    """
    output = dict()
    for attr_name in attr_names:
        output[attr_name] = getattr(instance, attr_name, default)
    return get_from_dict(output, *output.keys(), is_tuple=is_tuple, only_values=only_values, default=default)


def getattr_strict(obj, name: str):
    """
    Strict attribute access that raises AttributeError with proper message.

    Строгий доступ к атрибуту с правильным сообщением об ошибке.

    Args:
        obj: Object to get attribute from / Объект для получения атрибута
        name (str): Attribute name / Имя атрибута

    Returns:
        Attribute value / Значение атрибута

    Raises:
        AttributeError: If attribute doesn't exist / Если атрибут не существует
    """
    if hasattr(obj, name):
        return getattr(obj, name)
    elif isinstance(obj, type):
        raise AttributeError(f"type object '{obj.__name__}' has no attribute '{name}'")
    raise AttributeError(f"{obj.__class__.__name__} object has no attribute '{name}'")


def getattr_plus(obj, tree: Sequence[str], default=None, *, dict_mode: bool = False, catch_errors: bool = True):
    """
    Access nested attributes using dot notation.

    Доступ к вложенным атрибутам с использованием точечной нотации.

    Args:
        obj: Starting object / Начальный объект
        tree (Sequence[str]): Path as list of keys or dot-separated string / Путь как список или строка с точками
        default: Default value if path fails / Значение по умолчанию
        dict_mode (bool): Use dictionary indexing instead of attributes, default False / Использовать индексацию словаря
        catch_errors (bool): Return default on error instead of raising, default True / Возвращать default при ошибке

    Returns:
        Value at path / Значение по пути
    """
    if isinstance(tree, str):
        tree = tree.split('.')
    if len(tree) == 0:
        return default
    elif len(tree) == 1:
        key = tree[0]
        if dict_mode:
            try:
                return obj[key]
            except KeyError as error:
                if not catch_errors:
                    raise error
        else:
            try:
                return getattr_strict(obj, key)
            except AttributeError as error:
                if not catch_errors:
                    raise error
    else:
        output = obj
        for i, level in enumerate(tree):
            if dict_mode:
                try:
                    output = output[level]
                except KeyError:
                    if not catch_errors:
                        raise KeyError(f'{level} in level {i}')
                    break
            else:
                try:
                    output = getattr_strict(output, level)
                except AttributeError:
                    if not catch_errors:
                        raise AttributeError(f'{level} in level {i}')
                    break
        else:
            return output
    return default


def check_type(value, typing):
    """
    Check if value matches type hint.

    Проверяет, соответствует ли значение подсказке типа.

    Args:
        value: Value to check / Значение для проверки
        typing: Type hint to check against / Подсказка типа для проверки

    Returns:
        bool: True if type matches / True если тип соответствует
    """
    try:
        check_type_strict(value, typing)
        return True
    except (TypeError, TypeCheckError):
        return False


def get_own_attributes(obj):
    """
    Get attributes defined in the object's own class (not inherited).

    Получает атрибуты, определенные в собственном классе объекта (не унаследованные).

    Args:
        obj: Object to analyze / Объект для анализа

    Returns:
        set: Own attribute names / Имена собственных атрибутов
    """
    all_attrs = set(dir(obj))
    parent_attrs = set()

    cls = obj.__class__
    for parent in cls.__bases__:
        if parent != object:
            parent_attrs.update(dir(parent))

    return all_attrs - parent_attrs


class DescriptorsFinder:
    """
    Helper class to find descriptors in a class.

    Вспомогательный класс для поиска дескрипторов в классе.

    Args:
        cls (type): Class to analyze / Класс для анализа
    """

    def __init__(self, cls: type):
        self.cls = cls

    def _get_attrs(self, attr_name: str) -> set:
        attrs = set()
        for name, attr in self.cls.__dict__.items():
            if hasattr(attr, attr_name):
                attrs.add(name)
        return attrs

    def getters(self) -> set:
        """Get names of descriptors with __get__ method."""
        return self._get_attrs('__get__')

    def setters(self) -> set:
        """Get names of descriptors with __set__ method."""
        return self._get_attrs('__set__')

    def deleters(self) -> set:
        """Get names of descriptors with __delete__ method."""
        return self._get_attrs('__delete__')
