import platform
from hrenpack import ThemeType

if platform.system() == 'Windows':
    import winreg


    class RegistryError(Exception):
        pass


    def remove_registry_keys(hive: str, *keys):
        for key in keys:
            try:
                hive = eval(f'winreg.{hive}')
                subkey = key
                winreg.DeleteKey(hive, subkey)
                print(f"Удален ключ реестра: {key}")
            except OSError as e:
                raise RegistryError(f"Не удалось удалить ключ реестра {key}: {e}")


    def remove_registry_values(hive, subkey, *value_names):
        try:
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                for value_name in value_names:
                    try:
                        winreg.DeleteValue(reg_key, value_name)
                    except FileNotFoundError:
                        raise FileNotFoundError(f"Значение {value_name} не найдено в {subkey}")
                    except Exception as e:
                        raise RegistryError(f"Ошибка при удалении {value_name}: {e}")
        except PermissionError:
            raise OSError("Ошибка: Не хватает прав для удаления значений.")
        except Exception as e:
            raise RegistryError(f"Ошибка: {e}")


    def remove_values_in_keys(hive, **value_names):
        """Указывайте значения через **kwargs: ключ=(значение1, значение2) или
        введите _d_i_c_t_={ключ: (значение1, значение2)}"""
        if '_d_i_c_t_' in value_names:
            value_names = value_names['_d_i_c_t_']
        for key in value_names:
            values = value_names[key]
            remove_registry_values(hive, key, *values)


    def get_windows_theme() -> ThemeType:
        """
        Определяет тему Windows (светлая/темная)
        Возвращает: 'dark' или 'light'
        """
        try:
            # Путь к настройкам персонализации в реестре
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key_name = "AppsUseLightTheme"  # 0 - темная, 1 - светлая

            # Открываем ключ реестра
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_READ
            )

            # Читаем значение
            value, _ = winreg.QueryValueEx(key, key_name)
            winreg.CloseKey(key)

            return 'light' if value == 1 else 'dark'

        except Exception as e:
            print(f"Ошибка при чтении реестра: {e}")
            return 'light'


    def get_system_theme():
        """
        Определяет системную тему Windows
        Возвращает: 'dark' или 'light'
        """
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key_name = "SystemUsesLightTheme"  # Системная тема

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
            # Если не нашли системную тему, используем тему приложений
            return get_windows_theme()
else:
    raise ImportError('windows_registry is only supported on Windows')
