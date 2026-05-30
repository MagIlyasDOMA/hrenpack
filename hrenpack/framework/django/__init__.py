"""
Django framework core utilities.

Provides view context helpers, form utilities, URL handling,
HTML sanitization, and class-based view mixins.

Основные утилиты для фреймворка Django.

Предоставляет вспомогательные функции для контекста представлений, формы,
обработку URL, санитизацию HTML и примеси для классовых представлений.
"""

import importlib
from urllib.parse import urlencode
from django.conf import settings
from django.db.models import IntegerChoices
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from hrenpack import NullStr
from hrenpack.security import HTMLSanitizer


class HrenpackDjangoError(Exception):
    """Base exception for hrenpack Django utilities."""
    pass


def view_dict(title: str, h1_title: NullStr = None, **kwargs) -> dict:
    """
    Create context dictionary for views with title and h1_title.

    Создает словарь контекста для представлений с title и h1_title.

    Args:
        title (str): Page title / Заголовок страницы
        h1_title (NullStr): H1 heading text, uses title if None / Текст заголовка H1
        **kwargs: Additional context variables / Дополнительные переменные контекста

    Returns:
        dict: Context dictionary / Словарь контекста
    """
    kwargs['title'] = title
    kwargs['h1_title'] = title if h1_title is None else h1_title
    return kwargs


def boolean_choices(arg: IntegerChoices):
    """
    Convert IntegerChoices to boolean choices tuple.

    Преобразует IntegerChoices в кортеж булевых выборов.

    Args:
        arg (IntegerChoices): IntegerChoices class / Класс IntegerChoices

    Returns:
        tuple: Boolean choices tuple / Кортеж булевых выборов

    Example:
        >>> boolean_choices(MyChoices)
        ((False, 'No'), (True, 'Yes'))
    """
    return tuple(map(lambda x: (bool(x[0]), x[1]), arg.choices))


def semicolon_plus(model, del_id: bool = True):
    """
    Create dictionary of model fields with verbose names followed by colon.

    Создает словарь полей модели с verbose_names, за которыми следует двоеточие.

    Args:
        model: Django model class / Класс модели Django
        del_id (bool): Remove 'id' field from output, default True / Удалить поле 'id' из вывода

    Returns:
        dict: {field_name: 'verbose_name:'} / {имя_поля: 'verbose_name:'}
    """
    output = dict()
    for field in model._meta.fields:
        verbose_name = field.verbose_name + ':'
        name = field.name
        output[name] = verbose_name
    if del_id:
        del output['id']
    return output


class BooleanChoices(IntegerChoices):
    """
    IntegerChoices subclass that returns boolean choices.

    Подкласс IntegerChoices, возвращающий булевы выборы.

    Example:
        class MyChoices(BooleanChoices):
            NO = 0, 'No'
            YES = 1, 'Yes'
    """
    @property
    def choices(self):
        """Return boolean choices instead of integer choices."""
        return boolean_choices(self)


def get_view_app(view):
    """
    Get app name from view class.

    Получает имя приложения из класса представления.

    Args:
        view: View class or instance / Класс или экземпляр представления

    Returns:
        str: App name / Имя приложения
    """
    return view.__module__.split('.')[0]


def get_view_base_template(view):
    """
    Get base template name from view or settings.

    Получает имя базового шаблона из представления или настроек.

    Args:
        view: View class or instance / Класс или экземпляр представления

    Returns:
        str: Base template name / Имя базового шаблона
    """
    base_template = getattr(view, 'base_template_name', None)
    if not base_template:
        base_template = getattr(settings, 'BASE_TEMPLATE', 'empty.html')
    return base_template or 'empty.html'


def add_url_GET(base_url: str, request=None, **params):
    """
    Add GET parameters to URL.

    Добавляет GET параметры к URL.

    Args:
        base_url (str): Base URL / Базовый URL
        request: Django request object (adds request.GET) / Объект запроса Django
        **params: Additional parameters / Дополнительные параметры

    Returns:
        str: URL with encoded parameters / URL с закодированными параметрами
    """
    if request is not None:
        params.update(request.GET)
    return f'{base_url}?{urlencode(params)}'


def url_or_reverse(url: str, lazy_mode: bool = True, **kwargs):
    """
    Return URL if contains slash, otherwise reverse resolve.

    Возвращает URL, если содержит слеш, иначе выполняет reverse resolve.

    Args:
        url (str): URL or view name / URL или имя представления
        lazy_mode (bool): Use reverse_lazy if True, default True / Использовать reverse_lazy
        **kwargs: Arguments for reverse / Аргументы для reverse

    Returns:
        str: Resolved URL / Разрешенный URL
    """
    if '/' in url:
        return url
    func = reverse_lazy if lazy_mode else reverse
    return func(url, kwargs=kwargs)


def get_app_inclusion_namespace(app_name: str):
    """
    Get namespace for app from URL configuration.

    Получает пространство имен для приложения из конфигурации URL.

    Args:
        app_name (str): Application name / Имя приложения

    Returns:
        str: Namespace or None / Пространство имен или None
    """
    urlpatterns = importlib.import_module(settings.ROOT_URLCONF).urlpatterns
    for pattern in urlpatterns:
        if hasattr(pattern, 'app_name') and pattern.app_name == app_name:
            return pattern.namespace


def sanitize_html_and_mark_safe(html: str):
    """
    Sanitize HTML and mark as safe for Django templates.

    Очищает HTML и помечает как безопасный для шаблонов Django.

    Args:
        html (str): HTML content / HTML содержимое

    Returns:
        SafeString: Sanitized safe HTML string / Очищенная безопасная HTML строка
    """
    return mark_safe(HTMLSanitizer(html).sanitize())
