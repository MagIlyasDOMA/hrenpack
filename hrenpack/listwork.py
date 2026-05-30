"""
List and dictionary manipulation utilities.

Provides functions for working with lists, dictionaries, and nested data structures.

Утилиты для манипуляции списками и словарями.

Предоставляет функции для работы со списками, словарями и вложенными структурами данных.
"""

import re
from typing import Union, Literal, Optional, Iterable, Sequence, MutableMapping, Mapping

tdl = Union[tuple, dict, list]


def antizero(wnull, /):
    """
    Add leading zero to numbers less than 10.

    Добавляет ведущий ноль к числам меньше 10.

    Args:
        wnull: Number to format / Число для форматирования

    Returns:
        str: Number with leading zero if needed / Число с ведущим нулем при необходимости
    """
    if wnull < 10:
        output = '0' + str(wnull)
    else:
        output = str(wnull)
    return output


def intlist(input: list) -> list:
    """
    Convert all items in a list to integers.

    Преобразует все элементы списка в целые числа.

    Args:
        input (list): List of convertible items / Список преобразуемых элементов

    Returns:
        list: List of integers / Список целых чисел
    """
    return list(map(int, input))


def floatlist(input: list) -> list:
    """
    Convert all items in a list to floats.

    Преобразует все элементы списка в числа с плавающей точкой.

    Args:
        input (list): List of convertible items / Список преобразуемых элементов

    Returns:
        list: List of floats / Список чисел с плавающей точкой
    """
    return list(map(float, input))


def list_add(input: list, index: int, data) -> list:
    """
    Insert data at specific index, shifting elements to the right.

    Вставляет данные по указанному индексу, сдвигая элементы вправо.

    Args:
        input (list): Original list / Исходный список
        index (int): Position to insert / Позиция для вставки
        data: Data to insert / Данные для вставки

    Returns:
        list: New list with inserted data / Новый список с вставленными данными
    """
    forloop = len(input) + 1
    output = list()
    for i in range(forloop):
        if i < index:
            output.append(input[i])
        elif i == index:
            output.append(data)
        elif i > index:
            m = i - 1
            output.append(input[m])
    return output


def merging_dictionaries(*dicts: dict, **kwargs) -> dict:
    """
    Merge multiple dictionaries with later ones overriding earlier.

    Объединяет несколько словарей, более поздние переопределяют ранние.

    Args:
        *dicts: Dictionaries to merge / Словари для объединения
        **kwargs: Additional key-value pairs / Дополнительные пары ключ-значение

    Returns:
        dict: Merged dictionary / Объединенный словарь
    """
    return {**(dct for dct in dicts), **kwargs}


def split_quotes(text: str) -> list:
    """
    Split text while preserving quoted substrings as single tokens.

    Разделяет текст, сохраняя подстроки в кавычках как единые токены.

    Args:
        text (str): Text to split / Текст для разделения

    Returns:
        list: List of tokens / Список токенов
    """
    pattern = r"""
            (?:
                "(?:[^"\\]|\\.)*"
                |
                '(?:[^'\\]|\\.)*'
                |
                \S+              
            )
        """
    return re.findall(pattern, text, re.VERBOSE)


def del_keys(input: dict, *keys) -> None:
    """
    Delete multiple keys from a dictionary in-place.

    Удаляет несколько ключей из словаря in-place.

    Args:
        input (dict): Dictionary to modify / Словарь для изменения
        *keys: Keys to delete / Ключи для удаления
    """
    for key in keys:
        del input[key]


def dict_index(input: dict, value):
    """
    Find key by value in dictionary.

    Находит ключ по значению в словаре.

    Args:
        input (dict): Dictionary to search / Словарь для поиска
        value: Value to find / Значение для поиска

    Returns:
        Key associated with the value / Ключ, связанный со значением

    Raises:
        ValueError: If value not found / Если значение не найдено
    """
    for k, v in input.items():
        if v == value:
            return k
    else:
        raise ValueError(f"Dictionary {input} does not contain value {value}")


def strlist(input: list):
    """
    Convert all items in a list to strings.

    Преобразует все элементы списка в строки.

    Args:
        input (list): List of items / Список элементов

    Returns:
        list: List of strings / Список строк
    """
    input = list(input)
    for i in range(len(input)):
        input[i] = str(input[i])
    return input


def keys_dict_equals(*dicts: dict) -> bool:
    """
    Check if all dictionaries have the same keys.

    Проверяет, имеют ли все словари одинаковые ключи.

    Args:
        *dicts: Dictionaries to compare / Словари для сравнения

    Returns:
        bool: True if all have same keys / True если все имеют одинаковые ключи
    """
    dicts = list(dicts)
    first = tuple(dicts.pop(0).keys())
    for d in dicts:
        if first != tuple(d.keys()):
            return False
    return True


def del_none(lst: list) -> list:
    """
    Remove all None values from a list.

    Удаляет все значения None из списка.

    Args:
        lst (list): List to clean / Список для очистки

    Returns:
        list: Cleaned list / Очищенный список
    """
    while None in lst:
        lst.remove(None)
    return lst


def del_none_from_dict(*dicts, **kwargs) -> dict:
    """
    Remove all None values from merged dictionaries.

    Удаляет все значения None из объединенных словарей.

    Args:
        *dicts: Dictionaries to merge and clean / Словари для объединения и очистки
        **kwargs: Additional key-value pairs / Дополнительные пары ключ-значение

    Returns:
        dict: Dictionary without None values / Словарь без значений None
    """
    kwargs = merging_dictionaries(*dicts, kwargs)
    output = kwargs.copy()
    for key, value in kwargs.items():
        if value is None:
            output.pop(key)
    return output


def get_from_dict(input: dict, *keys, only_values: bool = False, default=None, pop_mode: bool = False):
    """
    Get multiple values from dictionary with optional pop.

    Получает несколько значений из словаря с опциональным удалением.

    Args:
        input (dict): Source dictionary / Исходный словарь
        *keys: Keys to get / Ключи для получения
        only_values (bool): Return only values, default False / Возвращать только значения
        default: Default value for missing keys / Значение по умолчанию
        pop_mode (bool): Remove keys from input, default False / Удалить ключи из входного словаря

    Returns:
        Union[dict, list]: Dictionary or list of values / Словарь или список значений
    """
    output = dict()
    for key in keys:
        value = input.pop(key, default)
        output[key] = value
        if not pop_mode:
            input[key] = value
    if only_values:
        return list(output.values())
    return output


def replace_fragment_from_args(old_frag: str, new_frag: str, *args: str, is_tuple: bool = False) -> list:
    """
    Replace substring in multiple strings.

    Заменяет подстроку в нескольких строках.

    Args:
        old_frag (str): Substring to replace / Подстрока для замены
        new_frag (str): Replacement substring / Подстрока-замена
        *args: Strings to process / Строки для обработки
        is_tuple (bool): Return tuple instead of list, default False / Вернуть кортеж вместо списка

    Returns:
        Union[list, tuple]: Processed strings / Обработанные строки
    """
    result = [arg.replace(old_frag, new_frag) for arg in args]
    return tuple(result) if is_tuple else result


class dict_enumerate:
    """
    Enumerate over dictionary items with index.

    Перебирает элементы словаря с индексом.

    Args:
        items (dict): Dictionary to enumerate / Словарь для перебора
    """

    def __init__(self, items: dict):
        self.items = items.items() if isinstance(items, dict) else items

    def __iter__(self):
        for i, kv in enumerate(self.items):
            yield i, *kv


def selective_slice(input, *keys, only_values: bool = False) -> tdl:
    """
    Extract specific keys from a dictionary.

    Извлекает определенные ключи из словаря.

    Args:
        input: Dictionary or mapping / Словарь или отображение
        *keys: Keys to extract / Ключи для извлечения
        only_values (bool): Return only values, default False / Возвращать только значения

    Returns:
        Union[dict, list]: Dictionary or list of values / Словарь или список значений

    Raises:
        KeyError: If any key is missing / Если какой-либо ключ отсутствует
    """
    output = dict()
    for key in keys:
        output[key] = input[key]
    if only_values:
        return list(output.values())
    return output


def dict_get(dct: dict, key, default=None):
    """
    Get value with special handling for False values.

    Получает значение с особой обработкой значений False.

    Args:
        dct (dict): Source dictionary / Исходный словарь
        key: Key to look up / Ключ для поиска
        default: Default value if key missing / Значение по умолчанию

    Returns:
        default if value is None or False? / default если значение None или False
    """
    output = dct.get(key)
    if output and output is not False:
        return default
    return output


def mislist(input: list, *args) -> list:
    """
    Return arguments that are NOT in the input list.

    Возвращает аргументы, которых НЕТ во входном списке.

    Args:
        input (list): Reference list / Список для проверки
        *args: Values to check / Значения для проверки

    Returns:
        list: Values not in input / Значения, отсутствующие в списке
    """
    return [arg for arg in args if arg not in input]


def dict_slice(input: dict, *keys, only_values: bool = False, all_required: bool = False):
    """
    Extract existing keys from dictionary, optionally requiring all.

    Извлекает существующие ключи из словаря, опционально требуя все.

    Args:
        input (dict): Source dictionary / Исходный словарь
        *keys: Keys to extract / Ключи для извлечения
        only_values (bool): Return only values, default False / Возвращать только значения
        all_required (bool): Raise error if any key missing, default False / Выбросить ошибку при отсутствии ключа

    Returns:
        Union[dict, list]: Dictionary or list of values / Словарь или список значений

    Raises:
        KeyError: If all_required is True and a key is missing / Если all_required=True и ключ отсутствует
    """
    output = dict()
    for key in keys:
        if key in input:
            output[key] = input[key]
        elif all_required:
            raise KeyError(key)
    return list(output.values()) if only_values else output


def two_tuples_to_dict(keys: Iterable, values: Iterable) -> dict:
    """
    Create dictionary from two iterables (keys and values).

    Создает словарь из двух итерируемых объектов (ключи и значения).

    Args:
        keys (Iterable): Keys for dictionary / Ключи для словаря
        values (Iterable): Values for dictionary / Значения для словаря

    Returns:
        dict: Resulting dictionary / Результирующий словарь
    """
    return dict(zip(keys, values))


def reverse_dict(input: dict) -> dict:
    """
    Reverse dictionary (swap keys and values).

    Переворачивает словарь (меняет местами ключи и значения).

    Args:
        input (dict): Dictionary to reverse / Словарь для переворота

    Returns:
        dict: Reversed dictionary / Перевернутый словарь

    Raises:
        ValueError: If values are not hashable / Если значения не хэшируемые
    """
    return dict(two_tuples_to_dict(input.values(), input.keys()))


def getitem_plus(input: Mapping, tree: Sequence[str], default=None, *, catch_errors: bool = True):
    """
    Access nested dictionary items using dot notation.

    Доступ к вложенным элементам словаря с использованием точечной нотации.

    Args:
        input (Mapping): Dictionary to access / Словарь для доступа
        tree (Sequence[str]): Path as list or dot-separated string / Путь как список или строка с точками
        default: Default value if path fails / Значение по умолчанию
        catch_errors (bool): Return default on error instead of raising, default True / Возвращать default при ошибке

    Returns:
        Value at path / Значение по пути
    """
    from hrenpack.encapsulation import getattr_plus
    return getattr_plus(input, tree, default, dict_mode=True, catch_errors=catch_errors)


def setitem_plus(input: MutableMapping, tree: Sequence[str], value, *, strict: bool = False):
    """
    Set value at nested dictionary path, creating intermediate dictionaries if needed.

    Устанавливает значение по вложенному пути в словаре, создавая промежуточные словари при необходимости.

    Args:
        input (MutableMapping): Dictionary to modify / Словарь для изменения
        tree (Sequence[str]): Path as list or dot-separated string / Путь как список или строка с точками
        value: Value to set / Значение для установки
        strict (bool): Raise error on missing intermediate keys, default False / Выбросить ошибку при отсутствии ключей

    Raises:
        TypeError: If intermediate object does not support item assignment / Если промежуточный объект не поддерживает присвоение
        KeyError: If strict=True and intermediate key missing / Если strict=True и промежуточный ключ отсутствует
    """
    if isinstance(tree, str):
        tree = tree.split('.')
    last_key = tree.pop()
    obj = input
    for level, key in enumerate(tree):
        if not hasattr(obj, '__setitem__'):
            raise TypeError(f"Object at level {level} is not a MutableMapping")
        elif key not in obj:
            if strict:
                raise KeyError(f"'{key}' at level {level} does not exist")
            obj[key] = dict()
        obj = obj[key]
    else:
        obj[last_key] = value
