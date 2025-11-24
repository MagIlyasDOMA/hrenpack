# Hrenpack v2.0.0
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from typing import TypedDict, Optional, Literal, Union
from datetime import datetime, date
from hrenpack.typings import SimpleList, Number

InputType = Literal[
    "button",
    "checkbox",
    "color",
    "date",
    "datetime-local",
    "email",
    "file",
    "hidden",
    "image",
    "month",
    "number",
    "password",
    "radio",
    "range",
    "reset",
    "search",
    "submit",
    "tel",
    "text",
    "time",
    "url",
    "week"
]

InputTypeExtended = Union[InputType, Literal["textarea"]]

MinMaxType = Union[Number, datetime, date]


class InputAttrs(TypedDict):
    autofocus: bool
    pattern: str
    min: MinMaxType
    max: MinMaxType
    step: Number
    checked: bool
    multiple: bool
    accept: Union[str, SimpleList]

