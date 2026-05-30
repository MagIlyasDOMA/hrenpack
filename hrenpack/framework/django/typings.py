"""
Type hints for Django framework.

Provides Protocol types for forms with cleaned_data.

Подсказки типов для фреймворка Django.

Предоставляет Protocol типы для форм с cleaned_data.
"""

from typing import Protocol, TypeVar, Dict, Any

D = TypeVar('D', default=Dict[str, Any])
"""
Type variable for cleaned_data dictionary type.
Тип переменной для словаря cleaned_data.
"""


class Form(Protocol[D]):
    """
    Protocol for Django forms with cleaned_data.

    Protocol для форм Django с cleaned_data.

    Attributes:
        cleaned_data (D): Cleaned form data / Очищенные данные формы
    """
    cleaned_data: D

    def is_valid(self) -> bool:
        """
        Check if form is valid.

        Проверяет, валидна ли форма.

        Returns:
            bool: True if valid / True если валидна
        """
        ...
