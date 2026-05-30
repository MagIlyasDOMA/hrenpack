"""
Iterable utilities for checking membership.

Provides multi_in function for checking multiple values in an iterable.

Утилиты для работы с итерируемыми объектами для проверки вхождения.

Предоставляет функцию multi_in для проверки нескольких значений в итерируемом объекте.
"""

from typing import Iterable, Literal


def multi_in(input: Iterable, *args, condition: Literal['or', 'and'] = 'or'):
    """
    Check if multiple values are in an iterable with logical condition.

    Проверяет, находятся ли несколько значений в итерируемом объекте с логическим условием.

    Args:
        input (Iterable): Iterable to check / Итерируемый объект для проверки
        *args: Values to check for presence / Значения для проверки наличия
        condition (Literal['or', 'and']): Logical condition, default 'or' / Логическое условие

    Returns:
        bool: Result of the condition / Результат условия

    Raises:
        ValueError: If no arguments provided / Если аргументы не предоставлены
    """
    if not args:
        raise ValueError('Must provide at least one argument')
    for arg in args:
        if arg not in input and condition == 'and':
            return False
        elif arg in input and condition == 'or':
            return True
    return condition == 'and'
