"""
Django framework DB utilities.

Provides helper functions for Django development including database configuration
from .env files and view context utilities.

Утилиты для БД фреймворка Django.

Предоставляет вспомогательные функции для разработки на Django, включая
конфигурацию базы данных из .env файлов и утилиты контекста представлений.
"""

from typing import Optional
from dotenv import dotenv_values


def dotenv_to_db(driver: str, env_path: Optional[str] = None) -> dict:
    """
    Convert .env file to Django database configuration dictionary.

    Преобразует .env файл в словарь конфигурации базы данных Django.

    Args:
        driver (str): Database driver (e.g., 'django.db.backends.postgresql') / Драйвер базы данных
        env_path (Optional[str]): Path to .env file / Путь к .env файлу

    Returns:
        dict: Database configuration dictionary / Словарь конфигурации базы данных

    Example:
        >>> dotenv_to_db('django.db.backends.postgresql')
        {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydb',
            'USER': 'user',
            'PASSWORD': 'pass',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    """
    env = dotenv_values(env_path)
    return dict(
        ENGINE=driver,
        NAME=env['DB_NAME'],
        USER=env['DB_USER'],
        PASSWORD=env['DB_PASSWORD'],
        HOST=env['DB_HOST'],
        PORT=env['DB_PORT']
    )
