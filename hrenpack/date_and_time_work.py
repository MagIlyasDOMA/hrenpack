"""
Date and time manipulation utilities.

Provides HoursMinutesAndSeconds class and functions for datetime formatting,
timezone handling, and time calculations.

Утилиты для работы с датой и временем.

Предоставляет класс HoursMinutesAndSeconds и функции для форматирования datetime,
работы с часовыми поясами и вычислений времени.
"""

import time, datetime, pytz, zoneinfo
from datetime import datetime as dt, date as date_object
from dataclasses import dataclass
from typing import Union, Optional, Literal
from tzlocal import get_localzone
from hrenpack.listwork import intlist, strlist


class HoursMinutesAndSeconds:
    """
    Class for working with time durations (hours, minutes, seconds).

    Класс для работы с временными интервалами (часы, минуты, секунды).

    Args:
        hours (int): Number of hours / Количество часов
        minutes (int): Number of minutes / Количество минут
        seconds (int): Number of seconds / Количество секунд
    """

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.__time_format()

    def __str__(self):
        """
        Convert to string in HH:MM:SS format.

        Преобразует в строку формата ЧЧ:ММ:СС.

        Returns:
            str: Formatted time string / Отформатированная строка времени
        """
        h, m, s = self.hours, self.minutes, self.seconds
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        return '{}:{}:{}'.format(h, m, s)

    def __int__(self):
        """Convert to total seconds."""
        return self.to_seconds()

    def __bool__(self):
        """Check if time is non-zero."""
        return self.to_seconds() != 0

    def __add__(self, other):
        """
        Add another time value.

        Складывает с другим временным значением.

        Args:
            other: HoursMinutesAndSeconds, str, or int / Другой объект

        Returns:
            HoursMinutesAndSeconds: Result / Результат

        Raises:
            ValueError: If other type is not supported / Если тип не поддерживается
        """
        if type(other) is HoursMinutesAndSeconds:
            h = self.hours + other.hours
            m = self.minutes + other.minutes
            s = self.seconds + other.seconds
        elif type(other) is str:
            h, m, s = other.split(':')
            h = int(h) + self.hours
            m = int(m) + self.minutes
            s = int(s) + self.seconds
        elif type(other) is int:
            h, m, s = self.hours, self.minutes, self.seconds
            s += other
            h, m, s = time_format(h, m, s)
        else:
            raise ValueError('HoursMinutesAndSeconds can add with int, str or HoursMinutesAndSeconds')
        return HoursMinutesAndSeconds(h, m, s)

    def __sub__(self, other):
        """
        Subtract another time value.

        Вычитает другое временное значение.

        Args:
            other: HoursMinutesAndSeconds, str, or int / Другой объект

        Returns:
            HoursMinutesAndSeconds: Result / Результат

        Raises:
            ValueError: If other type is not supported / Если тип не поддерживается
        """
        if type(other) is HoursMinutesAndSeconds:
            h = self.hours - other.hours
            m = self.minutes - other.minutes
            s = self.seconds - other.seconds
        elif type(other) is str:
            h, m, s = other.split(':')
            h = int(h) - self.hours
            m = int(m) - self.minutes
            s = int(s) - self.seconds
        elif type(other) is int:
            h, m, s = self.hours, self.minutes, self.seconds
            s -= other
        else:
            raise ValueError('From HoursMinutesAndSeconds can subtract int, str or HoursMinutesAndSeconds')
        return HoursMinutesAndSeconds(h, m, s)

    def __mul__(self, other: int):
        """
        Multiply time by integer.

        Умножает время на целое число.

        Args:
            other (int): Multiplier / Множитель

        Returns:
            HoursMinutesAndSeconds: Result / Результат
        """
        h = self.hours * other
        m = self.minutes * other
        s = self.seconds * other
        return HoursMinutesAndSeconds(h, m, s)

    def __time_format(self):
        """Normalize time values (convert excess seconds/minutes)."""
        while self.seconds >= 60:
            self.seconds -= 60
            self.minutes += 1
        while self.minutes >= 60:
            self.minutes -= 60
            self.hours += 1

    @classmethod
    def from_seconds(cls, seconds: int):
        """
        Create HoursMinutesAndSeconds from total seconds.

        Создает HoursMinutesAndSeconds из общего количества секунд.

        Args:
            seconds (int): Total seconds / Общее количество секунд

        Returns:
            HoursMinutesAndSeconds: Time object / Объект времени
        """
        return cls(*time_format(0, 0, seconds))

    @classmethod
    def from_string(cls, string: str, separator: str = ':', ms: Optional[bool] = None):
        """
        Create HoursMinutesAndSeconds from string.

        Создает HoursMinutesAndSeconds из строки.

        Args:
            string (str): Time string / Строка времени
            separator (str): Separator character, default ':' / Символ-разделитель
            ms (Optional[bool]): Whether format is MM:SS (True) or HH:MM (False) / Формат ММ:СС или ЧЧ:ММ

        Returns:
            HoursMinutesAndSeconds: Time object / Объект времени

        Raises:
            ValueError: If incorrect number of parts / Если неверное количество частей
        """
        slist = string.split(separator)
        if slist.__len__() == 3:
            h, m, s = string.split(separator)
        elif slist.__len__() == 2:
            if ms is None:
                raise ValueError('If using 2 arguments, ms parameter must be boolean')
            elif ms:
                h = 0
                m, s = slist
            else:
                h, m = slist
                s = 0
        else:
            raise ValueError("Must have 2 or 3 arguments")
        return cls(int(h), int(m), int(s))

    def to_seconds(self) -> int:
        """
        Convert to total seconds.

        Преобразует в общее количество секунд.

        Returns:
            int: Total seconds / Общее количество секунд
        """
        return self.hours * 3600 + self.minutes * 60 + self.seconds


def time_format(hours: int, minutes: int, seconds: int, return_mode: Literal['string', 'tuple', 'class'] = 'tuple'):
    """
    Normalize time values and return in specified format.

    Нормализует временные значения и возвращает в указанном формате.

    Args:
        hours (int): Hours / Часы
        minutes (int): Minutes / Минуты
        seconds (int): Seconds / Секунды
        return_mode (Literal['string', 'tuple', 'class']): Output format / Формат вывода

    Returns:
        Union[str, tuple, HoursMinutesAndSeconds]: Normalized time / Нормализованное время
    """
    while seconds >= 60:
        seconds -= 60
        minutes += 1
    while minutes >= 60:
        minutes -= 60
        hours += 1
    output = {
        'string': '{}:{}:{}'.format(hours, minutes, seconds),
        'tuple': (hours, minutes, seconds),
        'class': HoursMinutesAndSeconds(hours, minutes, seconds)
    }
    return output[return_mode]


def datetime_format(input: int):
    """
    Format number with leading zero if less than 10.

    Форматирует число с ведущим нулем, если меньше 10.

    Args:
        input (int): Number to format / Число для форматирования

    Returns:
        str: Formatted number / Отформатированное число
    """
    return '0' + str(input) if input < 10 else str(input)


def date_and_time_data():
    """
    Get current date and time as structured data.

    Получает текущую дату и время в виде структурированных данных.

    Returns:
        Data: Object with date and time attributes / Объект с атрибутами date и time
    """

    @dataclass
    class Data:
        date: str
        time: str

    now = dt.now()
    date = f'{datetime_format(now.day)}.{datetime_format(now.month)}.{now.year}'
    time = f'{datetime_format(now.hour)}:{datetime_format(now.minute)}:{datetime_format(now.second)}'
    return Data(date, time)


def date(year: bool) -> str:
    """
    Get current date string.

    Получает строку текущей даты.

    Args:
        year (bool): Include year in output / Включить год в вывод

    Returns:
        str: Date string / Строка даты
    """
    now = dt.now()
    data = f'{now.day}.{now.month}'
    return data + f'.{now.year}' if year else data


def time_summ(*args: Union[str, HoursMinutesAndSeconds], return_hms: bool = False):
    """
    Sum multiple time values.

    Суммирует несколько временных значений.

    Args:
        *args: Time values to sum / Временные значения для суммирования
        return_hms (bool): Return HoursMinutesAndSeconds object if True / Вернуть объект HoursMinutesAndSeconds

    Returns:
        Union[str, HoursMinutesAndSeconds]: Summed time / Суммированное время
    """
    args = list(args)
    first = args[0]
    output = HoursMinutesAndSeconds.from_string(first) if type(first) is str else first
    args.pop(0)
    for arg in args:
        output += arg
    return output if return_hms else str(output)


def perf_counter(func):
    """
    Decorator that measures and prints function execution time.

    Декоратор, измеряющий и выводящий время выполнения функции.

    Args:
        func: Function to decorate / Функция для декорирования

    Returns:
        callable: Wrapped function / Обернутая функция
    """

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print(end - start)

    return wrapper


def unix_to_datetime(unix_timestamp: int) -> dt:
    """
    Convert Unix timestamp to datetime object.

    Преобразует Unix timestamp в объект datetime.

    Args:
        unix_timestamp (int): Unix timestamp / Unix timestamp

    Returns:
        datetime: Datetime object / Объект datetime
    """
    return dt.fromtimestamp(unix_timestamp)


def datetime_to_time(input: dt) -> datetime.time:
    """
    Extract time part from datetime.

    Извлекает временную часть из datetime.

    Args:
        input (datetime): Datetime object / Объект datetime

    Returns:
        datetime.time: Time object / Объект времени
    """
    return datetime.time(input.hour, input.minute, input.second)


def string_to_datetime(input: str, dt_separator: str = ' ', date_separator: str = '.', time_separator: str = ':',
                       date_reverse: bool = False) -> dt:
    """
    Convert string to datetime.

    Преобразует строку в datetime.

    Args:
        input (str): Date-time string / Строка даты-времени
        dt_separator (str): Separator between date and time, default space / Разделитель даты и времени
        date_separator (str): Date component separator, default '.' / Разделитель компонентов даты
        time_separator (str): Time component separator, default ':' / Разделитель компонентов времени
        date_reverse (bool): Reverse date order (e.g., YYYY.MM.DD), default False / Перевернуть порядок даты

    Returns:
        datetime: Datetime object / Объект datetime
    """
    date, time = input.split(dt_separator)
    date = intlist(date.split(date_separator))
    time = intlist(time.split(time_separator))
    if date_reverse:
        date = list(reversed(date))
    return dt(*date, *time)


def string_to_date(input: str, date_separator: str = '.', date_reverse: bool = False) -> dt:
    """
    Convert string to date (with time set to 00:00:00).

    Преобразует строку в дату (со временем 00:00:00).

    Args:
        input (str): Date string / Строка даты
        date_separator (str): Date component separator, default '.' / Разделитель компонентов даты
        date_reverse (bool): Reverse date order, default False / Перевернуть порядок даты

    Returns:
        datetime: Datetime object with time 00:00:00 / Объект datetime с временем 00:00:00
    """
    return string_to_datetime(input + ' 00:00:00', date_separator=date_separator, date_reverse=date_reverse)


def zero_form(input: Union[str, int]):
    """
    Format number with leading zero if less than 10.

    Форматирует число с ведущим нулем, если меньше 10.

    Args:
        input (Union[str, int]): Number to format / Число для форматирования

    Returns:
        str: Formatted number / Отформатированное число
    """
    if isinstance(input, str):
        input = int(input)
    return str(input) if input > 9 else '0' + str(input)


def zero_str(input: Union[str, dt]):
    """
    Format time string with leading zeros.

    Форматирует строку времени с ведущими нулями.

    Args:
        input (Union[str, datetime]): Time string or datetime object / Строка времени или datetime объект

    Returns:
        str: Formatted time string / Отформатированная строка времени

    Raises:
        ValueError: If format is invalid / Если формат неверный
    """
    if isinstance(input, str):
        output = input.split(':')
        if len(output) == 2:
            h, m = output
            return ':'.join([zero_form(h), zero_form(m)])
        elif len(output) == 3:
            h, m, s = output
            return ':'.join([zero_form(h), zero_form(m), zero_form(s)])
        else:
            raise ValueError("Invalid time format")
    else:
        h, m, s = input.hour, input.minute, input.second
        return ':'.join([zero_form(h), zero_form(m), zero_form(s)])


def datetime_to_str(input: dt, mode: Literal['date', 'time', 'datetime'] = 'datetime',
                    date_separator: str = '.', time_separator: str = ':', without_seconds: bool = False,
                    date_order: Literal['dmy', 'dym', 'mdy', 'myd', 'ydm', 'ymd'] = 'dmy') -> str:
    """
    Convert datetime to formatted string.

    Преобразует datetime в отформатированную строку.

    Args:
        input (datetime): Datetime object / Объект datetime
        mode (Literal): Output mode - 'date', 'time', or 'datetime' / Режим вывода
        date_separator (str): Separator for date components / Разделитель компонентов даты
        time_separator (str): Separator for time components / Разделитель компонентов времени
        without_seconds (bool): Exclude seconds from output, default False / Исключить секунды из вывода
        date_order (Literal): Order of date components / Порядок компонентов даты

    Returns:
        str: Formatted string / Отформатированная строка

    Raises:
        ValueError: If mode or date_order is invalid / Если режим или порядок даты неверны
    """
    match date_order:
        case 'dmy':
            dym_tup = [input.day, input.month, input.year]
        case 'dym':
            dym_tup = [input.day, input.year, input.month]
        case 'mdy':
            dym_tup = [input.month, input.day, input.year]
        case 'myd':
            dym_tup = [input.month, input.year, input.day]
        case 'ydm':
            dym_tup = [input.year, input.day, input.month]
        case 'ymd':
            dym_tup = [input.year, input.month, input.day]
        case _:
            raise ValueError("Invalid date_order value")

    for i in range(3):
        if dym_tup[i] < 10:
            dym_tup[i] = '0' + str(dym_tup[i])

    date = date_separator.join(strlist(dym_tup))
    time = time_separator.join(
        strlist((input.hour, input.minute) if without_seconds else (input.hour, input.minute, input.second))
    )

    match mode:
        case 'date':
            return date
        case 'time':
            return time
        case 'datetime':
            return f'{date} {time}'
        case _:
            raise ValueError("Invalid mode value")


def now_to_str(mode: Literal['date', 'time', 'datetime'] = 'datetime',
               date_separator: str = '.', time_separator: str = ':', without_seconds: bool = False,
               date_order: Literal['dmy', 'dym', 'mdy', 'myd', 'ydm', 'ymd'] = 'dmy'):
    """
    Get current date/time as formatted string.

    Получает текущую дату/время в виде отформатированной строки.

    Args:
        mode (Literal): Output mode / Режим вывода
        date_separator (str): Separator for date components / Разделитель компонентов даты
        time_separator (str): Separator for time components / Разделитель компонентов времени
        without_seconds (bool): Exclude seconds / Исключить секунды
        date_order (Literal): Order of date components / Порядок компонентов даты

    Returns:
        str: Formatted current date/time / Отформатированная текущая дата/время
    """
    return datetime_to_str(dt.now(), mode, date_separator, time_separator, without_seconds, date_order)


def datetime_to_date_object(input: dt) -> date_object:
    """
    Convert datetime to date object.

    Преобразует datetime в объект date.

    Args:
        input (datetime): Datetime object / Объект datetime

    Returns:
        date: Date object / Объект даты
    """
    return date_object(day=input.day, month=input.month, year=input.year)


def current_timezone(*, raw_data: bool = False) -> Union[str, zoneinfo.ZoneInfo]:
    """
    Get current system timezone.

    Получает текущую системную временную зону.

    Args:
        raw_data (bool): Return ZoneInfo object instead of string, default False / Вернуть объект ZoneInfo вместо строки

    Returns:
        Union[str, zoneinfo.ZoneInfo]: Timezone name or ZoneInfo object / Название временной зоны или объект ZoneInfo
    """
    lz = get_localzone()
    return lz.key if not raw_data else lz


def get_timezone_offset(timezone_name: Optional[str] = None) -> int:
    """
    Get UTC offset in hours for a timezone.

    Получает смещение UTC в часах для временной зоны.

    Args:
        timezone_name (Optional[str]): Timezone name, uses system timezone if None / Название временной зоны

    Returns:
        int: UTC offset in hours / Смещение UTC в часах
    """
    if timezone_name is None:
        timezone_name = current_timezone()
    return int(dt.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()) // 3600
