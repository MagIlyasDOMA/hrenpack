"""
String manipulation utilities.

Provides functions for string operations including random string generation,
index editing, string validation, and more.

Утилиты для манипуляции строками.

Предоставляет функции для операций со строками, включая генерацию случайных строк,
редактирование по индексу, валидацию строк и другое.
"""

import string, re
from typing import Union
from random import randint, choice as randchoice

PYTHONNAME_LETTERS = string.ascii_lowercase + string.digits + '_'
tuplist = Union[tuple, list]


def antienter_str(string: str, space: bool = True) -> str:
    """
    Replace newlines with spaces.

    Заменяет символы новой строки на пробелы.

    Args:
        string (str): Input string / Входная строка
        space (bool): Use space as separator, default True / Использовать пробел как разделитель

    Returns:
        str: String without newlines / Строка без символов новой строки
    """
    separator = ' ' if space else ''
    return separator.join(string.split('\n'))


def antispace(string: str) -> str:
    """
    Remove all whitespace from string.

    Удаляет все пробельные символы из строки.

    Args:
        string (str): Input string / Входная строка

    Returns:
        str: String without whitespace / Строка без пробельных символов
    """
    return ''.join(string.split())


def string_add(*args: str) -> str:
    """
    Concatenate multiple strings.

    Объединяет несколько строк.

    Args:
        *args: Strings to concatenate / Строки для объединения

    Returns:
        str: Concatenated string / Объединенная строка
    """
    return ''.join(args)


def randstr(a: int, b: int) -> str:
    """
    Generate random integer as string in range [a, b].

    Генерирует случайное целое число в виде строки в диапазоне [a, b].

    Args:
        a (int): Minimum value / Минимальное значение
        b (int): Maximum value / Максимальное значение

    Returns:
        str: Random number as string / Случайное число в виде строки
    """
    return str(randint(a, b))


def prefix(base: str, prefix: str, is_suffix: bool = False) -> str:
    """
    Add prefix or suffix to string.

    Добавляет префикс или суффикс к строке.

    Args:
        base (str): Base string / Базовая строка
        prefix (str): Prefix or suffix to add / Префикс или суффикс для добавления
        is_suffix (bool): Add as suffix if True, default False / Добавить как суффикс

    Returns:
        str: String with prefix/suffix / Строка с префиксом/суффиксом
    """
    return base + prefix if is_suffix else prefix + base


def in_or(string: str, *args: str) -> bool:
    """
    Check if any of args is in string (OR condition).

    Проверяет, содержится ли любой из аргументов в строке (условие ИЛИ).

    Args:
        string (str): String to search / Строка для поиска
        *args: Substrings to look for / Подстроки для поиска

    Returns:
        bool: True if any substring found / True если найдена любая подстрока
    """
    for arg in args:
        if arg in string:
            return True
    return False


def in_and(string: str, *args: str) -> bool:
    """
    Check if all args are in string (AND condition).

    Проверяет, содержатся ли все аргументы в строке (условие И).

    Args:
        string (str): String to search / Строка для поиска
        *args: Substrings to look for / Подстроки для поиска

    Returns:
        bool: True if all substrings found / True если найдены все подстроки
    """
    for arg in args:
        if arg not in string:
            return False
    return True


def index_edit(string: str, index: int, letter: str) -> str:
    """
    Replace character at specific index.

    Заменяет символ по указанному индексу.

    Args:
        string (str): Input string / Входная строка
        index (int): Position to replace / Позиция для замены
        letter (str): New character (must be length 1) / Новый символ (должен быть длины 1)

    Returns:
        str: Modified string / Измененная строка

    Raises:
        ValueError: If letter is not a single character / Если letter не является одним символом
    """
    if len(letter) != 1:
        raise ValueError('Letter must be a single character')
    p1 = string[:index]
    p2 = string[index + 1:]
    return p1 + letter + p2


def string_reverse(string: str):
    """
    Reverse a string.

    Переворачивает строку.

    Args:
        string (str): Input string / Входная строка

    Returns:
        str: Reversed string / Перевернутая строка
    """
    output = list(string)
    output.reverse()
    return ''.join(output)


def index_edit_multi(string: str, values: dict[int, str]) -> str:
    """
    Replace multiple characters by index.

    Заменяет несколько символов по индексам.

    Args:
        string (str): Input string / Входная строка
        values (dict[int, str]): Dictionary mapping indices to new characters / Словарь соответствия индексов новым символам

    Returns:
        str: Modified string / Измененная строка
    """
    for key, value in values.items():
        string = index_edit(string, key, value)
    return string


def index_edit_join(string: str, indexes: tuplist, values: Union[tuplist, str]) -> str:
    """
    Replace multiple characters with paired lists.

    Заменяет несколько символов с использованием парных списков.

    Args:
        string (str): Input string / Входная строка
        indexes (tuplist): List/tuple of indices / Список/кортеж индексов
        values (Union[tuplist, str]): List/tuple of replacement characters / Список/кортеж символов для замены

    Returns:
        str: Modified string / Измененная строка

    Raises:
        ValueError: If lengths don't match or empty / Если длины не совпадают или пустые
    """
    if len(indexes) != len(values):
        raise ValueError('Length of indexes must be equal to length of values')
    elif len(indexes) == 0 or len(values) == 0:
        raise ValueError('Empty indexes or values')
    else:
        for i in range(len(indexes)):
            if type(indexes[i]) is not int:
                raise ValueError('Indexes must be integers')
            if type(values[i]) is not str:
                raise ValueError('Values must be strings')
            string = index_edit(string, indexes[i], values[i])
        return string


def generate_rand_string(length: int = 25):
    """
    Generate random string of letters and digits.

    Генерирует случайную строку из букв и цифр.

    Args:
        length (int): String length, default 25 / Длина строки

    Returns:
        str: Random string / Случайная строка
    """
    return ''.join(randchoice(string.ascii_letters + string.digits) for _ in range(length))


def remove_extra_spaces(text):
    """
    Replace multiple spaces with single space.

    Заменяет несколько пробелов на один.

    Args:
        text (str): Input text / Входной текст

    Returns:
        str: Text with normalized spaces / Текст с нормализованными пробелами
    """
    return re.sub(r'\s+', ' ', text).strip()


def words_to_letters(*words: str) -> list:
    """
    Convert words to list of individual letters.

    Преобразует слова в список отдельных букв.

    Args:
        *words: Words to convert / Слова для преобразования

    Returns:
        list: List of letters / Список букв
    """
    return list(''.join(words))


def only_this_letters(text: str, *letters: str) -> bool:
    """
    Check if text contains only allowed letters.

    Проверяет, содержит ли текст только разрешенные буквы.

    Args:
        text (str): Text to check / Текст для проверки
        *letters: Allowed letters / Разрешенные буквы

    Returns:
        bool: True if only allowed letters / True если только разрешенные буквы
    """
    letters = words_to_letters(*letters)
    for letter in text:
        if letter not in letters:
            return False
    return True


def only_pythonname(text: str) -> bool:
    """
    Check if text is a valid Python identifier.

    Проверяет, является ли текст допустимым идентификатором Python.

    Args:
        text (str): Text to check / Текст для проверки

    Returns:
        bool: True if valid Python identifier / True если допустимый идентификатор Python
    """
    return only_this_letters(text, PYTHONNAME_LETTERS)


def strip_quotes(text: str) -> str:
    """
    Remove surrounding quotes from string.

    Удаляет окружающие кавычки из строки.

    Args:
        text (str): Text to process / Текст для обработки

    Returns:
        str: Text without surrounding quotes / Текст без окружающих кавычек
    """
    if len(text) < 2:
        return text
    elif text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    elif text[0] == "'" and text[-1] == "'":
        return text[1:-1]
    return text
