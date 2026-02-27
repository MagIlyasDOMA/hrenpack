import importlib, pkgutil
from importlib import import_module
from typing import Any


def import_all_submodules(package_name):
    """Динамически импортирует все подмодули в пакете."""
    package = import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        try:
            importlib.import_module(full_module_name)
        except ImportError as e:
            print(f"Failed to import {full_module_name}: {e}")


class LazyImporter:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def __getattr__(self, name: str) -> Any:
        if self._module is None:
            self._module = __import__(self.module_name)
        return getattr(self._module, name)

    def __dir__(self) -> list:
        if self._module is None:
            self._module = __import__(self.module_name)
        return dir(self._module)


class LazyImportedObject:
    def __init__(self, module_name: str, object_name: str):
        self.module_name = module_name
        self.object_name = object_name
        self._obj: Any = None

    def _load(self) -> Any:
        if self._obj is None:
            module = importlib.import_module(self.module_name)
            self._obj = getattr(module, self.object_name)
        return self._obj

    def __call__(self, *args, **kwargs):
        """Для функций и классов"""
        return self._load()(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """Для доступа к атрибутам класса"""
        return getattr(self._load(), name)

    def __getitem__(self, key):
        """Если объект поддерживает индексацию"""
        return self._load()[key]
