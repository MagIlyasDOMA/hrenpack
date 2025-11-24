# Hrenpack v2.0.0
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

import functools
from markupsafe import Markup


def safe(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return Markup(str(func(*args, **kwargs)))
    return wrapper

