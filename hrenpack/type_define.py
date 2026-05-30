"""
Type checking and conversion utilities.

Provides functions for checking and converting between types,
including boolean conversion from strings.

Утилиты для проверки и преобразования типов.

Предоставляет функции для проверки и преобразования между типами,
включая преобразование строк в булевы значения.
"""

from typing import Optional, Any


def is_int(data) -> bool:
    """
    Check if data can be converted to integer.

    Проверяет, можно ли преобразовать данные в целое число.

    Args:
        data: Data to check / Данные для проверки

    Returns:
        bool: True if convertible to int / True если можно преобразовать в int
    """
    try:
        int(data)
    except ValueError:
        return False
    else:
        return True


def is_float(data) -> bool:
    """
    Check if data can be converted to float.

    Проверяет, можно ли преобразовать данные в число с плавающей точкой.

    Args:
        data: Data to check / Данные для проверки

    Returns:
        bool: True if convertible to float / True если можно преобразовать в float
    """
    try:
        float(data)
    except ValueError:
        return False
    else:
        return True


def is_bool(data) -> bool:
    """
    Check if data can be converted to boolean.

    Проверяет, можно ли преобразовать данные в булево значение.

    Args:
        data: Data to check / Данные для проверки

    Returns:
        bool: True if convertible to bool / True если можно преобразовать в bool
    """
    try:
        bool(data)
    except ValueError:
        return False
    else:
        return True


def convert_to_boolean(input: Any) -> bool:
    """
    Convert various inputs to boolean.

    Преобразует различные входные данные в булево значение.

    Args:
        input (Any): Value to convert / Значение для преобразования

    Returns:
        bool: Boolean representation / Булево представление

    Raises:
        ValueError: If string value is not recognized / Если строковое значение не распознано
    """
    if isinstance(input, bool):
        return input
    elif isinstance(input, str):
        if input.lower() in ('true', 'yes', 'on', '1', 't', 'y'):
            return True
        elif input.lower() in ('false', 'no', 'off', '0', 'f', 'n'):
            return False
        else:
            raise ValueError('Invalid boolean value')
    else:
        return bool(input)


def is_boolean(input: Any) -> bool:
    """
    Check if input can be converted to boolean.

    Проверяет, можно ли преобразовать входные данные в булево значение.

    Args:
        input (Any): Value to check / Значение для проверки

    Returns:
        bool: True if convertible to boolean / True если можно преобразовать в булево значение
    """
    try:
        convert_to_boolean(input)
    except:
        return False
    else:
        return True


def isinstance_multi(obj, *types) -> bool:
    """
    Check if object is instance of any of multiple types.

    Проверяет, является ли объект экземпляром любого из нескольких типов.

    Args:
        obj: Object to check / Объект для проверки
        *types: Types to check against / Типы для проверки

    Returns:
        bool: True if instance of any type / True если экземпляр любого типа
    """
    return isinstance(obj, types)


def issubclass_multi(obj, *classes) -> bool:
    """
    Check if class is subclass of any of multiple classes.

    Проверяет, является ли класс подклассом любого из нескольких классов.

    Args:
        obj: Class to check / Класс для проверки
        *classes: Classes to check against / Классы для проверки

    Returns:
        bool: True if subclass of any class / True если подкласс любого класса
    """
    return issubclass(obj, classes)


def is_object(arg, filter_uneditable: bool = True) -> Optional[bool]:
    """
    Check if argument is a proper object (not primitive type).

    Проверяет, является ли аргумент полноценным объектом (не примитивным типом).

    Args:
        arg: Argument to check / Аргумент для проверки
        filter_uneditable (bool): Exclude immutable types, default True / Исключить неизменяемые типы

    Returns:
        Optional[bool]: True if object, False if not, None if filter_uneditable excludes it / True если объект
    """
    if isinstance(arg, type):
        return False
    elif filter_uneditable and isinstance_multi(arg, int, str, float, bool, tuple, frozenset, bytes):
        return False
    elif isinstance(arg, object):
        return True
    return False
