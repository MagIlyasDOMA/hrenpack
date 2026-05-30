"""
Mixin classes for extending functionality of other classes.

Provides mixins for slots access, logging, and other common patterns.

Классы-примеси для расширения функциональности других классов.

Предоставляет примеси для доступа к слотсам, логирования и других общих паттернов.
"""


class SlotsReadMixin:
    """
    Mixin that adds read-only dictionary-style access to __slots__.

    Примесь, добавляющая доступ только для чтения в стиле словаря к __slots__.

    Raises:
        KeyError: If attribute not in __slots__ / Если атрибут не в __slots__
    """

    def __getitem__(self, item):
        """
        Get slot value using dictionary-style indexing.

        Получает значение слота через индексацию как в словаре.

        Args:
            item: Attribute name / Имя атрибута

        Returns:
            Value of the slot / Значение слота
        """
        if item in self.__slots__:
            return getattr(self, item)
        raise KeyError(item)


class SlotsMixin(SlotsReadMixin):
    """
    Mixin that adds read/write dictionary-style access to __slots__.

    Примесь, добавляющая доступ для чтения/записи в стиле словаря к __slots__.
    """

    def __setitem__(self, key, value):
        """
        Set slot value using dictionary-style indexing.

        Устанавливает значение слота через индексацию как в словаре.

        Args:
            key: Attribute name / Имя атрибута
            value: Value to set / Значение для установки
        """
        setattr(self, key, value)


class LogMixin:
    """
    Mixin that adds conditional logging based on log_mode attribute.

    Примесь, добавляющая условное логирование на основе атрибута log_mode.
    """

    def log(self, *values, sep: str = ' ', end: str = '\n', file=None, flush: bool = False):
        """
        Print values if log_mode is True.

        Печатает значения, если log_mode равен True.

        Args:
            *values: Values to print / Значения для печати
            sep (str): Separator between values / Разделитель между значениями
            end (str): End character / Конечный символ
            file: File to write to / Файл для записи
            flush (bool): Flush output buffer / Сбросить буфер вывода
        """
        if self.log_mode:
            print(*values, sep=sep, end=end, file=file, flush=flush)


class LogPlusMixin(LogMixin):
    """
    Extended LogMixin with log_mode attribute defaulting to False.

    Расширенная LogMixin с атрибутом log_mode по умолчанию False.
    """
    log_mode: bool = False
