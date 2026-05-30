"""
Windows Registry utilities (Windows only).

Provides functions and classes for working with Windows Registry,
including theme detection.

Утилиты для работы с реестром Windows (только Windows).

Предоставляет функции и классы для работы с реестром Windows,
включая определение темы оформления.
"""

import platform
from hrenpack import ThemeType
from typing import Union

if platform.system() != 'Windows':
    raise OSError('hrenpack.windows_registry supports only Windows')

import winreg


class RegistryError(Exception):
    """Base exception for registry-related errors."""
    pass


class UnknownHive(RegistryError):
    """Exception raised when registry hive is unknown."""
    pass


class RegistryManager:
    """
    Manager for Windows Registry operations.

    Менеджер для операций с реестром Windows.
    """

    def __init__(self):
        pass

    @staticmethod
    def parse_full_path(full_path: str) -> tuple[Union[winreg.HKEYType, int], str]:
        """
        Parse full registry path into hive and subkey path.

        Разбирает полный путь реестра на раздел и путь подключа.

        Args:
            full_path (str): Full registry path (e.g., "HKEY_CURRENT_USER\\Software\\...")

        Returns:
            tuple: (hive_handle, subkey_path) / (дескриптор_раздела, путь_подключа)

        Raises:
            UnknownHive: If hive is not recognized / Если раздел не распознан
        """
        hives = {
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKCR": winreg.HKEY_CLASSES_ROOT,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKU": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
            "HKCC": winreg.HKEY_CURRENT_CONFIG,
        }
        hive, path = full_path.split('\\', 1)
        if hive not in hives:
            raise UnknownHive(f"Unknown registry hive: {hive}")
        return hives[hive], path

    def rmkey(self, path: str):
        """
        Remove a registry key.

        Удаляет ключ реестра.

        Args:
            path (str): Full registry path / Полный путь в реестре
        """
        hive, path = self.parse_full_path(path)

    def rmtree(self, path: str):
        """
        Remove a registry key and all subkeys.

        Удаляет ключ реестра и все подразделы.

        Args:
            path (str): Full registry path / Полный путь в реестре
        """
        hive, path = self.parse_full_path(path)


def get_windows_theme() -> ThemeType:
    """
    Get Windows theme (light/dark) for apps.

    Получает тему Windows (светлая/темная) для приложений.

    Returns:
        ThemeType: 'light' or 'dark' / 'light' или 'dark'
    """
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key_name = "AppsUseLightTheme"

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_READ
        )

        value, _ = winreg.QueryValueEx(key, key_name)
        winreg.CloseKey(key)

        return 'light' if value == 1 else 'dark'

    except Exception:
        return 'light'


def get_system_theme():
    """
    Get Windows system theme (light/dark) for UI elements.

    Получает системную тему Windows (светлая/темная) для элементов интерфейса.

    Returns:
        ThemeType: 'light' or 'dark' / 'light' или 'dark'
    """
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key_name = "SystemUsesLightTheme"

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_READ
        )

        value, _ = winreg.QueryValueEx(key, key_name)
        winreg.CloseKey(key)

        return 'light' if value == 1 else 'dark'

    except Exception:
        return get_windows_theme()
