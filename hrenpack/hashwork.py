"""
Password hashing utilities.

Provides functions for hashing passwords with SHA algorithms and bcrypt.

Утилиты для хэширования паролей.

Предоставляет функции для хэширования паролей с помощью SHA алгоритмов и bcrypt.
"""

import hashlib, bcrypt
from typing import Literal


def hash_password(password: str, sha_alg: Literal[1, 256, 384, 512, 224] = 256) -> str:
    """
    Hash password using SHA algorithm.

    Хэширует пароль с использованием SHA алгоритма.

    Args:
        password (str): Password to hash / Пароль для хэширования
        sha_alg (Literal): SHA algorithm version: 1, 224, 256, 384, 512, default 256 / Версия SHA алгоритма

    Returns:
        str: Hashed password as hex string / Хэшированный пароль в виде hex-строки
    """

    def coding(code):
        return f'hashlib.sha{code}()'

    password_bytes = password.encode('utf-8')
    hashed = eval(coding(sha_alg))
    hashed.update(password_bytes)
    hashed_password = hashed.hexdigest()
    return hashed_password


def hash_password_bcrypt(password: str) -> str:
    """
    Hash password using bcrypt.

    Хэширует пароль с использованием bcrypt.

    Args:
        password (str): Password to hash / Пароль для хэширования

    Returns:
        str: Bcrypt hashed password / Bcrypt хэшированный пароль
    """
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def check_password_bcrypt(password: str, hashed_password: str) -> bool:
    """
    Verify password against bcrypt hash.

    Проверяет пароль на соответствие bcrypt хэшу.

    Args:
        password (str): Plain text password / Пароль в открытом виде
        hashed_password (str): Bcrypt hash to compare / Bcrypt хэш для сравнения

    Returns:
        bool: True if password matches / True если пароль совпадает
    """
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
