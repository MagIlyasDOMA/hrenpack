import logging
from contextlib import redirect_stdout, nullcontext
from functools import wraps


def non_print(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with redirect_stdout(nullcontext()):
            return func(*args, **kwargs)
    return wrapper


def args_kwargs(**kwargs):
    args_name = kwargs.get('args_name', 'args')
    kwargs_name = kwargs.get('kwargs_name', 'kwargs')
    copy_args = kwargs.get('copy_args', True)
    copy_kwargs = kwargs.get('copy_kwargs', True)
    del_kwargs = kwargs.get('del_kwargs', True)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **key_args):
            if args_name in key_args and copy_args:
                args = [*args, *key_args[args_name]]
                if del_kwargs:
                    del key_args[args_name]
            if kwargs_name in key_args and copy_kwargs:
                key_args = {**key_args, **key_args[kwargs_name]}
                if del_kwargs:
                    del key_args[kwargs_name]
            return func(*args, **key_args)
        return wrapper
    return decorator


def debug_logging(start_message: str = '', end_message: str = ''):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if start_message:
                logging.debug(start_message)
            output = func(*args, **kwargs)
            if end_message:
                logging.debug(end_message)
            return output
        return wrapper
    return decorator


def method(func): return func


def multi_decorator(*decorators):
    """Декораторы применяются слева направо"""
    def decorator(func):
        for dec in decorators:
            func = dec(func)
        return func
    return decorator
