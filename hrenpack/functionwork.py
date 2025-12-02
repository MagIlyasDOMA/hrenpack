# Hrenpack v2.2.1
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from hrenpack import null


def function_if(condition: bool, true, false=null, is_lambda: bool = False):
    if condition:
        return true if is_lambda else true()
    else:
        return false if is_lambda else false()


def lambda_generator(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def callable_object(arg):
    return lambda: arg
