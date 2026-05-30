"""
Python module utilities for dynamic imports and lazy loading.

Provides functions and classes for importing submodules, lazy imports,
and lazy object loading.

Утилиты для работы с модулями Python для динамического импорта и ленивой загрузки.

Предоставляет функции и классы для импорта подмодулей, ленивого импорта
и ленивой загрузки объектов.
"""

import importlib, pkgutil
from importlib import import_module
from typing import Any


def import_all_submodules(package_name):
    """
    Dynamically import all submodules in a package.

    Динамически импортирует все подмодули в пакете.

    Args:
        package_name (str): Name of the package / Имя пакета
    """
    package = import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        try:
            importlib.import_module(full_module_name)
        except ImportError as e:
            print(f"Failed to import {full_module_name}: {e}")


class LazyImporter:
    """
    Lazily import a module when first accessed.

    Лениво импортирует модуль при первом доступе.

    Args:
        module_name (str): Name of the module to import / Имя модуля для импорта
    """

    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def __getattr__(self, name: str) -> Any:
        """
        Get attribute from lazily loaded module.

        Получает атрибут из лениво загруженного модуля.

        Args:
            name (str): Attribute name / Имя атрибута

        Returns:
            Any: Attribute value / Значение атрибута
        """
        if self._module is None:
            self._module = __import__(self.module_name)
        return getattr(self._module, name)

    def __dir__(self) -> list:
        """
        Get directory of lazily loaded module.

        Получает директорию лениво загруженного модуля.

        Returns:
            list: Module attributes / Атрибуты модуля
        """
        if self._module is None:
            self._module = __import__(self.module_name)
        return dir(self._module)


class LazyImportedObject:
    """
    Lazily import a specific object from a module.

    Лениво импортирует конкретный объект из модуля.

    Args:
        module_name (str): Name of the module / Имя модуля
        object_name (str): Name of the object to import / Имя объекта для импорта
    """

    def __init__(self, module_name: str, object_name: str):
        self.module_name = module_name
        self.object_name = object_name
        self._obj: Any = None

    def _load(self) -> Any:
        """
        Load the object from module.

        Загружает объект из модуля.

        Returns:
            Any: Loaded object / Загруженный объект
        """
        if self._obj is None:
            module = importlib.import_module(self.module_name)
            self._obj = getattr(module, self.object_name)
        return self._obj

    def __call__(self, *args, **kwargs):
        """
        Call the lazily loaded object (for functions and classes).

        Вызывает лениво загруженный объект (для функций и классов).

        Args:
            *args: Positional arguments / Позиционные аргументы
            **kwargs: Keyword arguments / Ключевые аргументы

        Returns:
            Result of call / Результат вызова
        """
        return self._load()(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """
        Get attribute from lazily loaded object.

        Получает атрибут из лениво загруженного объекта.

        Args:
            name (str): Attribute name / Имя атрибута

        Returns:
            Any: Attribute value / Значение атрибута
        """
        return getattr(self._load(), name)

    def __getitem__(self, key):
        """
        Get item from lazily loaded object (if it supports indexing).

        Получает элемент из лениво загруженного объекта (если поддерживает индексацию).

        Args:
            key: Index or key / Индекс или ключ

        Returns:
            Item value / Значение элемента
        """
        return self._load()[key]
