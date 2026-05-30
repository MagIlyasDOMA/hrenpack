"""
Keyword arguments utilities.

Provides functions for working with kwargs dictionaries.

Утилиты для работы с ключевыми аргументами.

Предоставляет функции для работы со словарями kwargs.
"""


def kwarg_function(kwargs: dict, key: str, true, false):
    """
    Execute different functions based on whether a key exists in kwargs.

    Выполняет разные функции в зависимости от наличия ключа в kwargs.

    Args:
        kwargs (dict): Keyword arguments dictionary / Словарь ключевых аргументов
        key (str): Key to check / Ключ для проверки
        true: Function to call if key exists / Функция при наличии ключа
        false: Function to call if key does not exist / Функция при отсутствии ключа
    """
    if key in kwargs:
        true()
    else:
        false()


def get_kwarg(kwargs: dict, key: str, default=None, raise_error: bool = True, delete: bool = False):
    """
    Get a value from kwargs with optional error raising and deletion.

    Получает значение из kwargs с опциональным выбрасыванием ошибки и удалением.

    Args:
        kwargs (dict): Keyword arguments dictionary / Словарь ключевых аргументов
        key (str): Key to get / Ключ для получения
        default: Default value if key missing and raise_error is False / Значение по умолчанию
        raise_error (bool): Raise KeyError if key missing, default True / Выбросить KeyError при отсутствии ключа
        delete (bool): Delete key from kwargs after getting, default False / Удалить ключ из kwargs после получения

    Returns:
        Value associated with key / Значение, связанное с ключом

    Raises:
        KeyError: If key not found and raise_error is True / Если ключ не найден и raise_error=True
    """
    if default:
        raise_error = False
    if raise_error and key not in kwargs:
        raise KeyError(key)
    output = kwargs.get(key, default)
    if delete and key in kwargs:
        del kwargs[key]
    return output


def exclude_nones(**kwargs) -> dict:
    """
    Filter out None values from kwargs.

    Фильтрует значения None из kwargs.

    Args:
        **kwargs: Keyword arguments to filter / Ключевые аргументы для фильтрации

    Returns:
        dict: Dictionary with None values removed / Словарь с удаленными значениями None
    """
    output = dict()
    for key, value in kwargs.items():
        if value is not None:
            output[key] = value
    return output
