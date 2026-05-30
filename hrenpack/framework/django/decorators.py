"""
Django view decorators.

Provides decorators for view functions, including POST-only JSON responses.

Декораторы представлений Django.

Предоставляет декораторы для функций представлений, включая ответы JSON только для POST.
"""

import inspect, functools
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse


def post_json_response(view):
    """
    Decorator that allows only POST requests and returns JSON response.

    Декоратор, разрешающий только POST запросы и возвращающий JSON ответ.

    Args:
        view: View function to decorate / Функция представления для декорирования

    Returns:
        callable: Wrapped view / Обернутое представление

    Raises:
        ImproperlyConfigured: If view is a method (only FBV supported) / Если представление - метод (поддерживается только FBV)

    Example:
        @post_json_response
        def my_view(request):
            return JsonResponse({'success': True})
    """

    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if inspect.ismethod(view):
            raise ImproperlyConfigured('This view supports only FBV (Function-Based Views)')
        elif request.method == 'POST':
            return view(request, *args, **kwargs)
        return JsonResponse(dict(
            success=False,
            message='Required POST method',
            code=405
        ), status=405)

    return wrapper
