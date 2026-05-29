def kwarg_function(kwargs: dict, key: str, true, false):
    if key in kwargs:
        true()
    else:
        false()


def get_kwarg(kwargs: dict, key: str, default=None, raise_error: bool = True, delete: bool = False):
    if default:
        raise_error = False
    if raise_error and key not in kwargs:
        raise KeyError(key)
    output = kwargs.get(key, default)
    if delete and key in kwargs:
        del kwargs[key]
    return output


def exclude_nones(**kwargs) -> dict:
    output = dict()
    for key, value in kwargs.items():
        if value is not None: output[key] = value
    return output
