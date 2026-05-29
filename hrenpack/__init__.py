from .functionwork import empty_function
from .strwork import randstr
from .typings import *


def credits():
    print("Hrenpack")
    print("(c) Mag Ilyas DOMA, 2024-2026.")
    print("Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)")


__version__ = '3.0.0-beta.5'


def sts(word):
    stars = '*' * len(word)
    return stars


def of_utf8(filename, mode='r'):
    file = open(filename, mode, encoding='utf-8')
    return file


def write_a(path, data):
    file = open(path, 'a', encoding='utf-8')
    file.write(f'{str(data)}\n')
    file.close()


def write(path, text):
    file = open(path, 'w', encoding='utf-8')
    file.write(str(text))
    file.close()


def switch(variable, case: dict, default=empty_function):
    for key in case:
        func = case[key]
        if variable == key:
            func()
            break
    else:
        default()


def bincode_generator(length: int, is_int: bool = False):
    bincode = ''
    for i in range(length):
        bincode = bincode + randstr(0, 1)
    return int(bincode) if is_int else bincode


def who_called_me():
    import inspect
    current_frame = inspect.currentframe()
    calling_frame = current_frame.f_back
    return inspect.getfile(calling_frame)


def module_is_installed(module_name: str):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
