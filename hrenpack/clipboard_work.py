"""
Clipboard operations for text and images.

Provides functions to copy/paste text and get images from clipboard.

Операции с буфером обмена для текста и изображений.

Предоставляет функции для копирования/вставки текста и получения изображений из буфера обмена.
"""

import clipboard


class ClipBoardError(Exception):
    """Exception raised for clipboard operations errors."""
    pass


def get_clipboard_image():
    """
    Get image from clipboard.

    Получает изображение из буфера обмена.

    Returns:
        PIL.Image: Image from clipboard / Изображение из буфера обмена

    Raises:
        ClipBoardError: If clipboard is empty or not an image / Если буфер обмена пуст или не является изображением
        ModuleNotFoundError: If PIL is not installed / Если PIL не установлен
    """
    try:
        from PIL import ImageGrab

        im = ImageGrab.grabclipboard()
        if im is not None:
            return im
        else:
            raise ClipBoardError("Clipboard is empty or not an image")
    except (ImportError, ModuleNotFoundError):
        raise ModuleNotFoundError("PIL is required for image operations")


def copy_text(text: str) -> None:
    """
    Copy text to clipboard.

    Копирует текст в буфер обмена.

    Args:
        text (str): Text to copy / Текст для копирования
    """
    clipboard.copy(text)


def insert_text() -> str:
    """
    Get text from clipboard.

    Получает текст из буфера обмена.

    Returns:
        str: Text from clipboard / Текст из буфера обмена
    """
    return clipboard.paste()


def clipboard_is_image() -> bool:
    """
    Check if clipboard contains an image.

    Проверяет, содержит ли буфер обмена изображение.

    Returns:
        bool: True if clipboard contains image, False otherwise / True если буфер обмена содержит изображение

    Raises:
        ModuleNotFoundError: If PIL is not installed / Если PIL не установлен
    """
    try:
        from PIL import ImageGrab
        im = ImageGrab.grabclipboard()
        return im is not None
    except (ImportError, ModuleNotFoundError):
        raise ModuleNotFoundError("PIL is required for image operations")


def clipboard_image_error() -> None:
    """
    Raise error if clipboard doesn't contain an image.

    Вызывает ошибку, если буфер обмена не содержит изображение.

    Raises:
        ClipBoardError: If clipboard is empty or not an image / Если буфер обмена пуст или не является изображением
    """
    if not clipboard_is_image():
        raise ClipBoardError("Clipboard is empty or not an image")
