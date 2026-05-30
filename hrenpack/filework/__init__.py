"""
File handling utilities for various file formats.

Provides classes and functions for working with text files, SRT subtitles,
INI configuration files, JSON files, and CSV files.

Утилиты для работы с файлами различных форматов.

Предоставляет классы и функции для работы с текстовыми файлами, субтитрами SRT,
INI конфигурационными файлами, JSON файлами и CSV файлами.
"""

import os, json, csv, functools
from typing import Union, Literal, Any, List
from pathlike_typing import PathLike
from ..cmd import get_filename, get_extension, create_file
from ..listwork import list_add, keys_dict_equals
from configparser import ConfigParser, NoOptionError, NoSectionError


class FileTypeError(Exception):
    """Raised when file has incorrect extension."""
    pass


class FileIsNotEmptyError(Exception):
    """Raised when trying to write to non-empty file when empty is required."""
    pass


class FileIsEmptyError(Exception):
    """Raised when trying to read empty file when content is expected."""
    pass


def create_file_if_not_exists(path: PathLike) -> None:
    """
    Create file if it doesn't exist.

    Создает файл, если он не существует.

    Args:
        path (PathLike): File path / Путь к файлу
    """
    if not os.path.isfile(path):
        create_file(path)


def use_default(func):
    """
    Decorator that returns default value on NoOptionError or NoSectionError.

    Декоратор, возвращающий значение по умолчанию при NoOptionError или NoSectionError.

    Args:
        func: Method to decorate / Метод для декорирования

    Returns:
        callable: Wrapped method / Обернутый метод
    """
    @functools.wraps(func)
    def wrapper(self, section: str, key: str, default: Any = None):
        try:
            return func(self, section, key, default)
        except (NoOptionError, NoSectionError):
            return default
    return wrapper


class TextFile:
    """
    Base class for text file operations.

    Базовый класс для операций с текстовыми файлами.

    Args:
        path (PathLike): File path / Путь к файлу
        encoding (Union[str, int]): File encoding, default 'utf-8' / Кодировка файла
        create_file_if_not_exists (bool): Create file if missing, default True / Создать файл при отсутствии
    """
    def __init__(self, path: PathLike, encoding: Union[str, int] = 'utf-8', **kwargs):
        self.path = path
        self.get_filename = lambda: get_filename(self.path)
        self.get_extension = lambda: get_extension(self.path)
        self.encoding: str = str(encoding)
        self.search_and_delete = lambda input: self.search_and_edit(input, '')
        if kwargs.get('create_file_if_not_exists', True):
            create_file_if_not_exists(self.path)

    def read(self, letters: int = -1) -> str:
        """
        Read file content.

        Читает содержимое файла.

        Args:
            letters (int): Number of characters to read, -1 for all / Количество символов для чтения

        Returns:
            str: File content / Содержимое файла
        """
        file = open(self.path, encoding=self.encoding)
        data = file.read(letters)
        file.close()
        return data

    def rewrite(self, data: str):
        """
        Rewrite entire file with new data.

        Перезаписывает весь файл новыми данными.

        Args:
            data (str): New content / Новое содержимое
        """
        file = open(self.path, 'w', encoding=self.encoding)
        file.write(data)
        file.close()

    def add_data(self, data: str, separator: str = ''):
        """
        Append data to file.

        Добавляет данные в конец файла.

        Args:
            data (str): Data to append / Данные для добавления
            separator (str): Separator before data, default empty / Разделитель перед данными
        """
        file = open(self.path, 'a', encoding=self.encoding)
        file.write(separator)
        file.write(data)
        file.close()

    def copy(self, new_path: str, force: bool = False):
        """
        Copy file to new location.

        Копирует файл в новое место.

        Args:
            new_path (str): Destination path / Путь назначения
            force (bool): Overwrite if exists, default False / Перезаписать при существовании

        Raises:
            FileExistsError: If destination exists and force is False / Если файл существует и force=False
        """
        if os.path.isfile(new_path) and not force:
            raise FileExistsError(f'Cannot create new file because it already exists: {new_path}')
        else:
            data = self.read()
            file = open(new_path, 'w', encoding=self.encoding)
            file.write(data)
            file.close()

    def copy_and_edit_text(self, new_path: str, new_text: str):
        """
        Copy file and replace content with new text.

        Копирует файл и заменяет содержимое новым текстом.

        Args:
            new_path (str): Destination path / Путь назначения
            new_text (str): New content / Новое содержимое
        """
        self.copy(new_path)
        file = TextFile(new_path)
        file.rewrite(new_text)

    def copy_with_prefix(self, prefix_text: str, is_suffix: bool = False,
                         new_text: Union[str, bool] = False, is_return_filename: bool = False) -> str:
        """
        Copy file with prefix or suffix added to filename.

        Копирует файл с добавлением префикса или суффикса к имени.

        Args:
            prefix_text (str): Text to add / Текст для добавления
            is_suffix (bool): Add as suffix if True, default False / Добавить как суффикс
            new_text (Union[str, bool]): New content for copied file, False means keep original, default False / Новое содержимое
            is_return_filename (bool): Return new filename, default False / Вернуть новое имя файла

        Returns:
            str: New filename if is_return_filename is True / Новое имя файла
        """
        if is_suffix:
            new_filename = f'{self.path} {prefix_text}'
        else:
            new_filename = f'{prefix_text} {self.path}'

        self.copy(new_filename)

        if new_text is not False:
            copied_file = TextFile(new_filename)
            copied_file.rewrite(new_text)

        if is_return_filename:
            return new_filename

    def edit_line(self, line: int, new_data: str):
        """
        Edit specific line (line numbers start from 1).

        Редактирует определенную строку (нумерация строк с 1).

        Args:
            line (int): Line number (1-indexed) / Номер строки (с 1)
            new_data (str): New content for the line / Новое содержимое строки
        """
        lines = self.read().split('\n')
        lines[line - 1] = new_data
        self.rewrite('\n'.join(lines))

    def is_empty(self) -> bool:
        """
        Check if file is empty.

        Проверяет, пуст ли файл.

        Returns:
            bool: True if empty / True если пуст
        """
        return self.read() == ''

    def search_and_edit(self, input: str, output: str) -> None:
        """
        Search and replace text.

        Ищет и заменяет текст.

        Args:
            input (str): Text to find / Текст для поиска
            output (str): Replacement text / Текст для замены
        """
        new_text = self.read().replace(input, output)
        self.rewrite(new_text)

    def write_if_is_empty(self, data):
        """
        Write data only if file is empty.

        Записывает данные, только если файл пуст.

        Args:
            data: Data to write / Данные для записи

        Raises:
            FileIsNotEmptyError: If file is not empty / Если файл не пуст
        """
        if self.is_empty():
            self.rewrite(data)
        else:
            raise FileIsNotEmptyError("File must be empty to use this function")

    def read_lines(self, without_n: bool = True) -> Union[list[str], tuple[str]]:
        """
        Read file as list of lines.

        Читает файл как список строк.

        Args:
            without_n (bool): Remove newline characters, default True / Удалить символы новой строки

        Returns:
            Union[list[str], tuple[str]]: Lines / Строки
        """
        output = self.read().split('\n')
        if not without_n:
            for i, el in enumerate(output):
                output[i] = el + '\n'
        return output

    def newline(self, line: str):
        """
        Add new line at end of file.

        Добавляет новую строку в конец файла.

        Args:
            line (str): Line to add / Строка для добавления
        """
        if self.is_empty():
            self.rewrite(line)
        else:
            self.rewrite(f'{self.read()}\n{line}')

    def __str__(self):
        return self.read()

    def __bool__(self):
        """True if file is empty (opposite of typical)."""
        return self.is_empty()

    def open(self,
             mode: Literal[
                 "r+", "+r", "rt+", "r+t", "+rt", "tr+", "t+r", "+tr", "w+", "+w", "wt+", "w+t", "+wt", "tw+", "t+w", "+tw",
                 "a+", "+a", "at+", "a+t", "+at", "ta+", "t+a", "+ta", "x+", "+x", "xt+", "x+t", "+xt", "tx+", "t+x", "+tx",
                 "w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx", "r", "rt", "tr", "U", "rU", "Ur", "rtU", "rUt", "Urt",
                 "trU", "tUr", "Utr"] = "r",
             buffering: int = -1,
             errors: str | None = None,
             newline: str | None = None,
             closefd: bool = True):
        """
        Open file with Python's built-in open().

        Открывает файл с помощью встроенной функции open().

        Args:
            mode: File open mode / Режим открытия
            buffering: Buffering policy / Политика буферизации
            errors: Error handling / Обработка ошибок
            newline: Newline handling / Обработка новых строк
            closefd: Close file descriptor / Закрыть дескриптор

        Returns:
            file: Opened file object / Открытый файловый объект
        """
        return open(self.path, mode, buffering, self.encoding, errors, newline, closefd)


class SRTSubtitleFile(TextFile):
    """
    SRT subtitle file handler.

    Обработчик файлов субтитров SRT.

    Important: SRT file must follow proper format - single newline between different data types,
    double newline between sections.

    Важно: Файл SRT должен быть написан по правилам - один переход на новую строку между разными типами данных,
    два перехода на новую строку между секциями.

    Args:
        path (str): Path to SRT file / Путь к SRT файлу
        encoding (Union[str, int]): File encoding, default 'utf-8' / Кодировка файла
    """

    class SubtitleError(Exception):
        """Raised for invalid subtitle format."""
        pass

    def __init__(self, path: str, encoding: Union[str, int] = 'utf-8'):
        super().__init__(path, encoding)
        subtitle_data = self.read_subtitle()
        self.subtitles_timecodes = subtitle_data['timecodes']
        self.subtitles_text = subtitle_data['text']
        self.sections = subtitle_data['number']
        self.edit, self.elst, self.edit_subtitle = [self.edit_line_subtitle_text] * 3

    def read_subtitle(self) -> dict:
        """
        Parse subtitle file into structured data.

        Разбирает файл субтитров в структурированные данные.

        Returns:
            dict: Dictionary with 'timecodes', 'text', and 'number' keys / Словарь с ключами

        Raises:
            SubtitleError: If file format is invalid / Если формат файла неверный
        """
        try:
            sections = self.read().split('\n\n')
            timecodes, text_data = [[]] * 2
            for section in sections:
                if not section.strip():
                    continue
                parts = section.split('\n')
                if len(parts) >= 3:
                    number, timecode, text = parts[0], parts[1], '\n'.join(parts[2:])
                    timecodes.append(timecode)
                    text_data.append(text)
            return {'timecodes': timecodes, 'text': text_data, 'number': len(sections)}
        except ValueError:
            if not self.is_empty():
                raise self.SubtitleError("Invalid subtitle file format. This library cannot process it.")

    def edit_line_subtitle_text(self, line: int, new_text: str):
        """
        Edit subtitle text at specified line (1-indexed).

        Редактирует текст субтитра на указанной строке (с 1).

        Args:
            line (int): Subtitle number / Номер субтитра
            new_text (str): New text / Новый текст
        """
        text_line = line * 4 - 1
        self.edit_line(text_line, new_text)

    def edit_timecode(self, line: int, new_timecode_begin: str, new_timecode_end: str):
        """
        Edit timecode at specified line.

        Редактирует таймкод на указанной строке.

        Args:
            line (int): Subtitle number / Номер субтитра
            new_timecode_begin (str): Start time (e.g., "00:00:01,000") / Время начала
            new_timecode_end (str): End time (e.g., "00:00:02,000") / Время окончания
        """
        text_line = line * 4 - 2
        self.edit_line(text_line, f'{new_timecode_begin} --> {new_timecode_end}')


class ConfigurationFile(TextFile):
    """
    INI configuration file handler.

    Обработчик INI конфигурационных файлов.

    Args:
        path (str): Path to INI file, default 'config.ini' / Путь к INI файлу
        encoding (Union[str, int]): File encoding, default 'utf-8' / Кодировка файла
    """
    class _Section:
        """Dictionary-like section wrapper."""
        def __init__(self, config: ConfigParser, name: str):
            self.config = dict(config.items(name))

        def __getitem__(self, key: str):
            return self.config[key]

        def __setitem__(self, key: str, value: str):
            self.config[key] = value

        def get(self, key: str, default=None):
            return self.config.get(key, default)

    def __init__(self, path: str = 'config.ini', encoding: Union[str, int] = 'utf-8'):
        super().__init__(path, encoding)
        self.config = ConfigParser()
        self.read_config = lambda: self.config.read(self.path, encoding=self.encoding)
        self.read_config()
        self.get_bool = self.get_boolean

    @use_default
    def get_value(self, section: str, key: str, default: Any = None) -> str:
        """Get string value from config."""
        return self.config.get(section, key)

    @use_default
    def get_boolean(self, section: str, key: str, default: Any = False) -> bool:
        """Get boolean value from config."""
        return self.config.getboolean(section, key)

    @use_default
    def get_int(self, section: str, key: str, default: Any = 0) -> int:
        """Get integer value from config."""
        return self.config.getint(section, key)

    @use_default
    def get_float(self, section: str, key: str, default: Any = 0) -> float:
        """Get float value from config."""
        return self.config.getfloat(section, key)

    def set_value(self, section: str, key: str, value) -> None:
        """Set value in config and save."""
        self.config.set(section, key, str(value))
        self.save()

    def save(self):
        """Save config to file."""
        with open(self.path, 'w', encoding=self.encoding) as config:
            self.config.write(config)

    def section_exists(self, section: str) -> bool:
        """Check if section exists."""
        return section in self.config.sections()

    def value_exists(self, section: str, key: str) -> bool:
        """Check if key exists in section."""
        return self.config.has_option(section, key)

    def delete_value(self, section: str, key: str) -> None:
        """Delete key from section."""
        self.config.remove_option(section, key)
        self.save()

    def delete_section(self, section: str) -> None:
        """Delete entire section."""
        self.config.remove_section(section)
        self.save()

    def create_section(self, section: str) -> None:
        """Create new section."""
        self.config.add_section(section)
        self.save()

    def create_key_in_section(self, section: str, key: str, value) -> None:
        """Create key in section, creating section if needed."""
        if not self.value_exists(section, key):
            if not self.section_exists(section):
                self.create_section(section)
                self.config.set(section, key, str(value))
                self.save()
            else:
                self.config.set(section, key, str(value))
                self.save()
        else:
            if value != self.get_value(section, key):
                self.set_value(section, key, str(value))

    def add_comment(self, line_index: int, text: str, comment_letter: Literal[';', '#'] = ';'):
        """Add comment line at specified index."""
        lines = self.read_lines()
        lines = list_add(lines, line_index, ' '.join((comment_letter, text)))
        self.rewrite('\n'.join(lines))

    def edit_section(self, section: str, block: dict, rewrite: bool = False) -> None:
        """Edit entire section with dictionary."""
        if rewrite:
            try:
                self.delete_section(section)
            except NoSectionError:
                pass
            self.create_section(section)
        for key in block:
            self.set_value(section, key, block[key])

    def rewrite(self, data: str):
        """Rewrite file and reload config."""
        with open(self.path, 'w', encoding=self.encoding) as file:
            file.write(data)
            self.read_config()

    def set_bool(self, section: str, key: str, value):
        """Set boolean value."""
        self.set_value(section, key, bool(value))

    def set_int(self, section: str, key: str, value):
        """Set integer value."""
        self.set_value(section, key, int(value))

    def get_section(self, section: str, is_dict: bool = True) -> Union[list[tuple[str, str]], dict]:
        """Get all key-value pairs from section."""
        output = self.config.items(section)
        if is_dict:
            pre_output = dict()
            for el in output:
                pre_output[el[0]] = el[1]
            output = pre_output
        return output

    def edit(self, block: dict[str, dict[str, Any]], rewrite: bool = False) -> None:
        """Edit multiple sections at once."""
        if rewrite:
            config = ConfigParser()
            for section, options in block.items():
                config[section] = options
            with open(self.path, 'w') as configfile:
                config.write(configfile)
        else:
            for section, options in block.items():
                self.edit_section(section, options)

    def __getitem__(self, section):
        """Get section as dictionary."""
        return self._Section(self.config, section)


class JavaScriptObjectNotationFile(TextFile):
    """
    JSON file handler.

    Обработчик JSON файлов.

    Args:
        path (str): Path to JSON file / Путь к JSON файлу
        encoding (Union[str, int]): File encoding, default 'utf-8' / Кодировка файла
    """
    class JSONError(Exception):
        """Raised for JSON-specific errors."""
        pass

    def __init__(self, path: str, encoding: Union[str, int] = 'utf-8'):
        super().__init__(path, encoding)
        self.data = json.loads(self.read())

    def __dict__(self):
        return self.data

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(self.data)

    def save(self):
        """Save data to file."""
        with open(self.path, 'w', encoding=self.encoding) as file:
            json.dump(self.data, file, indent=4, ensure_ascii=self.encoding == 'ascii')

    def get_value(self, key, default=KeyError()):
        """Get value by key."""
        try:
            if type(default) is KeyError:
                raise default
            return self.data.get(key, default)
        except KeyError:
            raise self.JSONError(f"Key '{key}' does not exist in {get_filename(self.path)}")

    def set_value(self, key, value):
        """Set value by key."""
        self.data[key] = value
        self.save()

    def delete_value(self, key):
        """Delete key."""
        del self.data[key]
        self.save()

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        del self.data[key]
        self.save()

    def __iter__(self):
        return iter(self.data)

    def set_values(self, **values):
        """Set multiple values."""
        for key, value in values.items():
            self.data[key] = value
        self.save()

    def get_values(self, *keys):
        """Get multiple values."""
        output = dict()
        for key in keys:
            output[key] = self.get_value(key)
        return output

    def key_exists(self, key) -> bool:
        """Check if key exists."""
        return key in self.data

    def add_dict(self, data: dict):
        """Add dictionary data."""
        self.set_values(**data)

    def clear(self):
        """Clear all data."""
        self.data.clear()
        self.save()

    def rewrite_dict(self, data: dict):
        """Replace entire data with new dictionary."""
        self.clear()
        self.add_dict(data)

    def rewrite_values(self, **values):
        """Replace entire data with keyword arguments."""
        self.rewrite_dict(values)

    def __str__(self):
        return str(self.data)

    def read_data(self):
        """Get raw data."""
        return self.data


def write_file_if_not_exists(path: str, text: str = ''):
    """
    Create file with content only if it doesn't exist.

    Создает файл с содержимым, только если он не существует.

    Args:
        path (str): File path / Путь к файлу
        text (str): Content to write / Содержимое для записи

    Raises:
        FileExistsError: If file already exists / Если файл уже существует
    """
    if os.path.isfile(path):
        raise FileExistsError(f'Cannot create new file because it already exists: {path}')
    else:
        create_file(path)
        file = TextFile(path)
        file.rewrite(text)


class CommaSeparatedValuesFile(TextFile):
    """
    CSV file handler.

    Обработчик CSV файлов.

    Args:
        path (str): Path to CSV file / Путь к CSV файлу
        encoding (Union[str, int]): File encoding, default 'utf-8' / Кодировка файла
    """
    def __init__(self, path: str, encoding: Union[str, int] = 'utf-8'):
        super().__init__(path, encoding)

    def read_data(self):
        """Read CSV data as list of dictionaries."""
        with self.open() as file:
            return list(csv.DictReader(file))

    @staticmethod
    def __equals_keys(dicts: list[dict]) -> tuple:
        if keys_dict_equals(*dicts):
            return tuple(dicts[0].keys())

    def write_data(self, data: List[dict[str, Any]]):
        """
        Write data to CSV file.

        Args:
            data (List[dict[str, Any]]): List of dictionaries with same keys / Список словарей с одинаковыми ключами

        Raises:
            ValueError: If dictionaries have different keys / Если словари имеют разные ключи
        """
        with self.open('w', newline='') as file:
            fields = self.__equals_keys(data)
            if fields is None:
                raise ValueError("Data dictionaries must have the same keys")
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
