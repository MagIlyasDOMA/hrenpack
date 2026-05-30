"""
Screen resolution utilities for multi-monitor setups.

Provides functions to get monitor information, resolution, and refresh rate.

Утилиты для работы с разрешением экрана в многомониторных конфигурациях.

Предоставляет функции для получения информации о мониторах, разрешении и частоте обновления.
"""

import platform
from typing import Union
from screeninfo import get_monitors


class ResolutionNotFoundError(Exception):
    """Exception raised when resolution is not found in mapping."""
    pass


def get_monitor_info(monitor: int = 0):
    """
    Get information about a specific monitor.

    Получает информацию о конкретном мониторе.

    Args:
        monitor (int): Monitor index, default 0 / Индекс монитора

    Returns:
        Monitor: Monitor object / Объект монитора
    """
    return get_monitors()[monitor]


def get_primary_monitor_info():
    """
    Get information about the primary monitor.

    Получает информацию о главном мониторе.

    Returns:
        Monitor: Primary monitor object / Объект главного монитора
    """
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor


def get_resolution(monitor: int = 0, letter: str = '') -> Union[tuple[int, int], str]:
    """
    Get resolution of specified monitor.

    Получает разрешение указанного монитора.

    Args:
        monitor (int): Monitor index, default 0 / Индекс монитора
        letter (str): Separator between width and height, default '' / Разделитель между шириной и высотой

    Returns:
        Union[tuple[int, int], str]: Resolution as tuple or string / Разрешение в виде кортежа или строки
    """
    monitor_info = get_monitor_info(monitor)
    width, height = monitor_info.width, monitor_info.height
    return (width, height) if letter == '' else f'{width}{letter}{height}'


def resolution_function(**resolutions):
    """
    Execute function based on current screen resolution.

    Выполняет функцию в зависимости от текущего разрешения экрана.

    Args:
        **resolutions: Keyword args with pattern 'r{width}x{height}' or 'default' / Аргументы с шаблоном

    Raises:
        ResolutionNotFoundError: If resolution not found and no default / Если разрешение не найдено и нет default
    """
    resolution = get_resolution(letter='x')
    rr = 'r' + resolution
    if rr in resolutions:
        resolutions[rr]()
    elif 'default' in resolutions:
        resolutions['default']()
    else:
        raise ResolutionNotFoundError('Your resolution is not in the list')


def resolution_return(**resolutions):
    """
    Return value based on current screen resolution.

    Возвращает значение в зависимости от текущего разрешения экрана.

    Args:
        **resolutions: Keyword args with pattern 'r{width}x{height}' or 'default' / Аргументы с шаблоном

    Returns:
        Value for current resolution / Значение для текущего разрешения

    Raises:
        ResolutionNotFoundError: If resolution not found and no default / Если разрешение не найдено и нет default
    """
    resolution = get_resolution(letter='x')
    rr = 'r' + resolution
    if rr in resolutions:
        return resolutions[rr]
    elif 'default' in resolutions:
        return resolutions['default']
    else:
        raise ResolutionNotFoundError('Your resolution is not in the list')


def get_refresh_rate():
    """
    Get monitor refresh rate (Windows only).

    Получает частоту обновления монитора (только Windows).

    Returns:
        int: Refresh rate in Hz / Частота обновления в Гц

    Raises:
        OSError: If not on Windows / Если не Windows
    """
    if platform.system() == 'Windows':
        import win32api
        import win32con
        return win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS).DisplayFrequency
    else:
        raise OSError("This function only works on Windows")
