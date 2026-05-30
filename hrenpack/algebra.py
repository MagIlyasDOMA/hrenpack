"""
Algebra utilities for working with progressions and mathematical functions.

Provides ArithmeticProgression, GeometricProgression classes and subfactorial function.

Утилиты алгебры для работы с прогрессиями и математическими функциями.

Предоставляет классы ArithmeticProgression, GeometricProgression и функцию subfactorial.
"""

from math import factorial
from .classes import range_plus


class ArithmeticProgression:
    """
    Arithmetic progression class with indexing support.

    Класс арифметической прогрессии с поддержкой индексации.

    Args:
        first (float): First term of progression / Первый член прогрессии
        difference (float): Common difference / Разность прогрессии
    """

    def __init__(self, first: float, difference: float):
        self.first = first
        self.difference = difference

    def __getitem__(self, n: int):
        """
        Get the n-th term of the progression.

        Получает n-й член прогрессии.

        Args:
            n (int): Term index (1-based) / Индекс члена (начиная с 1)

        Returns:
            float: The n-th term / n-й член прогрессии

        Raises:
            IndexError: If n <= 0 / Если n <= 0
        """
        if n <= 0:
            raise IndexError('n must be positive')
        if n == 1:
            return self.first
        return self.first + (self.difference * (n - 1))


class GeometricProgression:
    """
    Geometric progression class with indexing support.

    Класс геометрической прогрессии с поддержкой индексации.

    Args:
        first (float): First term of progression / Первый член прогрессии
        denominator (float): Common ratio / Знаменатель прогрессии

    Raises:
        ValueError: If first or denominator is zero / Если первый член или знаменатель равны нулю
    """

    def __init__(self, first: float, denominator: float):
        if first == 0:
            raise ValueError("First term cannot be zero")
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        self.first = first
        self.denominator = denominator

    def __getitem__(self, n: int):
        """
        Get the n-th term of the progression.

        Получает n-й член прогрессии.

        Args:
            n (int): Term index (1-based) / Индекс члена (начиная с 1)

        Returns:
            float: The n-th term / n-й член прогрессии

        Raises:
            IndexError: If n <= 0 / Если n <= 0
        """
        if n <= 0:
            raise IndexError('n must be positive')
        if n == 1:
            return self.first
        return self.first * (self.denominator ** (n - 1))


def subfactorial(n: int) -> int:
    """
    Calculate the subfactorial (number of derangements) of n.

    Вычисляет субфакториал (количество беспорядков) числа n.

    Args:
        n (int): Non-negative integer / Неотрицательное целое число

    Returns:
        int: Subfactorial of n / Субфакториал n

    Raises:
        ValueError: If n < 0 / Если n < 0
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    elif n == 0:
        return 1
    elif n == 1:
        return 0
    result = 0
    for i in range_plus(n):
        result += (-1 ** n) / factorial(i)
    return factorial(n) * result
