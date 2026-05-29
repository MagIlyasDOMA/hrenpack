from typing import Optional, Any


def is_int(data) -> bool:
    try: int(data)
    except ValueError: return False
    else: return True


def is_float(data) -> bool:
    try: float(data)
    except ValueError: return False
    else: return True


def is_bool(data) -> bool:
    try: bool(data)
    except ValueError: return False
    else: return True


def convert_to_boolean(input: Any) -> bool:
    if isinstance(input, bool): return input
    elif isinstance(input, str):
        if input.lower() in ('true', 'yes', 'on', '1', 't', 'y'): return True
        elif input.lower() in ('false', 'no', 'off', '0', 'f', 'n'): return False
        else: raise ValueError('Invalid boolean value')
    else: return bool(input)


def is_boolean(input: Any) -> bool:
    try: convert_to_boolean(input)
    except: return False
    else: return True


def isinstance_multi(obj, *types) -> bool:
    return isinstance(obj, types)


def issubclass_multi(obj, *classes) -> bool:
    return issubclass(obj, classes)


def is_object(arg, filter_uneditable: bool = True) -> Optional[bool]:
    if isinstance(arg, type):
        return False
    elif filter_uneditable and isinstance_multi(arg, int, str, float, bool, tuple, frozenset, bytes):
        return False
    elif isinstance(arg, object):
        return True
    return False
