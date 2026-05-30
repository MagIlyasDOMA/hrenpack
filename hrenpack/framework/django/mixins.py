"""
Django class-based view mixins.

Provides mixins for context data, model management, URL handling,
and authorization.

Примеси для классовых представлений Django.

Предоставляет примеси для контекстных данных, управления моделями,
обработки URL и авторизации.
"""

from django.utils.decorators import classonlymethod
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from hrenpack import NullStr
from hrenpack.encapsulation import add_attrs_from_dict
from hrenpack.framework.django import view_dict


class DataMixin:
    """
    Mixin for adding title and h1_title to context.
    Use when incompatible with View and TemplateView classes.

    Примесь для добавления title и h1_title в контекст.
    Использовать в случае несовместимости с классами View и TemplateView.

    Attributes:
        title (str): Page title / Заголовок страницы
        h1_title (NullStr): H1 heading text / Текст заголовка H1
    """
    title: str
    h1_title: NullStr = None

    def get_context_data(self, **kwargs):
        """
        Add title and h1_title to context.

        Добавляет title и h1_title в контекст.

        Args:
            **kwargs: Existing context data / Существующие данные контекста

        Returns:
            dict: Updated context / Обновленный контекст
        """
        try:
            kwargs = super().get_context_data(**kwargs)
        except AttributeError as error:
            raise error
        kwargs['title'] = self.title
        kwargs['h1_title'] = self.h1_title
        return view_dict(**kwargs)


class NonAbstractMixin:
    """
    Mixin that allows passing title/h1_title to as_view().

    Примесь, позволяющая передавать title/h1_title в as_view().

    Example:
        MyView.as_view(title="My Page", h1_title="Welcome")
    """

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Create view with optional title and h1_title.

        Создает представление с опциональными title и h1_title.
        """
        add_attrs_from_dict(cls, title=initkwargs.get('title', None), h1_title=initkwargs.get('h1_title', None))
        return super().as_view(**initkwargs)


class ModelManagerMixin:
    """
    Mixin for model manager access.

    Примесь для доступа к менеджеру модели.

    Attributes:
        model_manager: Model or manager to use / Модель или менеджер для использования
    """
    model_manager = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.model_manager is None:
            self.model_manager = self.model


class SuccessURLMixin:
    """
    Mixin for success URL handling.

    Примесь для обработки URL успеха.

    Attributes:
        success_url (str): URL to redirect after success / URL для перенаправления после успеха
    """
    success_url: str

    def get_success_url(self):
        """
        Get success URL.

        Получает URL успеха.

        Returns:
            str: Success URL / URL успеха
        """
        return self.success_url


class UserAuthorizeMixin:
    """
    Mixin for user authorization flag.

    Примесь для флага авторизации пользователя.

    Attributes:
        authorize (bool): Authorization flag / Флаг авторизации
    """
    authorize: bool = False

    def get_context_data(self, **kwargs):
        """
        Add authorize flag to context.

        Добавляет флаг авторизации в контекст.

        Args:
            **kwargs: Existing context data / Существующие данные контекста

        Returns:
            dict: Updated context / Обновленный контекст
        """
        kwargs['authorize'] = self.authorize
        return super().get_context_data(**kwargs)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Create view with optional authorize flag.

        Создает представление с опциональным флагом авторизации.
        """
        authorize = initkwargs.get('authorize', False)
        if authorize and not cls.authorize:
            cls.authorize = True
        return super().as_view(**initkwargs)


class TemplateViewMixin(ContextMixin, TemplateResponseMixin):
    """
    Mixin combining ContextMixin and TemplateResponseMixin.

    Примесь, объединяющая ContextMixin и TemplateResponseMixin.
    """
    pass
