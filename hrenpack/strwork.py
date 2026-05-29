import string, re
from typing import Union
from random import randint, choice as randchoice

PYTHONNAME_LETTERS = string.ascii_lowercase + string.digits + '_'
tuplist = Union[tuple, list]


def antienter_str(string: str, space: bool = True) -> str:
    separator = ' ' if space else ''
    return separator.join(string.split('\n'))


def antispace(string: str) -> str: return ''.join(string.split())


def string_add(*args: str) -> str: return ''.join(args)


def randstr(a: int, b: int) -> str:
    return str(randint(a, b))


def prefix(base: str, prefix: str, is_suffix: bool = False) -> str:
    return base + prefix if is_suffix else prefix + base


def in_or(string: str, *args: str) -> bool:
    for arg in args:
        if arg in string: return True
    return False


def in_and(string: str, *args: str) -> bool:
    for arg in args:
        if arg not in string: return False
    return True


def index_edit(string: str, index: int, letter: str) -> str:
    if len(letter) != 1:
        raise ValueError('Letter must be a single character')
    p1 = string[:index]
    p2 = string[index + 1:]
    return p1 + letter + p2


def string_reverse(string: str):
    output = list(string)
    output.reverse()
    return ''.join(output)


def index_edit_multi(string: str, values: dict[int, str]) -> str:
    for key, value in values.items():
        string = index_edit(string, key, value)
    return string


def index_edit_join(string: str, indexes: tuplist, values: Union[tuplist, str]) -> str:
    if len(indexes) != len(values):
        raise ValueError('Length of indexes must be equal to length of values')
    elif len(indexes) == 0 or len(values) == 0:
        raise ValueError('Empty indexes or values')
    else:
        for i in range(len(indexes)):
            if type(indexes[i]) is not int:
                raise ValueError('Indexes must be integers')
            if type(values[i]) is not str:
                raise ValueError('Values must be strings')
            string = index_edit(string, indexes[i], values[i])
        return string


def generate_rand_string(length: int = 25):
    return ''.join(randchoice(string.ascii_letters + string.digits) for _ in range(length))


def remove_extra_spaces(text):
    # Заменяем несколько пробелов подряд на один
    return re.sub(r'\s+', ' ', text).strip()


def words_to_letters(*words: str) -> list:
    return list(''.join(words))


def only_this_letters(text: str, *letters: str) -> bool:
    letters = words_to_letters(*letters)
    for letter in text:
        if letter not in letters:
            return False
    return True


def only_pythonname(text: str) -> bool:
    return only_this_letters(text, PYTHONNAME_LETTERS)


def strip_quotes(text: str) -> str:
    if len(text) < 2:
        return text
    elif text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    elif text[0] == "'" and text[-1] == "'":
        return text[1:-1]
    return text
