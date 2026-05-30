"""
Number and mathematical utilities.

Provides functions for working with numbers, including square root checking,
division with rounding, probability, temperature conversion, and more.

Утилиты для работы с числами и математикой.

Предоставляет функции для работы с числами, включая проверку квадратного корня,
деление с округлением, вероятности, преобразование температур и другое.
"""

import math
from typing import Union, Optional
from hrenpack.listwork import intlist
from random import randint


class HexagonalError(ValueError):
    """Exception raised for hexagonal number errors."""
    pass


def is_int(input: float, /) -> bool:
    return str(abs(input)).isdigit()


def is_square_int(integer: int):
    """
    Check if integer is a perfect square.

    Проверяет, является ли целое число полным квадратом.

    Args:
        integer (int): Number to check / Число для проверки

    Returns:
        bool: True if perfect square / True если полный квадрат
    """
    return is_int(math.sqrt(integer))


def division_with_rounding(dividend: float, divisor: float, round_in_any_case: bool = False,
                           round_according_to_the_laws_of_mathematics: bool = False):
    """
    Divide with various rounding options.

    Делит с различными вариантами округления.

    Args:
        dividend (float): Number being divided / Делимое
        divisor (float): Number to divide by / Делитель
        round_in_any_case (bool): Always round down to integer, default False / Всегда округлять вниз до целого
        round_according_to_the_laws_of_mathematics (bool): Use mathematical rounding, default False / Использовать математическое округление

    Returns:
        Union[int, float]: Quotient / Частное
    """
    quotient = dividend / divisor
    if round_in_any_case:
        output = int_float_separate(quotient, True, True)[0]
    elif round_according_to_the_laws_of_mathematics:
        output = round(quotient, 0)
    else:
        output = dividend // divisor
    return output


presence_of_remainder_on_division = lambda dividend, divisor: dividend % divisor == 0
"""
Check if division has no remainder.
Проверяет, есть ли остаток от деления.
"""


def true_chance(chance: float):
    """
    Return True with a given probability percentage.

    Возвращает True с заданной вероятностью в процентах.

    Args:
        chance (float): Probability percentage (0-100) / Вероятность в процентах

    Returns:
        bool: True with given probability / True с заданной вероятностью
    """
    b = int(1 / (chance / 100))
    rand = randint(1, b)
    return rand == b


def number_in(num: float, minimum: float, maximum: float, steel: bool = False) -> bool:
    """
    Check if number is within range.

    Проверяет, находится ли число в диапазоне.

    Args:
        num (float): Number to check / Число для проверки
        minimum (float): Lower bound / Нижняя граница
        maximum (float): Upper bound / Верхняя граница
        steel (bool): Use strict inequality, default False / Использовать строгое неравенство

    Returns:
        bool: True if within range / True если в диапазоне

    Raises:
        ValueError: If minimum >= maximum / Если minimum >= maximum
    """
    if minimum >= maximum:
        raise ValueError(f'Minimum must be less than maximum')
    else:
        return minimum < num < maximum if steel else minimum <= num <= maximum


def moreless(num: float, min: float, max: float, is_strict: bool = False) -> bool:
    """
    Alias for number_in function.

    Псевдоним для функции number_in.

    Args:
        num (float): Number to check / Число для проверки
        min (float): Lower bound / Нижняя граница
        max (float): Upper bound / Верхняя граница
        is_strict (bool): Use strict inequality, default False / Использовать строгое неравенство

    Returns:
        bool: True if within range / True если в диапазоне
    """
    if min > max:
        raise ValueError("min must be less than max")
    return min < num < max if is_strict else min <= num <= max


moreless_strict = lambda num, min, max: moreless(num, min, max, True)
"""
Check with strict inequalities.
Проверка со строгими неравенствами.
"""

moreless_not_strict = lambda num, min, max: moreless(num, min, max, False)
"""
Check with non-strict inequalities.
Проверка с нестрогими неравенствами.
"""


def pifs(number: Union[float, str]) -> str:
    """
    Add plus sign to positive numbers.

    Добавляет знак плюса к положительным числам.

    Args:
        number (Union[float, str]): Number to format / Число для форматирования

    Returns:
        str: Number with sign / Число со знаком
    """
    if type(number) is str:
        number = float(number)
    return str(number) if number <= 0 else f'+{number}'


def closest_number(number, *numbers, prefer_max: Optional[bool] = None):
    """
    Find closest number from a list.

    Находит ближайшее число из списка.

    Args:
        number: Target number / Целевое число
        *numbers: Numbers to search / Числа для поиска
        prefer_max (Optional[bool]): If multiple closest, prefer max (True), min (False), or first (None), default None / Если несколько ближайших, предпочесть максимум (True), минимум (False) или первый (None)

    Returns:
        Closest number / Ближайшее число
    """
    closest_distance = min(abs(x - number) for x in numbers)
    candidates = [x for x in numbers if abs(x - number) == closest_distance]
    if prefer_max is None:
        return candidates[0]
    elif prefer_max:
        return max(candidates)
    else:
        return min(candidates)


def to_fahrenheit(temp_celsius: float, round_: int = 0):
    """
    Convert Celsius to Fahrenheit.

    Преобразует градусы Цельсия в Фаренгейты.

    Args:
        temp_celsius (float): Temperature in Celsius / Температура в Цельсиях
        round_ (int): Number of decimal places, default 0 / Количество знаков после запятой

    Returns:
        float: Temperature in Fahrenheit / Температура в Фаренгейтах
    """
    return round((temp_celsius * 9 / 5) + 32, round_)


def to_celsius(temp_fahrenheit: float, round_: int = 0):
    """
    Convert Fahrenheit to Celsius.

    Преобразует градусы Фаренгейта в Цельсии.

    Args:
        temp_fahrenheit (float): Temperature in Fahrenheit / Температура в Фаренгейтах
        round_ (int): Number of decimal places, default 0 / Количество знаков после запятой

    Returns:
        float: Temperature in Celsius / Температура в Цельсиях
    """
    return round((temp_fahrenheit - 32) * 5 / 9, round_)


def zero_len(number: float, length: int) -> str:
    """
    Pad number with leading zeros to specified length.

    Дополняет число ведущими нулями до указанной длины.

    Args:
        number (float): Number to pad / Число для дополнения
        length (int): Desired total length / Желаемая общая длина

    Returns:
        str: Padded number as string / Дополненное число в виде строки
    """
    number = str(number)
    integer, fl = number.split('.')
    integer = '0' * (length - len(integer)) + integer
    return '.'.join([integer, fl])


def module(number: float):
    """
    Get absolute value (alternative to abs()).

    Получает абсолютное значение (альтернатива abs()).

    Args:
        number (float): Number to get absolute value of / Число для получения модуля

    Returns:
        float: Absolute value / Абсолютное значение
    """
    return number if number >= 0 else -number


def round_and_delete(number: int, digits: int):
    """
    Round number to specified digits and remove trailing zeros.

    Округляет число до указанного количества цифр и удаляет завершающие нули.

    Args:
        number (int): Number to round / Число для округления
        digits (int): Number of digits to round to / Количество цифр для округления

    Returns:
        int: Rounded number / Округленное число
    """
    d = int('1' + '0' * digits)
    number = round(number, -digits)
    return number // d


def randcolor():
    """
    Generate random hexadecimal color.

    Генерирует случайный шестнадцатеричный цвет.

    Returns:
        str: Random color code (e.g., '#a1b2c3') / Случайный код цвета
    """
    return f'#{randint(0, 16777215):x}'
