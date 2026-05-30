"""
File system and system command utilities.

Provides functions for file operations, path manipulation, system information,
and admin privilege handling.

Утилиты файловой системы и системных команд.

Предоставляет функции для операций с файлами, манипуляции путями,
информации о системе и обработки прав администратора.
"""

import os, ctypes, shutil, getpass, platform, random, string, subprocess
from datetime import datetime
from pathlike_typing import PathLike
from typing import Union, List
from dataclasses import dataclass
from pathlib import Path


def get_filename(path: PathLike, raise_error: bool = True) -> str:
    """
    Extract filename from a path.

    Извлекает имя файла из пути.

    Args:
        path (PathLike): Path to file / Путь к файлу
        raise_error (bool): Raise exception if file doesn't exist, default True / Выбросить исключение, если файл не существует

    Returns:
        str: Filename / Имя файла

    Raises:
        FileNotFoundError: If file doesn't exist and raise_error is True / Если файл не существует и raise_error=True
    """
    path = str(path)
    if '/' in path:
        output = path.split('/')[-1]
    elif '\\' in path:
        output = path.split('\\')[-1]
    else:
        output = path

    if not os.path.isfile(path) and raise_error:
        raise FileNotFoundError('No such file: ' + path)
    else:
        return output


def get_extension(path: PathLike, raise_error: bool = True) -> str:
    """
    Get file extension from path.

    Получает расширение файла из пути.

    Args:
        path (PathLike): Path to file / Путь к файлу
        raise_error (bool): Raise exception if file doesn't exist, default True / Выбросить исключение, если файл не существует

    Returns:
        str: File extension (without dot) / Расширение файла (без точки)
    """
    filename = get_filename(path, raise_error)
    return filename.split('.')[-1] if '.' in filename else ''


def get_path_without_filename(path: str, raise_error: bool = True):
    """
    Get directory path without filename.

    Получает путь к директории без имени файла.

    Args:
        path (str): Full file path / Полный путь к файлу
        raise_error (bool): Raise exception if file doesn't exist, default True / Выбросить исключение, если файл не существует

    Returns:
        str: Directory path / Путь к директории
    """
    path = str(path)
    if '/' in path:
        path_list = path.split('/')
        path_list.pop()
    elif '\\' in path:
        path_list = path.split('\\')
        path_list.pop()
    else:
        path_list = [path]
    output = os.path.join(*path_list)
    if not os.path.isfile(path) and raise_error:
        raise FileNotFoundError('No such file: ' + path)
    else:
        return output


def get_path_and_filename(path: str, raise_error: bool = True):
    """
    Get both directory path and filename.

    Получает путь к директории и имя файла.

    Args:
        path (str): Full file path / Полный путь к файлу
        raise_error (bool): Raise exception if file doesn't exist, default True / Выбросить исключение, если файл не существует

    Returns:
        tuple: (directory_path, filename) / (путь_к_директории, имя_файла)
    """
    if raise_error and not os.path.isfile(path):
        raise FileNotFoundError('No such file: ' + path)
    return get_path_without_filename(path), get_filename(path)


def rename(path: str, new_filename: str):
    """
    Rename a file.

    Переименовывает файл.

    Args:
        path (str): Current file path / Текущий путь к файлу
        new_filename (str): New filename / Новое имя файла
    """
    pwfn, filename = get_path_and_filename(path)
    if pwfn:
        new_path = f'{pwfn}/{new_filename}'
    else:
        new_path = new_filename
    os.rename(path, new_path)


def create_file(path: str):
    """
    Create a new empty file.

    Создает новый пустой файл.

    Args:
        path (str): Path for new file / Путь для нового файла

    Raises:
        FileExistsError: If file already exists / Если файл уже существует
    """
    try:
        open(path, 'x').close()
    except FileExistsError:
        raise FileExistsError(f'Cannot create file because it already exists: {path}')


def get_filename_without_extension(path: str, raise_error: bool = True) -> str:
    """
    Get filename without extension.

    Получает имя файла без расширения.

    Args:
        path (str): File path / Путь к файлу
        raise_error (bool): Raise exception if file doesn't exist, default True / Выбросить исключение, если файл не существует

    Returns:
        str: Filename without extension / Имя файла без расширения
    """
    filename = get_filename(path, raise_error)
    fl = filename.split('.')
    fl.pop()
    return '.'.join(fl)


def get_path_without_extension(path: str, raise_error: bool = True) -> str:
    """
    Get file path without extension.

    Получает путь к файлу без расширения.

    Args:
        path (str): File path / Путь к файлу
        raise_error (bool): Raise exception if file doesn't exist, default True / Выбросить исключение, если файл не существует

    Returns:
        str: Path without extension / Путь без расширения
    """
    filename = get_filename_without_extension(path, raise_error)
    pwfl = get_path_without_filename(path, raise_error)
    return f'{pwfl}/{filename}'


def delete_file(path: str):
    """
    Delete a file.

    Удаляет файл.

    Args:
        path (str): Path to file to delete / Путь к файлу для удаления
    """
    os.remove(path)


def create_file_exist(path: str, space: bool = True):
    """
    Create a file with automatic renaming if exists.

    Создает файл с автоматическим переименованием, если существует.

    Args:
        path (str): Desired file path / Желаемый путь к файлу
        space (bool): Add space before number, default True / Добавить пробел перед числом

    Returns:
        Optional[FileNameInfo]: File info if return_filename_and_path is True / Информация о файле
    """
    if not os.path.isfile(path):
        new_path = path
    else:
        counter = 0
        separator = ' ' if space else ''
        pafn = get_path_without_extension(path, False)
        extension = get_extension(path)
        while True:
            new_path = f'{pafn}{separator}({counter}).{extension}'
            if os.path.isfile(new_path):
                counter += 1
            else:
                break

    create_file(new_path)
    return new_path


def edit_time(year: int = -1, month: int = -1, day: int = -1, hour: int = -1, minute: int = -1,
              second: int = -1) -> None:
    """
    Edit system date and time (Windows only).

    Изменяет системную дату и время (только Windows).

    Args:
        year (int): Year, uses current if -1 / Год
        month (int): Month, uses current if -1 / Месяц
        day (int): Day, uses current if -1 / День
        hour (int): Hour, uses current if -1 / Час
        minute (int): Minute, uses current if -1 / Минута
        second (int): Second, uses current if -1 / Секунда
    """
    now = datetime.now()
    if year < 0:
        year = now.year
    if month < 0:
        month = now.month
    if day < 0:
        day = now.day
    if hour < 0:
        hour = now.hour
    if minute < 0:
        minute = now.minute
    if second < 0:
        second = now.second

    os.system(f'date {year}.{month}.{day}')
    os.system(f'time {hour}:{minute}:{second}')


def is_admin() -> bool:
    """
    Check if program is running with administrator privileges (Windows).

    Проверяет, запущена ли программа с правами администратора (Windows).

    Returns:
        bool: True if admin, False otherwise / True если администратор
    """
    return bool(ctypes.windll.shell32.IsUserAnAdmin())


def admin_error() -> None:
    """
    Raise error if not running as administrator.

    Вызывает ошибку, если программа не запущена с правами администратора.

    Raises:
        OSError: If not admin / Если не администратор
    """
    if not is_admin():
        raise OSError("Please restart the program with administrator privileges")


def admin_pause() -> None:
    """
    Print admin message and wait for input if not admin.

    Выводит сообщение об администраторе и ожидает ввод.
    """
    if not is_admin():
        print("Please restart the program with administrator privileges")
        input()


def admin_pause_exit() -> None:
    """Print admin message, wait for input, and exit."""
    admin_pause()
    exit(1)


def remove_files_and_folders(*paths):
    """
    Remove multiple files and folders.

    Удаляет несколько файлов и папок.

    Args:
        *paths: Paths to remove / Пути для удаления

    Raises:
        OSError: If deletion fails / Если удаление не удалось
    """
    for path in paths:
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                raise OSError(f"Failed to delete file {path}: {e}")
        elif os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                raise OSError(f"Failed to delete folder {path}: {e}")


def get_username() -> str:
    """
    Get current system username.

    Получает имя текущего пользователя системы.

    Returns:
        str: Username / Имя пользователя
    """
    return getpass.getuser()


def get_files_startswith(directory: str, start: str, full_path: bool = True) -> List[str]:
    """
    Get files in directory that start with a prefix.

    Получает файлы в директории, начинающиеся с префикса.

    Args:
        directory (str): Directory path / Путь к директории
        start (str): Prefix to match / Префикс для поиска
        full_path (bool): Return full paths, default True / Возвращать полные пути

    Returns:
        List[str]: List of matching files / Список подходящих файлов
    """
    files = os.listdir(directory)
    filtered_files = [f for f in files if f.startswith(start)]
    if full_path:
        output = list()
        for file in filtered_files:
            output.append(os.path.join(directory, file))
    else:
        output = filtered_files
    return output


def all_files_and_dirs(directory):
    """
    Get all files and directories recursively.

    Получает все файлы и директории рекурсивно.

    Args:
        directory: Root directory / Корневая директория

    Returns:
        list: All paths / Все пути
    """
    output = []
    for root, dirs, files in os.walk(directory):
        output.extend([os.path.join(root, name) for name in files])
        output.extend([os.path.join(root, name) for name in dirs])
    return output


def all_files(directory, full_path: bool = True) -> List[str]:
    """
    Get all files recursively.

    Получает все файлы рекурсивно.

    Args:
        directory: Root directory / Корневая директория
        full_path (bool): Return full paths, default True / Возвращать полные пути

    Returns:
        List[str]: List of file paths / Список путей к файлам
    """
    path = Path(directory)
    if not full_path:
        return [get_filename(str(file)) for file in path.rglob('*') if file.is_file()]
    return [str(file) for file in path.rglob('*') if file.is_file()]


def generate_random_filename(length: int = 10, extension: str = '') -> str:
    """
    Generate random filename.

    Генерирует случайное имя файла.

    Args:
        length (int): Length of random part, default 10 / Длина случайной части
        extension (str): File extension without dot, default empty / Расширение файла без точки

    Returns:
        str: Random filename / Случайное имя файла
    """
    letters_and_digits = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(letters_and_digits) for _ in range(length))
    if extension:
        extension = '.' + extension
    return random_name + extension


def uninstall_program(program_name):
    """
    Uninstall a program using WMIC (Windows only).

    Удаляет программу через WMIC (только Windows).

    Args:
        program_name (str): Name of program to uninstall / Имя программы для удаления
    """
    try:
        subprocess.run(['wmic', 'product', 'where', f'name="{program_name}"', 'call', 'uninstall'], check=True)
        print(f'Program "{program_name}" successfully uninstalled.')
    except subprocess.CalledProcessError as e:
        print(f'Error during uninstallation: {e}')


def admin_required(func):
    """
    Decorator that requires administrator privileges.

    Декоратор, требующий права администратора.

    Args:
        func: Function to decorate / Функция для декорирования

    Returns:
        callable: Wrapped function / Обернутая функция

    Raises:
        OSError: If not admin / Если не администратор
    """

    def wrapper(*args, **kwargs):
        if is_admin():
            return func(*args, **kwargs)
        raise OSError("Access denied")

    return wrapper


def get_max_path_length():
    """
    Get maximum path length limit for the operating system.

    Получает максимальную длину пути для операционной системы.

    Returns:
        int: Maximum path length in characters / Максимальная длина пути в символах
    """
    system = platform.system()

    # Base limits for different OS
    limits = {
        "Windows": 260,
        "Darwin": 1024,  # macOS
        "Linux": 4096
    }

    base_limit = limits.get(system, 255)

    if system == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\FileSystem"
            )
            value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
            winreg.CloseKey(key)

            if value == 1:
                return 32767
        except: pass

    return base_limit


def is_path_valid(path: PathLike) -> bool:
    """
    Validate if a path is valid for the current OS.

    Проверяет, является ли путь допустимым для текущей ОС.

    Args:
        path (PathLike): Path to validate / Путь для проверки

    Returns:
        bool: True if valid, False otherwise / True если допустим
    """
    try:
        path = Path(path)

        if len(str(path)) > get_max_path_length():
            return False

        reserved_names = {'CON', 'PRN', 'AUX', 'NUL',
                          'COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                          'COM6', 'COM7', 'COM8', 'COM9',
                          'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5',
                          'LPT6', 'LPT7', 'LPT8', 'LPT9'}

        for part in path.parts:
            name_without_ext = Path(part).stem.upper()
            if name_without_ext in reserved_names:
                return False

        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            if char in str(path):
                return False

        # Check for trailing spaces or dots
        for part in path.parts:
            if part and (part[-1] in (' ', '.')):
                return False

        return True
    except Exception:
        return False
