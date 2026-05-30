"""
MIME type detection for files.

Provides multiple methods to detect MIME types using different backends.

Определение MIME типов для файлов.

Предоставляет несколько методов определения MIME типов с использованием разных бэкендов.
"""

import mimetypes
from pathlike_typing import PathLike
from .cmd import get_extension
from .constants import MIME_TYPES, COMPOUND_EXTENSIONS


def get_mime_type(path: str):
    """
    Get MIME type using mimetypes module.

    Получает MIME тип с использованием модуля mimetypes.

    Args:
        path (str): File path / Путь к файлу

    Returns:
        str: MIME type, default 'application/octet-stream' / MIME тип
    """
    return mimetypes.guess_type(path)[0] or 'application/octet-stream'


def get_mime_type_extension(path: PathLike):
    """
    Get MIME type using custom extension mapping.

    Получает MIME тип с использованием пользовательского отображения расширений.

    Args:
        path (PathLike): File path / Путь к файлу

    Returns:
        str: MIME type / MIME тип
    """
    path = str(path)
    for ext, mime in COMPOUND_EXTENSIONS.items():
        if path.endswith(ext):
            return mime
    return MIME_TYPES.get(get_extension(path), 'application/octet-stream')


def get_mime_type_filetype(path: str):
    """
    Get MIME type using filetype module.

    Получает MIME тип с использованием модуля filetype.

    Args:
        path (str): File path / Путь к файлу

    Returns:
        str: MIME type, default 'application/octet-stream' / MIME тип
    """
    from filetype import guess
    kind = guess(path)
    if kind is None:
        return 'application/octet-stream'
    return kind.mime


def get_mime_type_magic(path: str):
    """
    Get MIME type using puremagic module.

    Получает MIME тип с использованием модуля puremagic.

    Args:
        path (str): File path / Путь к файлу

    Returns:
        str: MIME type / MIME тип
    """
    from puremagic import from_file
    return from_file(path, True)
