import platform
from hrenpack import ThemeType
from typing import Union

if platform.system() != 'Windows':
    raise OSError('hrenpack.windows_registry supports only Windows')

import winreg


class RegistryError(Exception): pass


class UnknownHive(RegistryError): pass


class RegistryManager:
    def __init__(self):
        pass

    @staticmethod
    def parse_full_path(full_path: str) -> tuple[Union[winreg.HKEYType, int], str]:
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
        if hive not in hives: raise UnknownHive(hive)
        return hives[hive], path

    def rmkey(self, path: str):
        hive, path = self.parse_full_path(path)

    def rmtree(self, path: str):
        hive, path = self.parse_full_path(path)


def get_windows_theme() -> ThemeType:
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

    except Exception as e:
        return 'light'


def get_system_theme():
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
