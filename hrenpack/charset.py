"""
Character encoding detection and conversion utilities.

Provides functions to detect file encodings, test encodings, and convert to UTF-8.

Утилиты для определения кодировок и преобразования.

Предоставляет функции для определения кодировок файлов, тестирования кодировок
и преобразования в UTF-8.
"""

import encodings, chardet
from typing import Union, Optional
from charset_normalizer import from_bytes
from hrenpack.listwork import replace_fragment_from_args

ALL_ENCODINGS = set(replace_fragment_from_args('_', '-', *set(encodings.aliases.aliases.values())))


def test_file_encoding(path: str, encoding: str, message: bool = False):
    """
    Test if a file can be read with specified encoding.

    Проверяет, можно ли прочитать файл с указанной кодировкой.

    Args:
        path (str): Path to file / Путь к файлу
        encoding (str): Encoding to test / Кодировка для проверки
        message (bool): Return message instead of boolean, default False / Вернуть сообщение вместо булева значения

    Returns:
        Union[bool, str, tuple]: Test result / Результат проверки
    """
    try:
        with open(path, encoding=encoding) as file:
            try:
                file.read()
            except Exception as err:
                if message:
                    return f"Error {err.__class__.__name__} with encoding", encoding
                return False
            else:
                if message:
                    return "Encoding", encoding, "is working correctly"
                return True
    except Exception as error:
        if message:
            return f"Error {error.__class__.__name__} opening file with encoding", encoding
        return False


def select_encoding(path: str) -> str:
    """
    Automatically select the correct encoding for a file.

    Автоматически подбирает правильную кодировку для файла.

    Args:
        path (str): Path to file / Путь к файлу

    Returns:
        str: Detected encoding / Определенная кодировка
    """
    for enc in ALL_ENCODINGS:
        if test_file_encoding(path, enc):
            return enc


def test_all_encodings(path: str):
    """
    Test all encodings on a file and print results.

    Проверяет все кодировки на файле и выводит результаты.

    Args:
        path (str): Path to file / Путь к файлу
    """
    for enc in ALL_ENCODINGS:
        print(test_file_encoding(path, enc, True))


def get_encoding(input: Union[str, bytes, bytearray]) -> str:
    """
    Detect encoding of input data.

    Определяет кодировку входных данных.

    Args:
        input (Union[str, bytes, bytearray]): Input data / Входные данные

    Returns:
        str: Detected encoding / Определенная кодировка
    """
    return from_bytes(input).best().encoding


def convert_to_utf_8(input: bytes, encoding: Optional[str] = None) -> bytes:
    """
    Convert input bytes to UTF-8 encoding.

    Преобразует входные байты в кодировку UTF-8.

    Args:
        input (bytes): Input bytes / Входные байты
        encoding (Optional[str]): Source encoding, auto-detected if None / Исходная кодировка

    Returns:
        bytes: UTF-8 encoded bytes / Байты в кодировке UTF-8
    """
    if encoding is None:
        encoding = get_encoding(input)
    return input.decode(encoding).encode('utf-8')


def detect_encoding(file_content):
    """
    Detect encoding using BOM markers and chardet.

    Определяет кодировку с использованием маркеров BOM и chardet.

    Args:
        file_content (bytes): File content as bytes / Содержимое файла в байтах

    Returns:
        str: Detected encoding / Определенная кодировка
    """
    # First check for explicit BOM markers
    if file_content.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-sig'
    elif file_content.startswith(b'\xff\xfe'):
        return 'utf-16'

    # Use chardet for complex cases
    result = chardet.detect(file_content)
    encoding = result['encoding'].lower()

    # Fix typical errors
    encoding_map = {
        'windows-1251': 'cp1251',
        'utf_8': 'utf-8',
        'ascii': 'utf-8'  # ASCII is a subset of UTF-8
    }
    return encoding_map.get(encoding, encoding)
