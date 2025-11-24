# Hrenpack v2.0.0
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from typing import Optional, Union
from hrenpack.typings import SimpleList


class InputAttrsMixin:
    checked: bool = False
    placeholder: Optional[str] = None
    minlength: Optional[int] = None
    maxlength: Optional[int] = None
    step: Optional[int] = None
    multiple: bool = False
    accept: Optional[Union[str, SimpleList]] = None
