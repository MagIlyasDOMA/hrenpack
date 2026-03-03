import time, datetime, pytz, zoneinfo
from datetime import datetime as dt, date as date_object
from dataclasses import dataclass
from typing import Union, Optional, Literal
from tzlocal import get_localzone
from hrenpack.listwork import intlist, strlist


class HoursMinutesAndSeconds:
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.__time_format()

    def __str__(self):
        h, m, s = self.hours, self.minutes, self.seconds
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        return '{}:{}:{}'.format(h, m, s)

    def __int__(self):
        return self.to_seconds()

    def __bool__(self):
        return self.to_seconds() != 0

    def __add__(self, other):
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
            # h, m, s = time_format(h, m, s)
        else:
            raise ValueError('From HoursMinutesAndSeconds can subtract int, str or HoursMinutesAndSeconds')
        return HoursMinutesAndSeconds(h, m, s)

    def __mul__(self, other: int):
        h = self.hours * other
        m = self.minutes * other
        s = self.seconds * other
        return HoursMinutesAndSeconds(h, m, s)

    def __time_format(self):
        while self.seconds >= 60:
            self.seconds -= 60
            self.minutes += 1
        while self.minutes >= 60:
            self.minutes -= 60
            self.hours += 1

    @classmethod
    def from_seconds(cls, seconds: int):
        return cls(*time_format(0, 0, seconds))

    @classmethod
    def from_string(cls, string: str, separator: str = ':', ms: Optional[bool] = None):
        slist = string.split(separator)
        if slist.__len__() == 3:
            h, m, s = string.split(separator)
        elif slist.__len__() == 2:
            if ms is None:
                raise ValueError('Если используются только 2 аргумента, то параметр ms должен быть булевым значением')
            elif ms:
                h = 0
                m, s = slist
            else:
                h, m = slist
                s = 0
        else:
            raise ValueError("Аргументов должно быть либо 2, либо 3")
        return cls(int(h), int(m), int(s))

    def to_seconds(self) -> int:
        return self.hours * 3600 + self.minutes * 60 + self.seconds


def time_format(hours: int, minutes: int, seconds: int, return_mode: Literal['string', 'tuple', 'class'] = 'tuple'):
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
    return '0' + str(input) if input < 10 else str(input)


def date_and_time_data():
    @dataclass
    class Data:
        date: str
        time: str

    now = dt.now()
    date = f'{datetime_format(now.day)}.{datetime_format(now.month)}.{now.year}'
    time = f'{datetime_format(now.hour)}:{datetime_format(now.minute)}:{datetime_format(now.second)}'
    return Data(date, time)


def date(year: bool) -> str:
    now = dt.now()
    data = f'{now.day}.{now.month}'
    return data + f'.{now.year}' if year else data


def time_summ(*args: Union[str, HoursMinutesAndSeconds], return_hms: bool = False):
    args = list(args)
    first = args[0]
    output = HoursMinutesAndSeconds.from_string(first) if type(first) is str else first
    args.pop(0)
    for arg in args:
        output += arg
    return output if return_hms else str(output)


def perf_counter(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print(end - start)

    return wrapper


def unix_to_datetime(unix_timestamp: int) -> dt:
    return dt.fromtimestamp(unix_timestamp)


def datetime_to_time(input: dt) -> datetime.time:
    return datetime.time(input.hour, input.minute, input.second)


def string_to_datetime(input: str, dt_separator: str = ' ', date_separator: str = '.', time_separator: str = ':',
                       date_reverse: bool = False) -> dt:
    date, time = input.split(dt_separator)
    date = intlist(date.split(date_separator))
    time = intlist(time.split(time_separator))
    if date_reverse:
        date = list(reversed(date))
    return dt(*date, *time)


def string_to_date(input: str, date_separator: str = '.', date_reverse: bool = False) -> dt:
    return string_to_datetime(input + ' 00:00:00', date_separator=date_separator, date_reverse=date_reverse)


def zero_form(input: Union[str, int]):
    if isinstance(input, str):
        input = int(input)
    return str(input) if input > 9 else '0' + str(input)


def zero_str(input: Union[str, dt]):
    if isinstance(input, str):
        output = input.split(':')
        if len(output) == 2:
            h, m = output
            return ':'.join([zero_form(h), zero_form(m)])
        elif len(output) == 3:
            h, m, s = output
            return ':'.join([zero_form(h), zero_form(m), zero_form(s)])
        else:
            raise ValueError
    else:
        h, m, s = input.hour, input.minute, input.second
        return ':'.join([zero_form(h), zero_form(m), zero_form(s)])


def datetime_to_str(input: dt, mode: Literal['date', 'time', 'datetime'] = 'datetime',
                    date_separator: str = '.', time_separator: str = ':', without_seconds: bool = False,
                    date_order: Literal['dmy', 'dym', 'mdy', 'myd', 'ydm', 'ymd'] = 'dmy') -> str:
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
            raise ValueError

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
            raise ValueError


def now_to_str(mode: Literal['date', 'time', 'datetime'] = 'datetime',
               date_separator: str = '.', time_separator: str = ':', without_seconds: bool = False,
               date_order: Literal['dmy', 'dym', 'mdy', 'myd', 'ydm', 'ymd'] = 'dmy'):
    return datetime_to_str(dt.now(), mode, date_separator, time_separator, without_seconds, date_order)


def datetime_to_date_object(input: dt) -> date_object:
    return date_object(day=input.day, month=input.month, year=input.year)


def current_timezone(*, /, raw_data: bool = False) -> Union[str, zoneinfo.ZoneInfo]:
    lz = get_localzone()
    return lz.key if not raw_data else lz


def get_timezone_offset(timezone_name: Optional[str] = None) -> int:
    if timezone_name is None: timezone_name = current_timezone()
    return int(dt.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()) // 3600
