"""
Exception handling utilities.

Provides function to convert exceptions to string and custom warning class.

Утилиты для обработки исключений.

Предоставляет функцию преобразования исключений в строку и пользовательский класс предупреждения.
"""

def convert_exception_to_str(exception: Exception):
    """
    Convert exception to string with class name and message.

    Преобразует исключение в строку с именем класса и сообщением.

    Args:
        exception (Exception): Exception object / Объект исключения

    Returns:
        str: Formatted exception string / Отформатированная строка исключения
    """
    return f'{exception.__class__.__name__}: {str(exception)}'


class ExtraArgumentsWarning(UserWarning):
    """Warning raised when extra arguments are provided but ignored."""
    pass
