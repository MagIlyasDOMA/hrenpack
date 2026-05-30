"""
Django class-based views extensions.

Provides extended view classes with title, h1_title, and template support.

Расширения классовых представлений Django.

Предоставляет расширенные классы представлений с поддержкой title, h1_title и шаблонов.
"""

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Model
from django.shortcuts import render, redirect
from django.utils.decorators import classonlymethod
from django.views import View as DjangoView, generic
from django.contrib.auth import views as auth_views, logout, get_user_model, login
from hrenpack import NullStr
from hrenpack.listwork import get_from_dict
from hrenpack.encapsulation import set_attrs_if_is_none
from hrenpack.framework.django import view_dict
from hrenpack.framework.django.mixins import (NonAbstractMixin, ModelManagerMixin, UserAuthorizeMixin,
                                              TemplateViewMixin)


class BaseView(DjangoView, NonAbstractMixin):
    """
    Base view with title, h1_title, and template support.

    Базовое представление с поддержкой title, h1_title и шаблона.

    Attributes:
        title (NullStr): Page title / Заголовок страницы
        h1_title (NullStr): H1 heading / Заголовок H1
        dont_header (bool): Disable header rendering / Отключить рендеринг заголовка
    """
    title: NullStr = None
    h1_title: NullStr = None
    dont_header: bool = False
    _base_template_name: str = getattr(settings, 'BASE_TEMPLATE', 'empty.html')

    def get_context_data(self, **kwargs):
        """
        Get context data with title and h1_title.

        Получает данные контекста с title и h1_title.

        Args:
            **kwargs: Additional context / Дополнительный контекст

        Returns:
            dict: Context dictionary / Словарь контекста
        """
        kwargs = super().get_context_data(**kwargs)
        kwargs['title'] = self.title if self.title else "Page"
        kwargs['h1_title'] = self.h1_title
        kwargs['dont_header'] = self.dont_header
        kwargs['base_template_name'] = self.base_template_name
        return view_dict(**kwargs)

    @property
    def base_template_name(self):
        """
        Get base template name.

        Получает имя базового шаблона.

        Returns:
            str: Base template name / Имя базового шаблона
        """
        return getattr(self, '_base_template_name',
                       getattr(settings, 'BASE_TEMPLATE', 'empty.html'))

    @base_template_name.setter
    def base_template_name(self, value):
        """Set base template name."""
        self._base_template_name = value or getattr(settings, 'BASE_TEMPLATE', 'empty.html')

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Create view with optional title, h1_title, template_name.

        Создает представление с опциональными title, h1_title, template_name.
        """
        initkwargs.setdefault('title', "Page")
        set_attrs_if_is_none(cls, **get_from_dict(initkwargs, 'title', 'h1_title', 'template_name',
                                                  'extra_context', pop_mode=True))
        return super().as_view(**initkwargs)


class View(BaseView, TemplateViewMixin):
    """Basic view with template support."""
    pass


class TemplateView(BaseView, generic.TemplateView):
    """Template view with BaseView features."""
    pass


class ListView(BaseView):
    """
    List view for displaying model objects.

    Представление списка для отображения объектов модели.

    Attributes:
        model (Model): Django model / Модель Django
        context_name (str): Context variable name, default 'db' / Имя переменной контекста
    """
    model: Model
    context_name: str = 'db'

    def get_context_data(self, **kwargs):
        """Add queryset to context."""
        kwargs = super().get_context_data(**kwargs)
        kwargs[self.context_name] = self.get_queryset()
        return kwargs

    def get_queryset(self):
        """Get all objects from model."""
        return self.model.objects.all()


class DetailView(ModelManagerMixin, BaseView, generic.DetailView):
    """Detail view with model manager support."""
    pass


class FormView(BaseView, generic.FormView):
    """Form view with BaseView features."""
    pass


class CreateView(BaseView, generic.CreateView):
    """Create view with BaseView features."""
    pass


class UpdateView(ModelManagerMixin, BaseView, generic.UpdateView):
    """Update view with model manager support."""
    pass


class PasswordChangeView(BaseView, auth_views.PasswordChangeView):
    """Password change view."""
    pass


class PasswordChangeDoneView(BaseView, auth_views.PasswordChangeDoneView):
    """Password change done view."""
    pass


class PasswordResetView(BaseView, auth_views.PasswordResetView):
    """Password reset view."""
    pass


class PasswordResetDoneView(BaseView, auth_views.PasswordResetDoneView):
    """Password reset done view."""
    pass


class PasswordResetConfirmView(BaseView, auth_views.PasswordResetConfirmView):
    """Password reset confirm view."""
    pass


class PasswordResetCompleteView(UserAuthorizeMixin, BaseView, auth_views.PasswordResetCompleteView):
    """Password reset complete view with authorization."""
    pass


class LoginView(BaseView, auth_views.LoginView):
    """Login view."""
    title = "Login"


class LogoutView(BaseView, auth_views.LogoutView):
    """Logout view."""
    title = "You have been logged out"


def create_logout_view(template_name: str, title: str = "You have been logged out", h1_title: NullStr = None,
                       dont_header: bool = False, **kwargs):
    """
    Create a logout view function.

    Создает функцию представления для выхода из аккаунта.

    Args:
        template_name (str): Template name / Имя шаблона
        title (str): Page title / Заголовок страницы
        h1_title (NullStr): H1 heading / Заголовок H1
        dont_header (bool): Disable header / Отключить заголовок
        **kwargs: Additional context / Дополнительный контекст

    Returns:
        callable: Logout view function / Функция представления выхода
    """

    def logout_view(request):
        logout(request)
        return render(request, template_name, view_dict(title, h1_title, dont_header=dont_header, **kwargs))

    return logout_view


def create_logout_view_with_next():
    """
    Create a logout view that redirects to 'next' parameter.

    Создает представление выхода, перенаправляющее на параметр 'next'.

    Returns:
        callable: Logout view with redirect / Представление выхода с перенаправлением
    """

    def logout_view(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(request.GET.get('next', '/'))

    return logout_view


class RegistrationView(CreateView):
    """
    User registration view.

    Представление регистрации пользователя.
    """
    title = "Registration"
    model = get_user_model()
    form_class = UserCreationForm

    def form_valid(self, form):
        """Log in user after successful registration."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class StaticFileView(generic.RedirectView):
    """
    View for serving static files.

    Представление для обслуживания статических файлов.
    """

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Create view with required path parameter.

        Создает представление с обязательным параметром path.

        Args:
            path (str): Path to static file / Путь к статическому файлу

        Returns:
            StaticFileView: View instance / Экземпляр представления

        Raises:
            KeyError: If path not provided / Если path не предоставлен
        """
        path = initkwargs.pop('path')
        if path is None:
            raise KeyError('path')
        return super().as_view(url=staticfiles_storage.url(path), **initkwargs)
