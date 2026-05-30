"""
Useful classes for Python development.

Provides DictObject, frozendict, Environment, NonStrictDict, and other utility classes.

Полезные классы для разработки на Python.

Предоставляет DictObject, frozendict, Environment, NonStrictDict и другие классы-утилиты.
"""

import platform, os
import warnings
from typing import Any, IO, Optional, Literal
from dotenv import load_dotenv, dotenv_values
from pathlike_typing import PathLike
from .listwork import merging_dictionaries
from .type_define import convert_to_boolean


class DictObject:
    """
    Convert a dictionary to an object with attribute access.

    Преобразует словарь в объект с доступом через атрибуты.

    Args:
        dictionary (dict): Source dictionary / Исходный словарь
        recursive (bool): Recursively convert nested dicts, default False / Рекурсивно преобразовывать вложенные словари
    """

    def __init__(self, dictionary: dict, recursive: bool = False):
        for key, value in dictionary.items():
            if isinstance(value, dict) and recursive:
                # Recursively convert nested dictionaries
                setattr(self, key, DictObject(value))
            elif isinstance(value, list) and recursive:
                # Process lists with possible nested dictionaries
                setattr(self, key, [
                    DictObject(item) if isinstance(item, dict) else item
                    for item in value
                ])
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"<DictObject: {self.__dict__}>"

    def __getitem__(self, item):
        """
        Get value using dictionary-style indexing.

        Получает значение через индексацию как в словаре.

        Args:
            item: Key to access / Ключ для доступа

        Returns:
            Value associated with key / Значение, связанное с ключом

        Raises:
            KeyError: If attribute does not exist / Если атрибут не существует
        """
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def __setitem__(self, key, value):
        """
        Set value using dictionary-style indexing.

        Устанавливает значение через индексацию как в словаре.

        Args:
            key: Key to set / Ключ для установки
            value: Value to assign / Значение для присвоения
        """
        setattr(self, key, value)

    def __delitem__(self, key):
        """
        Delete attribute using dictionary-style indexing.

        Удаляет атрибут через индексацию как в словаре.

        Args:
            key: Key to delete / Ключ для удаления

        Raises:
            KeyError: If attribute does not exist / Если атрибут не существует
        """
        if hasattr(self, key):
            delattr(self, key)
        raise KeyError(key)


def call_method(method_name: str, objects: tuple, *args, **kwargs):
    """
    Call a method on multiple objects.

    Вызывает метод на нескольких объектах.

    Args:
        method_name (str): Name of the method to call / Имя вызываемого метода
        objects (tuple): Tuple of objects / Кортеж объектов
        *args: Positional arguments for the method / Позиционные аргументы для метода
        **kwargs: Keyword arguments for the method / Ключевые аргументы для метода
    """
    for obj in objects:
        getattr(obj, method_name)(*args, **kwargs)


class TkTemplate:
    """
    Template for Tkinter windows (Windows only).

    Шаблон для окон Tkinter (только Windows).

    Args:
        title (str): Window title / Заголовок окна
        width (int): Window width / Ширина окна
        height (int): Window height / Высота окна
        background (str): Background color, default 'white' / Цвет фона
        resizable (bool): Whether window is resizable, default False / Можно ли изменять размер
        icon (str): Path to icon file / Путь к файлу иконки
        stylesheet (dict): Stylesheet dictionary / Словарь стилей

    Raises:
        OSError: On non-Windows systems or if tkinter not installed / На не-Windows системах или если tkinter не установлен
    """

    # Implementation depends on platform


class Class:
    """Simple empty class / Обычный пустой класс"""
    pass


class range_plus:
    """
    Enhanced range with more flexible arguments.

    Улучшенный range с более гибкими аргументами.

    Args:
        *args: Positional arguments: (end) or (start, end) or (start, end, step) / Позиционные аргументы
        **kwargs: Keyword arguments: start, end, step / Ключевые аргументы

    Raises:
        ValueError: If no arguments or too many arguments / Если нет аргументов или слишком много
    """

    def __init__(self, *args, **kwargs):
        if kwargs:
            new_args = (kwargs.get('start', 1), kwargs['end'], kwargs.get('step', 1))
        elif args:
            args = list(args)
            largs = len(args)
            if largs == 1:
                new_args = (1, args[0] + 1, 1)
            else:
                args[1] += 1
                if largs == 2:
                    new_args = (args[0], args[1], 1)
                elif largs == 3:
                    new_args = args
                else:
                    raise ValueError("Maximum 3 arguments")
        else:
            raise ValueError("At least 1 argument required")

        self.range = range(*new_args)

    def __iter__(self):
        return iter(self.range)

    def __str__(self):
        return str(self.range)


class RawString(str):
    """
    String subclass that preserves raw string behavior when concatenating.

    Подкласс строки, сохраняющий поведение сырой строки при конкатенации.
    """

    def __add__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return RawString(super().__add__(other))

    def __radd__(self, other):
        return RawString(str(other) + str(self))

    def convert(self):
        """
        Convert to regular string.

        Преобразует в обычную строку.

        Returns:
            str: Regular string / Обычная строка
        """
        return str(self)

    def __eq__(self, other):
        return other == self or str(other) == str(self)


class frozendict(dict):
    """
    Immutable dictionary.

    Неизменяемый словарь.

    Raises:
        TypeError: On any modification attempt / При любой попытке изменения
    """

    def __setitem__(self, key, value):
        raise TypeError(f"'{self.__class__.__name__}' object does not support item assignment")

    def __delitem__(self, key):
        raise TypeError(f"'{self.__class__.__name__}' object does not support item deletion")

    def __hash__(self):
        return hash(tuple(self.items()))


class Environment:
    """
    Environment variable manager with local and global storage.

    Менеджер переменных окружения с локальным и глобальным хранилищем.

    Args:
        **local_data: Initial local environment variables / Начальные локальные переменные окружения
    """

    def __init__(self, **local_data):
        self.local_data = self._format_dict(local_data)

    @staticmethod
    def _format_dict(*dicts: dict, **kwargs) -> dict:
        """
        Format dictionary keys to uppercase.

        Форматирует ключи словаря в верхний регистр.

        Args:
            *dicts: Dictionaries to merge / Словари для объединения
            **kwargs: Additional key-value pairs / Дополнительные пары ключ-значение

        Returns:
            dict: Formatted dictionary with uppercase keys / Отформатированный словарь с ключами в верхнем регистре

        Raises:
            TypeError: If key is not string / Если ключ не является строкой
        """
        output = dict()
        for key, value in merging_dictionaries(*dicts, kwargs).items():
            if not isinstance(key, str):
                raise TypeError("Key must be str")
            output[key.upper()] = value
        return output

    @staticmethod
    def _dotenv_values(dotenv_path: PathLike = None, stream: Optional[IO[str]] = None, verbose: bool = False,
                       override: bool = False, interpolate: bool = True, encoding: str = 'utf-8'):
        """Get values from .env file without loading to os.environ."""
        return dotenv_values(dotenv_path, stream, verbose, interpolate, encoding)

    @classmethod
    def load(cls, dotenv_path: PathLike = None, stream: Optional[IO[str]] = None, verbose: bool = False,
             override: bool = False, interpolate: bool = True, encoding: str = 'utf-8',
             local: bool = False) -> 'Environment':
        """
        Load environment from .env file.

        Загружает окружение из .env файла.

        Args:
            dotenv_path: Path to .env file / Путь к .env файлу
            stream: File stream / Поток файла
            verbose: Verbose mode / Подробный режим
            override: Override existing variables / Переопределять существующие переменные
            interpolate: Interpolate variables / Интерполировать переменные
            encoding: File encoding / Кодировка файла
            local: Store locally only, don't set in os.environ / Хранить только локально

        Returns:
            Environment: Environment instance / Экземпляр Environment
        """
        dotenv_func = cls._dotenv_values if local else load_dotenv
        raw_data = dotenv_func(dotenv_path, stream, verbose, override, interpolate, encoding)
        data = dict(raw_data) if local else dict()
        return cls(**data)

    def __getitem__(self, key: str):
        """
        Get environment variable (local first, then global).

        Получает переменную окружения (сначала локальную, затем глобальную).

        Args:
            key (str): Variable name / Имя переменной

        Returns:
            Variable value / Значение переменной

        Raises:
            KeyError: If variable not found / Если переменная не найдена
        """
        if key in self.local_data:
            return self.local_data[key]
        return os.environ[key]

    def __setitem__(self, key: str, value: Any):
        """
        Set global environment variable.

        Устанавливает глобальную переменную окружения.

        Args:
            key (str): Variable name / Имя переменной
            value (Any): Value to set / Значение для установки
        """
        os.environ[key.upper()] = str(value)

    def __delitem__(self, key):
        """
        Delete environment variable.

        Удаляет переменную окружения.

        Args:
            key: Variable name / Имя переменной

        Raises:
            KeyError: If variable not found / Если переменная не найдена
        """
        if key in self.local_data:
            del self.local_data[key]
        del os.environ[key]

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get variable with default value.

        Получает переменную со значением по умолчанию.

        Args:
            key (str): Variable name / Имя переменной
            default (Any): Default value if not found / Значение по умолчанию

        Returns:
            Variable value or default / Значение переменной или значение по умолчанию
        """
        try:
            return self[key]
        except KeyError:
            return default

    def get_int(self, key: str, default: Optional[int] = None, strict: bool = True) -> Optional[int]:
        """
        Get variable as integer.

        Получает переменную как целое число.

        Args:
            key (str): Variable name / Имя переменной
            default (Optional[int]): Default value / Значение по умолчанию
            strict (bool): Raise exception on conversion error if True / Выбрасывать исключение при ошибке преобразования

        Returns:
            Optional[int]: Integer value or default / Целое значение или значение по умолчанию

        Raises:
            TypeError, ValueError: If conversion fails and strict=True / Если преобразование не удалось и strict=True
        """
        try:
            return int(self.get(key, default))
        except (TypeError, ValueError) as error:
            if strict:
                raise error
            return default

    def get_float(self, key: str, default: Optional[float] = None, strict: bool = True) -> Optional[float]:
        """
        Get variable as float.

        Получает переменную как число с плавающей точкой.

        Args:
            key (str): Variable name / Имя переменной
            default (Optional[float]): Default value / Значение по умолчанию
            strict (bool): Raise exception on conversion error if True / Выбрасывать исключение при ошибке преобразования

        Returns:
            Optional[float]: Float value or default / Значение с плавающей точкой или значение по умолчанию
        """
        try:
            return float(self.get(key, default))
        except (TypeError, ValueError) as error:
            if strict:
                raise error
            return default

    def get_bool(self, key: str, default: Optional[bool] = None, strict: bool = True) -> Optional[bool]:
        """
        Get variable as boolean.

        Получает переменную как булево значение.

        Args:
            key (str): Variable name / Имя переменной
            default (Optional[bool]): Default value / Значение по умолчанию
            strict (bool): Raise exception on conversion error if True / Выбрасывать исключение при ошибке преобразования

        Returns:
            Optional[bool]: Boolean value or default / Булево значение или значение по умолчанию
        """
        try:
            value = (self.get(key, default)
                     if not isinstance(self, type)
                     else os.environ.get(key.upper(), default))
            return convert_to_boolean(value) if value is not None else default
        except (TypeError, ValueError) as error:
            if strict:
                raise error
            return default

    def set(self, key: str, value: Any, local: bool = False) -> None:
        """
        Set environment variable.

        Устанавливает переменную окружения.

        Args:
            key (str): Variable name / Имя переменной
            value (Any): Value to set / Значение для установки
            local (bool): Store locally only, default False / Хранить только локально
        """
        if not local:
            self[key] = value
        else:
            self.local_data[key.upper()] = value

    def setdefault(self, key: str, value: Any, local: bool = False, local_global: bool = False) -> None:
        """
        Set variable if not already set.

        Устанавливает переменную, если она еще не установлена.

        Args:
            key (str): Variable name / Имя переменной
            value (Any): Value to set / Значение для установки
            local (bool): Store locally only / Хранить только локально
            local_global (bool): Deprecated, ignored when local=False / Устаревший, игнорируется
        """
        if not local:
            if local_global:
                warnings.warn('The local_global argument will not apply because local=False', UserWarning, 2)
            if self.get(key) is None:
                self.set(key, value)
        else:
            if key in self:
                return
            self.local_data.setdefault(key.upper(), value)

    def write_local(self, delete: bool = False) -> 'Environment':
        """
        Write local variables to global environment.

        Записывает локальные переменные в глобальное окружение.

        Args:
            delete (bool): Clear local data after writing, default False / Очистить локальные данные после записи

        Returns:
            Environment: Self for chaining / Себя для цепочки вызовов
        """
        for key, value in self.local_data.items():
            os.environ[key] = str(value)
        if delete:
            self.local_data = dict()
        return self

    def update(self, *dicts, **kwargs) -> 'Environment':
        """
        Update global environment with dictionaries.

        Обновляет глобальное окружение словарями.

        Args:
            *dicts: Dictionaries to merge / Словари для объединения
            **kwargs: Additional key-value pairs / Дополнительные пары ключ-значение

        Returns:
            Environment: Self for chaining / Себя для цепочки вызовов
        """
        for key, value in self._format_dict(*dicts, **kwargs).items():
            self[key] = value
        return self

    def update_local(self, *dicts, **kwargs) -> 'Environment':
        """
        Update local environment with dictionaries.

        Обновляет локальное окружение словарями.

        Args:
            *dicts: Dictionaries to merge / Словари для объединения
            **kwargs: Additional key-value pairs / Дополнительные пары ключ-значение

        Returns:
            Environment: Self for chaining / Себя для цепочки вызовов
        """
        self.local_data.update(self._format_dict(*dicts, **kwargs))
        return self

    def delete(self, *keys: str) -> 'Environment':
        """
        Delete variables.

        Удаляет переменные.

        Args:
            *keys: Variable names to delete / Имена переменных для удаления

        Returns:
            Environment: Self for chaining / Себя для цепочки вызовов
        """
        for key in keys:
            try:
                del self[key]
            except KeyError:
                pass
        return self

    def __iter__(self):
        """Iterate over all environment variables."""
        return iter(merging_dictionaries(dict(os.environ), self.local_data))

    def write_file(self, filename: PathLike = '.env', *vars: str, local: bool = False,
                   global_: bool = True, blacklist_mode: bool = False) -> None:
        """
        Write environment variables to a .env file.

        Записывает переменные окружения в .env файл.

        Args:
            filename: Output file path / Путь к выходному файлу
            *vars: Variable names to include / Имена переменных для включения
            local (bool): Use only local data / Использовать только локальные данные
            global_ (bool): Use global environment / Использовать глобальное окружение
            blacklist_mode (bool): Treat vars as blacklist instead of whitelist / Использовать vars как черный список

        Raises:
            ValueError: If both local and global_ are False / Если оба флага False
        """
        global_env = dict(os.environ)
        if global_ and local:
            env = merging_dictionaries(global_env, self.local_data)
        elif global_:
            env = self.local_data
        elif local:
            env = global_env
        else:
            raise ValueError("At least one of local or global_ must be True")

        with open(filename, 'w') as file:
            for key, value in env.items():
                if any((all((not blacklist_mode, key in vars)), all((blacklist_mode, key not in vars)))):
                    file.write(f'{key}="{value}"\n')


class EmptyClass:
    """
    Class that returns None for any attribute access.

    Класс, возвращающий None при любом доступе к атрибутам.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass

    def __getattr__(self, key: str) -> Any:
        """Return None for any attribute access."""
        return None


class NonStrictDict(dict):
    """
    Dictionary that returns a default value for missing keys.

    Словарь, возвращающий значение по умолчанию для отсутствующих ключей.

    Args:
        seq: Initial sequence / Начальная последовательность
        default: Default value for missing keys / Значение по умолчанию
        **kwargs: Additional key-value pairs / Дополнительные пары ключ-значение
    """

    def __init__(self, seq=None, default=None, /, **kwargs):
        super().__init__(seq, **kwargs)
        self.default = default

    def __getitem__(self, item):
        """
        Get value or default if key missing.

        Получает значение или значение по умолчанию, если ключ отсутствует.

        Args:
            item: Key to access / Ключ для доступа

        Returns:
            Value or default / Значение или значение по умолчанию
        """
        try: return super().__getitem__(item)
        except KeyError: return self.default
