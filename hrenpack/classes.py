import platform, os
import warnings
from typing import Any, IO, Optional
from dotenv import load_dotenv, dotenv_values
from pathlike_typing import PathLike
from hrenpack.boolwork import str_to_bool
from hrenpack.listwork import if_dict_key, dict_keyf, merging_dictionaries


class DictObject:
    def __init__(self, dictionary: dict, recursive: bool = False):
        for key, value in dictionary.items():
            if isinstance(value, dict) and recursive:
                # Рекурсивно преобразуем вложенные словари
                setattr(self, key, DictObject(value))
            elif isinstance(value, list) and recursive:
                # Обрабатываем списки с возможными вложенными словарями
                setattr(self, key, [
                    DictObject(item) if isinstance(item, dict) else item
                    for item in value
                ])
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"<DictObject: {self.__dict__}>"


def call_method(method_name: str, objects: tuple, *args, **kwargs):
    for obj in objects:
        getattr(obj, method_name)(*args, **kwargs)


if platform.system() == 'Windows':
    try:
        from tkinter import Tk

        class TkTemplate(Tk):
            def __init__(self, title: str, width: int, height: int, background: str = 'white', resizable: bool = False, **kwargs):
                super().__init__()
                self.title(title)
                self.resizable(resizable, resizable)
                self.geometry(f'{width}x{height}')
                self['bg'] = background
                if if_dict_key(kwargs, 'icon'):
                    self.iconbitmap(kwargs['icon'])
                self.stylesheet = dict_keyf(kwargs, 'stylesheet', dict())
                self.__stylesheet__()
                self.widgets_init()

            def widgets_init(self):
                pass

            def __stylesheet__(self):
                self.stylesheet_class = DictObject(self.stylesheet)
    except (ModuleNotFoundError, ImportError):
        class TkTemplate:
            def __new__(cls, *args, **kwargs):
                raise OSError("No module named 'tkinter'")

            def __init__(self, *args, **kwargs):
                raise OSError("No module named 'tkinter'")
else:
    class TkTemplate:
        def __new__(cls, *args, **kwargs):
            raise OSError('This class is only supported on Windows')

        def __init__(self, *args, **kwargs):
            raise OSError('This class is only supported on Windows')


class Class:
    """Обычный пустой класс"""


class range_plus:
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
                    raise ValueError("Максимум 3 аргумента")
        else:
            raise ValueError("Нужен хотя бы 1 аргумент")
        self.range = range(*new_args)

    def __iter__(self):
        return iter(self.range)

    def __str__(self):
        return str(self.range)


class RawString(str):
    def __add__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return RawString(super().__add__(other))

    def __radd__(self, other):
        return RawString(str(other) + str(self))  # Гарантированно работает для любых типов

    def convert(self):
        return str(self)

    def __eq__(self, other):
        return other == self or str(other) == str(self)


class frozendict(dict):
    def __setitem__(self, key, value):
        raise TypeError(f"'{self.__class__.__name__}' object does not support item assignment")

    def __delitem__(self, key):
        raise TypeError(f"'{self.__class__.__name__}' object does not support item deletion")


class TransposedList:
    def __init__(self, data):
        self._validate_data(data)
        self._data = data

    def _validate_data(self, data):
        try:
            iter(data)  # Проверяем, что объект итерируемый
            if not data:
                return  # Пустые данные допустимы

            # Проверяем, что все вложенные элементы имеют одинаковую длину
            first_len = len(data[0]) if hasattr(data[0], '__len__') else len(list(data[0]))
            for item in data:
                current_len = len(item) if hasattr(item, '__len__') else len(list(item))
                if current_len != first_len:
                    raise ValueError("All sub-iterables must have the same length")
        except TypeError as e:
            raise TypeError("Input data must be iterable") from e
        except IndexError as e:
            raise ValueError("Input data cannot be empty") from e

    def raw(self):
        return list(self._data) if not hasattr(self._data, '__len__') else self._data

    def __len__(self):
        if not self._data:
            return 0
        first_item = self._data[0]
        return len(first_item) if hasattr(first_item, '__len__') else len(list(first_item))

    def __iter__(self):
        # Если данные пустые, возвращаем пустой итератор
        if not self._data:
            return iter([])

        # Создаем итераторы для всех вложенных последовательностей
        iterators = [iter(subseq) for subseq in self._data]

        # Генерируем транспонированные строки
        while True:
            try:
                # Собираем элементы из каждого итератора
                yield [next(it) for it in iterators]
            except StopIteration:
                break

    def __getitem__(self, index):
        try:
            # Проверяем, что индекс допустим
            if not isinstance(index, (int, slice)):
                raise TypeError("Index must be integer or slice")

            # Если данные пустые, вызываем исключение
            if not self._data:
                raise IndexError("Index out of range")

            # Получаем длину первой подпоследовательности
            first_len = len(self._data[0]) if hasattr(self._data[0], '__len__') else len(list(self._data[0]))

            # Обработка целочисленного индекса
            if isinstance(index, int):
                if index < -first_len or index >= first_len:
                    raise IndexError("Index out of range")

                # Возвращаем транспонированную строку
                return [subseq[index] if hasattr(subseq, '__getitem__') else list(subseq)[index]
                        for subseq in self._data]

            # Обработка слайса
            else:
                # Преобразуем в список, чтобы можно было делать несколько итераций
                data_list = list(self._data)
                # Получаем транспонированный список
                transposed = list(zip(*data_list))
                # Применяем слайс
                sliced = transposed[index]
                # Преобразуем обратно в список списков (а не кортежей)
                return [list(row) for row in sliced]

        except (IndexError, TypeError) as e:
            raise type(e)(f"Failed to get item at index {index}: {str(e)}") from e

    def __setitem__(self, index, value):
        try:
            # Проверяем, что индекс допустим
            if not isinstance(index, int):
                raise TypeError("Index must be integer for assignment")

            # Проверяем, что данные не пустые
            if not self._data:
                raise IndexError("Cannot assign to empty transposed sequence")

            # Проверяем, что значение имеет правильную длину
            if len(value) != len(self._data):
                raise ValueError(f"Value must have length {len(self._data)}")

            # Устанавливаем значения в исходные последовательности
            for i, subseq in enumerate(self._data):
                # Проверяем, поддерживает ли подпоследовательность присваивание
                if hasattr(subseq, '__setitem__'):
                    subseq[index] = value[i]
                else:
                    raise TypeError(f"Subsequence at position {i} does not support item assignment")

        except (IndexError, TypeError, ValueError) as e:
            raise type(e)(f"Failed to set item at index {index}: {str(e)}") from e

    def __delitem__(self, index):
        try:
            # Проверяем, что индекс допустим
            if not isinstance(index, int):
                raise TypeError("Index must be integer for deletion")

            # Проверяем, что данные не пустые
            if not self._data:
                raise IndexError("Cannot delete from empty transposed sequence")

            # Удаляем элементы из исходных последовательностей
            for subseq in self._data:
                # Проверяем, поддерживает ли подпоследовательность удаление
                if hasattr(subseq, '__delitem__'):
                    del subseq[index]
                else:
                    raise TypeError("Subsequence does not support item deletion")

        except (IndexError, TypeError) as e:
            raise type(e)(f"Failed to delete item at index {index}: {str(e)}") from e

    def __repr__(self):
        return f"TransposedList({self._data})"

    def __str__(self):
        transposed = list(self)
        return str(transposed)


class Environment:

    def __init__(self, **local_data):
        self.local_data = self._format_dict(local_data)

    @staticmethod
    def _format_dict(*dicts: dict, **kwargs) -> dict:
        output = dict()
        for key, value in merging_dictionaries(*dicts, kwargs).items():
            if not isinstance(key, str):
                raise TypeError("Key must be str")
            output[key.upper()] = value
        return output

    @classmethod
    def load(cls, dotenv_path: PathLike = None, stream: Optional[IO[str]] = None, verbose: bool = False,
             override: bool = False, interpolate: bool = True, encoding: str = 'utf-8',
             local: bool = False) -> 'Environment':
        dotenv_func = dotenv_values if local else load_dotenv
        raw_data = dotenv_func(dotenv_path, stream, verbose, override, interpolate, encoding)
        data = dict(raw_data) if local else dict()
        return cls(**data)

    def __getitem__(self, key: str):
        if key in self.local_data:
            return self.local_data[key]
        return os.environ[key]

    def __setitem__(self, key: str, value: Any):
        os.environ[key.upper()] = str(value)

    def __delitem__(self, key):
        if key in self.local_data:
            del self.local_data[key]
        del os.environ[key]

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def get_int(self, key: str, default: Optional[int] = None, strict: bool = True) -> Optional[int]:
        try:
            return int(self.get(key, default))
        except (TypeError, ValueError) as error:
            if strict:
                raise error
            return default

    def get_float(self, key: str, default: Optional[float] = None, strict: bool = True) -> Optional[float]:
        try:
            return float(self.get(key, default))
        except (TypeError, ValueError) as error:
            if strict:
                raise error
            return default

    def get_bool(self, key: str, default: Optional[bool] = None, strict: bool = True) -> Optional[bool]:
        try:
            value = (self.get(key, default)
                     if not isinstance(self, type)
                     else os.environ.get(key.upper(), default))
            return str_to_bool(value) if value is not None else default
        except (TypeError, ValueError) as error:
            if strict:
                raise error
            return default

    def set(self, key: str, value: Any, local: bool = False) -> None:
        if not local: self[key] = value
        else: self.local_data[key.upper()] = value

    def setdefault(self, key: str, value: Any, local: bool = False, local_global: bool = False) -> None:
        if not local:
            if local_global:
                warnings.warn('The local_global argument will not apply because local=False', UserWarning, 2)
            if self.get(key) is None:
                self.set(key, value)
        else:
            if key in self: return
            self.local_data.setdefault(key.upper(), value)

    def write_local(self, delete: bool = False) -> 'Environment':
        for key, value in self.local_data.items():
            os.environ[key] = str(value)
        if delete:
            self.local_data = dict()
        return self

    def update(self, *dicts, **kwargs) -> 'Environment':
        for key, value in self._format_dict(*dicts, **kwargs).items():
            self[key] = value
        return self

    def update_local(self, *dicts, **kwargs) -> 'Environment':
        self.local_data.update(self._format_dict(*dicts, **kwargs))
        return self

    def delete(self, *keys: str) -> 'Environment':
        for key in keys:
            try:
                del self[key]
            except KeyError:
                pass
        return self

    def __iter__(self):
        return iter(merging_dictionaries(dict(os.environ), self.local_data))

    def write_file(self, filename: PathLike = '.env', *vars: str, local: bool = False,
                   global_: bool = True, blacklist_mode: bool = False) -> None:
        global_env = dict(os.environ)
        if global_ and local:
            env = merging_dictionaries(global_env, self.local_data)
        elif global_:
            env = self.local_data
        elif local:
            env = global_env
        else:
            raise ValueError()
        with open(filename, 'w') as file:
            for key, value in env.items():
                if any((all((not blacklist_mode, key in vars)), all((blacklist_mode, key not in vars)))):
                    file.write(f'{key}="{value}"\n')

