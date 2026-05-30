"""
Internationalization utilities for detecting system language.

Provides function to get system language from environment variables or OS settings.

Утилиты интернационализации для определения системного языка.

Предоставляет функцию получения системного языка из переменных окружения или настроек ОС.
"""

import os, sys, locale


def get_system_language() -> str:
    """
    Detect the system's default language.

    Определяет системный язык по умолчанию.

    Checks in order: LANG environment variable, Windows UI language,
    system locale, defaults to 'en'.

    Проверяет в порядке: переменная окружения LANG, язык интерфейса Windows,
    системная локаль, по умолчанию 'en'.

    Returns:
        str: Language code (e.g., 'en', 'ru') / Код языка
    """
    env_lang = os.environ.get('LANG') or os.environ.get('LANGUAGE')
    sys_lang = None
    default_lang = None

    if sys.platform == 'win32':
        try:
            import ctypes
            windll = ctypes.windll.kernel32
            sys_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()].split('_')[0]
        except:
            pass

    try:
        default_lang = locale.getdefaultlocale()[0].split('_')[0]
    except:
        pass

    return env_lang or sys_lang or default_lang or 'en'
