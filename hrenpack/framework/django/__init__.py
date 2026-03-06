import importlib
from urllib.parse import urlencode
from django.conf import settings
from django.db.models import IntegerChoices
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from hrenpack import NullStr
from hrenpack.security import HTMLSanitizer


class HrenpackDjangoError(Exception):
    pass


def view_dict(title: str, h1_title: NullStr = None, **kwargs) -> dict:
    kwargs['title'] = title
    kwargs['h1_title'] = title if h1_title is None else h1_title
    return kwargs


def boolean_choices(arg: IntegerChoices):
    return tuple(map(lambda x: (bool(x[0]), x[1]), arg.choices))


def semicolon_plus(model, del_id: bool = True):
    output = dict()
    for field in model._meta.fields:
        verbose_name = field.verbose_name + ':'
        name = field.name
        output[name] = verbose_name
    if del_id:
        del output['id']
    return output


class BooleanChoices(IntegerChoices):
    @property
    def choices(self):
        return boolean_choices(self)


def get_view_app(view):
    return view.__module__.split('.')[0]


def get_view_base_template(view):
    # Добавьте проверку на None и пустую строку
    base_template = getattr(view, 'base_template_name', None)
    if not base_template:
        base_template = getattr(settings, 'BASE_TEMPLATE', 'empty.html')
    return base_template or 'empty.html'  # Гарантирует возврат непустого значения


def add_url_GET(base_url: str, request=None, **params):
    if request is not None:
        params.update(request.GET)
    return f'{base_url}?{urlencode(params)}'


def url_or_reverse(url: str, lazy_mode: bool = True, **kwargs):
    if '/' in url:
        return url
    func = reverse_lazy if lazy_mode else reverse
    return func(url, kwargs=kwargs)


def get_app_inclusion_namespace(app_name: str):
    urlpatterns = importlib.import_module(settings.ROOT_URLCONF).urlpatterns
    for pattern in urlpatterns:
        if hasattr(pattern, 'app_name') and pattern.app_name == app_name:
            return pattern.namespace


def sanitize_html_and_mark_safe(html: str):
    return mark_safe(HTMLSanitizer(html).sanitize())
