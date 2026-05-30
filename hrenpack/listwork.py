import re
from typing import Union, Literal, Optional, Iterable, Sequence, MutableMapping, Mapping

tdl = Union[tuple, dict, list]


def antizero(wnull, /):
    if wnull < 10: output = '0' + str(wnull)
    else: output = str(wnull)
    return output


def intlist(input: list) -> list: return list(map(int, input))


def floatlist(input: list) -> list: return list(map(float, input))


def list_add(input: list, index: int, data) -> list:
    forloop = len(input) + 1
    output = list()
    for i in range(forloop):
        if i < index:
            output.append(input[i])
        elif i == index:
            output.append(data)
        elif i > index:
            m = i - 1
            output.append(input[m])
    return output


def merging_dictionaries(*dicts: dict, **kwargs) -> dict:
    return {**(dct for dct in dicts), **kwargs}


def split_quotes(text: str) -> list:
    pattern = r"""
            (?:
                "(?:[^"\\]|\\.)*"
                |
                '(?:[^'\\]|\\.)*'
                |
                \S+              
            )
        """
    return re.findall(pattern, text, re.VERBOSE)


def del_keys(input: dict, *keys) -> None:
    for key in keys:
        del input[key]


def dict_index(input: dict, value):
    for k, v in input.items():
        if v == value:
            return k
    else:
        raise ValueError(f"Словарь {input} не содержит значения {value}")


def strlist(input: list):
    input = list(input)
    for i in range(len(input)): input[i] = str(input[i])
    return input


def keys_dict_equals(*dicts: dict) -> bool:
    dicts = list(dicts)
    first = tuple(dicts.pop(0).keys())
    for d in dicts:
        if first != tuple(d.keys()):
            return False
    return True


def del_none(lst: list) -> list:
    while None in lst: lst.remove(None)
    return lst


def del_none_from_dict(*dicts, **kwargs) -> dict:
    kwargs = merging_dictionaries(*dicts, kwargs)
    output = kwargs.copy()
    for key, value in kwargs.items():
        if value is None:
            output.pop(key)
    return output


def get_from_dict(input: dict, *keys, only_values: bool = False, default=None,
                  pop_mode: bool = False):
    output = dict()
    for key in keys:
        value = input.pop(key, default)
        output[key] = value
        if not pop_mode:
            input[key] = value
    if only_values: return list(output.values())
    return output


def replace_fragment_from_args(old_frag: str, new_frag: str, *args: str, is_tuple: bool = False) -> list:
    return [arg.replace(old_frag, new_frag) for arg in args]


class dict_enumerate:
    def __init__(self, items: dict):
        self.items = items.items() if isinstance(items, dict) else items

    def __iter__(self):
        for i, kv in enumerate(self.items): yield i, *kv


def selective_slice(input, *keys, only_values: bool = False) -> tdl:
    output = dict()
    for key in keys:
        output[key] = input[key]
    if only_values:
        return list(output.values())
    return output


def dict_get(dct: dict, key, default=None):
    output = dct.get(key)
    if output and output is not False:
        return default
    return output


def mislist(input: list, *args) -> list:
    return [arg for arg in args if arg not in input]


def dict_slice(input: dict, *keys, only_values: bool = False, all_required: bool = False):
    output = dict()
    for key in keys:
        if key in input:
            output[key] = input[key]
        elif all_required:
            raise KeyError(key)
    return list(output.values()) if only_values else output


def two_tuples_to_dict(keys: Iterable, values: Iterable) -> dict:
    return dict(zip(keys, values))


def reverse_dict(input: dict) -> dict:
    return dict(two_tuples_to_dict(input.values(), input.keys()))


def getitem_plus(input: Mapping, tree: Sequence[str], default=None, *, catch_errors: bool = True):
    from hrenpack.encapsulation import getattr_plus
    return getattr_plus(input, tree, default, dict_mode=True, catch_errors=catch_errors)


def setitem_plus(input: MutableMapping, tree: Sequence[str], value, *, strict: bool = False):
    if isinstance(tree, str): tree = tree.split('.')
    last_key = tree.pop()
    obj = input
    for level, key in enumerate(tree):
        if not hasattr(obj, '__setitem__'): raise TypeError(f"Key in level {level} is not MutableMapping")
        elif key not in obj:
            if strict: raise KeyError(f"'{key}' in level {level}")
            obj[key] = dict()
        obj = obj[key]
    else: obj[last_key] = value
