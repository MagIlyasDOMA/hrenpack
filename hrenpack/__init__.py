"""
Hrenpack - Utility package for Python development.

This package provides various utilities for file handling, string operations,
encodings, environment variables, and more.

hrenpack - Пакет утилит для разработки на Python.

Этот пакет предоставляет различные утилиты для работы с файлами, строками,
кодировками, переменными окружения и многое другое.
"""

from .functionwork import empty_function
from .strwork import randstr
from .typings import *


def credits():
    """
    Print package credits information.

    Печатает информацию о кредитах пакета.
    """
    print("Hrenpack")
    print("(c) MagIlyasDOMA, 2024-2026.")
    print("Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)")


__version__ = '3.1.3'


def sts(word):
    """
    Create a string of asterisks with the same length as input word.

    Создает строку из звездочек той же длины, что и входное слово.

    Args:
        word (str): Input word / Входное слово

    Returns:
        str: String of asterisks / Строка из звездочек
    """
    stars = '*' * len(word)
    return stars


def of_utf8(filename, mode='r'):
    """
    Open a file with UTF-8 encoding.

    Открывает файл с кодировкой UTF-8.

    Args:
        filename (str): Path to file / Путь к файлу
        mode (str): File opening mode, default 'r' / Режим открытия файла, по умолчанию 'r'

    Returns:
        file: File object / Файловый объект
    """
    file = open(filename, mode, encoding='utf-8')
    return file


def write_a(path, data):
    """
    Append data to a file with UTF-8 encoding.

    Добавляет данные в файл с кодировкой UTF-8.

    Args:
        path (str): Path to file / Путь к файлу
        data (any): Data to append / Данные для добавления
    """
    file = open(path, 'a', encoding='utf-8')
    file.write(f'{str(data)}\n')
    file.close()


def write(path, text):
    """
    Write data to a file with UTF-8 encoding (overwrites).

    Записывает данные в файл с кодировкой UTF-8 (перезаписывает).

    Args:
        path (str): Path to file / Путь к файлу
        text (any): Text to write / Текст для записи
    """
    file = open(path, 'w', encoding='utf-8')
    file.write(str(text))
    file.close()


def switch(variable, case: dict, default=empty_function):
    """
    Switch-case implementation using a dictionary.

    Реализация switch-case с использованием словаря.

    Args:
        variable: Value to compare / Значение для сравнения
        case (dict): Dictionary mapping values to functions / Словарь сопоставления значений функциям
        default (callable): Default function if no match, default empty_function / Функция по умолчанию, если нет совпадения
    """
    for key in case:
        func = case[key]
        if variable == key:
            func()
            break
    else:
        default()


def bincode_generator(length: int, is_int: bool = False):
    """
    Generate a random binary string of specified length.

    Генерирует случайную двоичную строку указанной длины.

    Args:
        length (int): Length of binary code / Длина двоичного кода
        is_int (bool): Return as integer if True, default False / Вернуть как целое число, если True

    Returns:
        Union[str, int]: Binary string or integer / Двоичная строка или целое число
    """
    bincode = ''
    for i in range(length):
        bincode = bincode + randstr(0, 1)
    return int(bincode) if is_int else bincode


def who_called_me():
    """
    Get the filename of the function that called this function.

    Получает имя файла функции, которая вызвала эту функцию.

    Returns:
        str: Path to the calling file / Путь к вызывающему файлу
    """
    import inspect
    current_frame = inspect.currentframe()
    calling_frame = current_frame.f_back
    return inspect.getfile(calling_frame)


def module_is_installed(module_name: str):
    """
    Check if a Python module is installed.

    Проверяет, установлен ли модуль Python.

    Args:
        module_name (str): Name of the module / Имя модуля

    Returns:
        bool: True if installed, False otherwise / True если установлен, иначе False
    """
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
