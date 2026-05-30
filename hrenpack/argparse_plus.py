"""
Extended ArgumentParser with additional features.

Provides ArgumentParser class with auto-help on no arguments, version flag,
and quiet mode support.

Расширенный ArgumentParser с дополнительными возможностями.

Предоставляет класс ArgumentParser с автоматической справкой при отсутствии аргументов,
флагом версии и поддержкой тихого режима.
"""

import argparse, sys, functools
from argparse import Namespace
from .functionwork import empty_function
from .iterwork import multi_in


def no_args_is_help(method):
    """
    Decorator that shows help when no arguments are provided.

    Декоратор, показывающий справку, когда аргументы не предоставлены.

    Args:
        method: Method to decorate / Метод для декорирования

    Returns:
        callable: Wrapped method / Обернутый метод
    """

    @functools.wraps(method)
    def wrapper(self, args=None, namespace=None):
        if self._no_args_is_help:
            self.noargs_is_help()
        return getattr(super(type(self), self), method.__name__, empty_function)(args, namespace)

    return wrapper


class ArgumentParser(argparse.ArgumentParser):
    """
    Extended ArgumentParser with additional features.

    Расширенный ArgumentParser с дополнительными возможностями.

    Args:
        no_args_is_help (bool): Show help when no args provided, default False / Показать справку без аргументов
        version (str): Version string for --version flag / Строка версии для флага --version
        add_quiet (bool): Add --quiet flag, default False / Добавить флаг --quiet
        **kwargs: Additional arguments for argparse.ArgumentParser / Дополнительные аргументы
    """

    def __init__(self, **kwargs):
        self._no_args_is_help = kwargs.pop('no_args_is_help', False)
        self._version = kwargs.pop('version', None)
        self._add_quiet = kwargs.pop('add_quiet', False)
        super().__init__(**kwargs)
        if self._version is not None:
            self.add_argument('--version', '-v', action='version', version=self._version)
        if self._add_quiet:
            self.add_argument('--quiet', '-q', action='store_true')

    def noargs_is_help(self):
        """
        Show help and exit if no arguments provided.

        Показывает справку и выходит, если аргументы не предоставлены.
        """
        if len(sys.argv) <= 1:
            self.print_help()
            sys.exit(0)

    @no_args_is_help
    def parse_args(self, args=None, namespace=None) -> Namespace:
        """Parse arguments, show help if none provided."""
        pass

    @no_args_is_help
    def parse_known_args(self, args=None, namespace=None) -> tuple[Namespace, list[str]]:
        """Parse known arguments, show help if none provided."""
        pass

    @no_args_is_help
    def parse_intermixed_args(self, args=None, namespace=None) -> Namespace:
        """Parse intermixed arguments, show help if none provided."""
        pass

    @no_args_is_help
    def parse_known_intermixed_args(self, args=None, namespace=None) -> tuple[Namespace, list[str]]:
        """Parse known intermixed arguments, show help if none provided."""
        pass

    @property
    def logging(self):
        """
        Check if logging is enabled (not quiet).

        Проверяет, включено ли логирование (не тихий режим).

        Returns:
            bool: True if logging enabled / True если логирование включено
        """
        return not multi_in(sys.argv, '--quiet', '-q')

    def log(self, *values, sep: str = ' ', end: str = '\n'):
        """
        Print values if logging is enabled.

        Печатает значения, если логирование включено.

        Args:
            *values: Values to print / Значения для печати
            sep (str): Separator between values, default space / Разделитель между значениями
            end (str): End character, default newline / Конечный символ
        """
        if self.logging:
            print(*values, sep=sep, end=end)
