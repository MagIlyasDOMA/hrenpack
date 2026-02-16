import math, warnings
from typing import Union, Optional
from hrenpack.listwork import intlist
from random import randint


class HexagonalError(ValueError):
    pass


def int_float_separate(input: float, is_tuple: bool = False, is_int: bool = False):
    int_and_float = str(input).split('.')
    if is_int:
        int_and_float = intlist(int_and_float)
    if is_tuple:
        int_and_float = tuple(int_and_float)
    return int_and_float


def is_square_int(integer: int):
    sq = math.sqrt(integer)
    ls = int_float_separate(sq, True)
    return ls[1] == '0'


def division_with_rounding(dividend: float, divisor: float, round_in_any_case: bool = False, round_according_to_the_laws_of_mathematics: bool = False):
    quotient = dividend / divisor
    if round_in_any_case:
        output = int_float_separate(quotient, True, True)[0]
    elif round_according_to_the_laws_of_mathematics:
        output = round(quotient, 0)
    else:
        output = dividend // divisor
    return output


presence_of_remainder_on_division = lambda dividend, divisor: dividend % divisor == 0


# change - шанс
# Шанс указывается в процентах
def true_chance(chance: float):
    b = int(1 / (chance / 100))
    rand = randint(1, b)
    return rand == b


def number_in(num: float, minimum: float, maximum: float, steel: bool = False) -> bool:
    if minimum >= maximum:
        raise ValueError(f'Минимум должен быть меньше максимума')
    else:
        return minimum < num < maximum if steel else minimum <= num <= maximum


def hex_to_dec(hex_string: str) -> int:
    return int(hex_string, 16)


def dec_to_hex(dec: int) -> str:
    warnings.warn('This function will be removed in version 3.0.0', DeprecationWarning, 2)
    num = hex(dec)
    return num[2:]


def oct_to_dec(oct_int: int) -> int:
    return int(str(oct_int), 8)


def dec_to_oct(dec: int) -> int:
    num = oct(dec)
    return int(num[2:])


def moreless(num: float, min: float, max: float, is_strict: bool = False) -> bool:
    if min > max:
        raise ValueError("min должен быть меньше max")
    return min < num < max if is_strict else min <= num <= max


moreless_strict = lambda num, min, max: moreless(num, min, max, True)
moreless_not_strict = lambda num, min, max: moreless(num, min, max, False)


def pifs(number: Union[float, str]) -> str:
    if type(number) is str:
        number = float(number)
    return str(number) if number <= 0 else f'+{number}'


def closest_number(number, *numbers, prefer_max: Optional[bool] = None):
    closest_distance = min(abs(x - number) for x in numbers)
    candidates = [x for x in numbers if abs(x - number) == closest_distance]
    if prefer_max is None:
        return candidates[0]
    elif prefer_max:
        return max(candidates)
    else:
        return min(candidates)


def to_fahrenheit(temp_celsius: float, round_: int = 0):
    return round((temp_celsius * 9 / 5) + 32, round_)


def to_celsius(temp_fahrenheit: float, round_: int = 0):
    return round((temp_fahrenheit - 32) * 5 / 9, round_)


def zero_len(number: float, length: int) -> str:
    number = str(number)
    integer, fl = number.split('.')
    integer = '0' * (length - len(integer)) + integer
    return '.'.join([integer, fl])


def module(number: float):
    return number if number >= 0 else -number


def round_and_delete(number: int, digits: int):
    d = int('1' + '0' * digits)
    number = round(number, -digits)
    return number // d
