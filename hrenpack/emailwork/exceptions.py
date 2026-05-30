"""
Emailwork module exceptions.

Provides custom exceptions for email protocol operations.

Исключения модуля emailwork.

Предоставляет пользовательские исключения для операций с email протоколами.
"""

from hrenpack.exceptions import convert_exception_to_str


class ProtocolNotInitialized(Exception):
    """Raised when trying to use an uninitialized protocol."""
    pass


class FolderNotFound(Exception):
    """Raised when specified folder does not exist."""
    pass


class DownloadError(Exception):
    """
    Raised when email download fails.

    Вызывается при ошибке загрузки email.

    Args:
        exception: Original exception or error message / Исходное исключение или сообщение об ошибке
        *args: Additional arguments / Дополнительные аргументы
    """

    def __init__(self, exception, *args):
        if isinstance(exception, Exception):
            first_arg = convert_exception_to_str(exception)
        else:
            first_arg = exception
        super().__init__(first_arg, *args)
