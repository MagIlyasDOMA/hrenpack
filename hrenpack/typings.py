"""
Type hints and aliases for the hrenpack package.

Provides common type definitions for use throughout the package.

Подсказки типов и псевдонимы для пакета hrenpack.

Предоставляет общие определения типов для использования во всем пакете.
"""

from typing import Union, Optional, Literal, Callable, Any
from pathlib import Path
from pathlike_typing import PathLike
from hrenpack.classes import range_plus


def literal_add(base, *args):
    """
    Add literals to a Union type.

    Добавляет литералы к Union типу.

    Args:
        base: Base Union type / Базовый Union тип
        *args: Literal values to add / Литеральные значения для добавления

    Returns:
        Union: Union type with added literals / Union тип с добавленными литералами
    """
    return Union[base, Literal[*args]]


Number = Union[int, float]
"""Union type for int and float."""

SimpleList = Union[list, tuple, set]
"""Union type for simple sequence types."""

si = Union[int, str]
"""Union type for int or str."""

IntStr = si
"""Alias for si (int or str)."""

NullStr = Optional[str]
"""Optional string type."""

integer, string, boolean = int, str, bool
"""Aliases for basic types."""

tuplist = Union[list, tuple]
"""Union type for list or tuple."""

tdl = Union[tuple, list, dict]
"""Union type for tuple, list, or dict."""

ColorTyping = Union[tuple[int, int, int], list[int, int, int], tuple[int, int, int, float], list[int, int, int, float]]
"""Type for RGB or RGBA color values."""

FivePointScale = Literal[*range_plus(5)]
"""Literal type for 1-5 scale."""

TenPointScale = Literal[*range_plus(10)]
"""Literal type for 1-10 scale."""

ZeroFivePointScale = literal_add(FivePointScale, 0)
"""Literal type for 0-5 scale."""

ZeroTenPointScale = literal_add(TenPointScale, 0)
"""Literal type for 0-10 scale."""

ThemeType = Literal['light', 'dark']
"""Literal type for theme names."""

EnvDict = dict[str, str]
"""Dictionary type for environment variables."""

JsonData = Union[str, int, float, bool, dict, list]
"""Type for JSON-serializable data."""

HttpMethodBasic = Literal['GET', 'POST']
"""Basic HTTP method literals."""

HttpMethodExtended = Union[HttpMethodBasic, Literal['PUT', 'PATCH', 'DELETE']]
"""Extended HTTP method literals."""

HttpMethod = Union[HttpMethodExtended, Literal['HEAD', 'OPTIONS', 'TRACE', 'CONNECT']]
"""All standard HTTP method literals."""

GetterFunc = Callable[[], Any]
"""Type for getter function with no arguments."""

SetterFunc = Callable[[Any], None]
"""Type for setter function with one argument."""
