"""
Function utilities for working with callables.

Provides empty function placeholder, conditional function execution,
lambda generators, and callable objects.

Утилиты для работы с вызываемыми объектами.

Предоставляет заглушку пустой функции, условное выполнение функций,
генераторы лямбд и вызываемые объекты.
"""


def empty_function(*args, **kwargs):
    """
    Function that does nothing.

    Функция, которая ничего не делает.

    Can be used as a placeholder or default callback.

    Может использоваться как заглушка или callback по умолчанию.
    """
    pass


def function_if(condition: bool, true, false=empty_function, is_lambda: bool = False):
    """
    Execute function based on condition.

    Выполняет функцию в зависимости от условия.

    Args:
        condition (bool): Condition to check / Условие для проверки
        true: Function or value if condition is True / Функция или значение при True
        false: Function or value if condition is False, default empty_function / Функция или значение при False
        is_lambda (bool): Treat true/false as values to return, not functions, default False / Интерпретировать как значения

    Returns:
        Result of executed function or value / Результат выполнения функции или значение
    """
    if condition:
        return true if is_lambda else true()
    else:
        return false if is_lambda else false()


def lambda_generator(func, *args, **kwargs):
    """
    Generate a lambda that calls the given function with arguments.

    Генерирует лямбду, вызывающую данную функцию с аргументами.

    Args:
        func: Function to wrap / Функция для обертки
        *args: Positional arguments for the function / Позиционные аргументы
        **kwargs: Keyword arguments for the function / Ключевые аргументы

    Returns:
        callable: Lambda that calls the function / Лямбда, вызывающая функцию
    """
    return lambda: func(*args, **kwargs)


def callable_object(arg):
    """
    Convert a value into a callable that returns that value.

    Преобразует значение в вызываемый объект, возвращающий это значение.

    Args:
        arg: Value to wrap / Значение для обертки

    Returns:
        callable: Function that returns the argument / Функция, возвращающая аргумент
    """
    return lambda: arg
