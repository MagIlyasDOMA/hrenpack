"""
Django model fields extensions.

Provides custom model fields and lookups for Django.

Расширения полей моделей Django.

Предоставляет пользовательские поля моделей и поисковые запросы для Django.
"""

from django.db import models
from .lookup import DirnameLookup


class FilePathField(models.CharField):
    """
    CharField for file paths with dirname lookup support.

    CharField для путей к файлам с поддержкой поиска по имени директории.
    """
    pass


FilePathField.register_lookup(DirnameLookup)
