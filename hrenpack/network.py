"""
Network utilities for HTTP requests and connectivity testing.

Provides functions for checking internet connection, downloading files,
and working with ReCaptcha.

Утилиты сети для HTTP запросов и тестирования подключения.

Предоставляет функции для проверки интернет-соединения, загрузки файлов
и работы с ReCaptcha.
"""

import os, tempfile, uuid, requests
from urllib.parse import urlencode
from pathlike_typing import PathLike
from tqdm import tqdm
from hrenpack import NullStr


class NetworkError(Exception):
    """Exception raised for network-related errors."""
    pass


def connection_check():
    """
    Check internet connection by requesting Google.

    Проверяет интернет-соединение запросом к Google.

    Returns:
        bool: True if connected / True если подключение есть

    Raises:
        NetworkError: If no connection / Если нет подключения
    """
    error = NetworkError("No internet connection")
    try:
        response = requests.get("https://google.com", timeout=5)
        if response.status_code != 200:
            raise error
        return True
    except requests.ConnectionError:
        raise error


def is_connected() -> bool:
    """
    Check internet connection without raising exceptions.

    Проверяет интернет-соединение без выбрасывания исключений.

    Returns:
        bool: True if connected / True если подключение есть
    """
    try:
        connection_check()
    except NetworkError:
        return False
    else:
        return True


def connect_to_site(url: str, **kwargs) -> bool:
    """
    Test if a specific site is reachable.

    Проверяет, доступен ли конкретный сайт.

    Args:
        url (str): URL to test / URL для проверки
        **kwargs: Additional arguments for requests.get / Дополнительные аргументы для requests.get

    Returns:
        bool: True if site returns 200 / True если сайт возвращает 200
    """
    if is_connected():
        response = requests.get(url, **kwargs)
        return response.status_code == 200
    else:
        return False


class TestResponse:
    """
    Callback handler for HTTP responses.

    Обработчик обратных вызовов для HTTP ответов.

    Args:
        response (requests.Response): HTTP response / HTTP ответ
    """

    def __init__(self, response: requests.Response):
        self.response = response

    def __call__(self, *args, **kwargs):
        """
        Call appropriate method based on response status.

        Вызывает соответствующий метод в зависимости от статуса ответа.
        """
        if self.response.status_code == 200:
            self.success(*args, **kwargs)
        else:
            self.error(*args, **kwargs)

    def success(self, *args, **kwargs):
        """Called on successful response (status 200)."""
        pass

    def error(self, *args, **kwargs):
        """Called on error response (non-200 status)."""
        pass


def download_file(url, name: str, to: PathLike = '', params=None, use_progressbar: bool = False, **request_kwargs):
    """
    Download a file from URL.

    Загружает файл по URL.

    Args:
        url: URL to download from / URL для загрузки
        name (str): Output filename / Имя выходного файла
        to (PathLike): Destination directory, default current / Целевая директория
        params: URL parameters / Параметры URL
        use_progressbar (bool): Show progress bar, default False / Показать прогресс-бар
        **request_kwargs: Additional arguments for requests.get / Дополнительные аргументы для requests.get

    Returns:
        str: Path to downloaded file / Путь к загруженному файлу
    """
    path = os.path.join(to, name)
    response = requests.get(url, params, stream=True, **request_kwargs)
    if use_progressbar:
        total_size = int(response.headers.get('content-length', 0))
        with open(path, 'wb') as file, tqdm(
                desc=name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                file.write(data)
    else:
        with open(path, 'wb') as file:
            file.write(response.content)
    return path


def download_file_to_temp(url, extension: str = '', name: str = '', params=None, use_progressbar: bool = False,
                          **request_kwargs):
    """
    Download file to temporary directory.

    Загружает файл во временную директорию.

    Args:
        url: URL to download from / URL для загрузки
        extension (str): File extension without dot / Расширение файла без точки
        name (str): Custom filename (UUID if empty), default empty / Имя файла (UUID если пусто)
        params: URL parameters / Параметры URL
        use_progressbar (bool): Show progress bar / Показать прогресс-бар
        **request_kwargs: Additional arguments for requests.get / Дополнительные аргументы для requests.get

    Returns:
        str: Path to downloaded file / Путь к загруженному файлу
    """
    tempdir = tempfile.gettempdir()
    if not name:
        name = str(uuid.uuid4())
    if extension:
        extension = '.' + extension
    path = download_file(url, name + extension, tempdir, params, use_progressbar, **request_kwargs)
    return path


class ReCaptchaV3:
    """
    Google reCAPTCHA v3 verification handler.

    Обработчик верификации Google reCAPTCHA v3.

    Args:
        secret_key (str): Secret key from Google / Секретный ключ от Google
        site_key (NullStr): Site key from Google / Ключ сайта от Google
        score_threshold (float): Minimum score to pass, default 0.5 / Минимальный проходной балл
    """

    def __init__(self, secret_key: str, site_key: NullStr, score_threshold: float = 0.5):
        self.secret_key = secret_key
        self.score_threshold = score_threshold
        self.site_key = site_key

    @property
    def js_api_url(self) -> str:
        """
        Get JavaScript API URL for this site key.

        Получает URL JavaScript API для этого ключа сайта.

        Returns:
            str: reCAPTCHA JS API URL / URL JS API reCAPTCHA
        """
        return f'https://www.google.com/recaptcha/api.js?render={self.site_key}'

    def verify(self, token: str) -> bool:
        """
        Verify reCAPTCHA token.

        Проверяет токен reCAPTCHA.

        Args:
            token (str): reCAPTCHA token to verify / Токен reCAPTCHA для проверки

        Returns:
            bool: True if verification passes / True если проверка пройдена
        """
        if not token:
            return False
        json = requests.post('https://www.google.com/recaptcha/api/siteverify',
                             {'secret': self.secret_key, 'response': token}).json()
        return json.get('success', False) and float(json.get('score', 0)) >= self.score_threshold


def GET_url(base_url: str, **params) -> str:
    """
    Build GET URL with query parameters.

    Строит GET URL с параметрами запроса.

    Args:
        base_url (str): Base URL / Базовый URL
        **params: Query parameters / Параметры запроса

    Returns:
        str: Full URL with encoded parameters / Полный URL с закодированными параметрами
    """
    return f'{base_url}?{urlencode(params)}'
