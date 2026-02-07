import inspect, functools
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse


def post_json_response(view):
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if inspect.ismethod(view):
            raise ImproperlyConfigured('This view supports only FBV')
        elif request.method == 'POST':
            return view(request, *args, **kwargs)
        return JsonResponse(dict(
            status='error',
            message='Required POST method',
            code=405
        ), status=405)
    return wrapper
