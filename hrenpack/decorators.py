"""
Useful decorators for Python functions.

Provides decorators for suppressing output, merging arguments, debug logging,
and applying multiple decorators.

Полезные декораторы для функций Python.

Предоставляет декораторы для подавления вывода, объединения аргументов,
отладочного логирования и применения нескольких декораторов.
"""

import logging
from contextlib import redirect_stdout, nullcontext
from functools import wraps


def non_print(func):
    """
    Decorator that suppresses all print output from a function.

    Декоратор, подавляющий весь вывод print из функции.

    Args:
        func: Function to decorate / Функция для декорирования

    Returns:
        callable: Wrapped function / Обернутая функция
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with redirect_stdout(nullcontext()):
            return func(*args, **kwargs)

    return wrapper


def args_kwargs(**kwargs):
    """
    Decorator factory that merges args/kwargs from dictionary parameters.

    Фабрика декораторов, объединяющая args/kwargs из параметров-словарей.

    Args:
        args_name (str): Name of dict containing additional args, default 'args' / Имя словаря с доп. аргументами
        kwargs_name (str): Name of dict containing additional kwargs, default 'kwargs' / Имя словаря с доп. kwargs
        copy_args (bool): Copy args from the dict, default True / Копировать args из словаря
        copy_kwargs (bool): Copy kwargs from the dict, default True / Копировать kwargs из словаря
        del_kwargs (bool): Delete the dict parameters after processing, default True / Удалить параметры-словари

    Returns:
        callable: Decorator / Декоратор
    """
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
    """
    Decorator factory that adds debug logging before and after function execution.

    Фабрика декораторов, добавляющая отладочное логирование до и после выполнения функции.

    Args:
        start_message (str): Message to log before function execution / Сообщение до выполнения функции
        end_message (str): Message to log after function execution / Сообщение после выполнения функции

    Returns:
        callable: Decorator / Декоратор
    """

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


def method(func):
    """
    Identity decorator for marking methods (does nothing).

    Декоратор-идентификатор для маркировки методов (ничего не делает).

    Args:
        func: Function to return unchanged / Функция для возврата без изменений

    Returns:
        callable: The same function / Та же функция
    """
    return func


def multi_decorator(*decorators):
    """
    Apply multiple decorators from left to right.

    Применяет несколько декораторов слева направо.

    Args:
        *decorators: Decorators to apply / Декораторы для применения

    Returns:
        callable: Decorator that applies all given decorators / Декоратор, применяющий все переданные декораторы
    """

    def decorator(func):
        for dec in decorators:
            func = dec(func)
        return func

    return decorator
