import functools, inspect
from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from typing import Sequence
from typeguard import check_type as check_type_strict, TypeCheckError
from hrenpack.functionwork import empty_function
from hrenpack.listwork import get_from_dict


class EncapsulationError(Exception):
    pass


def count_inheritance_levels(cls):
    # Получаем все классы в порядке разрешения методов
    mro = cls.__mro__
    # Считаем, сколько раз base_class есть в цепочке MRO
    count = 0
    for c in mro:
        if c is object:
            count += 1
    return count - 2


def check_method_in_parent(cls, name, debug_mode: bool = False):
    bases = cls.__bases__
    if debug_mode:
        print(bases)
    for base in bases:
        if hasattr(base, name):
            if debug_mode:
                print(base.__name__)
            return True
    return False


class AbstractClass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls is AbstractClass or AbstractClass in cls.__bases__:
            raise TypeError("Это абстрактный класс, его можно только наследовать")
        try:
            return super().__new__(cls, *args, **kwargs)
        except TypeError:
            return super().__new__(cls)


# def abstractclass(cls):
#     class _Class(cls, AbstractClass):
#         pass
#     return _Class


# class ClassMethodMeta(type):
#     """Не работает"""
#     def __new__(cls, name, bases, attrs):
#         new_class = super().__new__(cls, name, bases, attrs)
#
#         for attr_name, attr_value in attrs.items():
#             if callable(attr_value):
#                 if '__' in attr_name:
#                     continue
#                 setattr(new_class, attr_name, classmethod(attr_value))
#
#         return new_class
#
#
# class StaticClass(metaclass=ClassMethodMeta):
#     """Не работает"""
#     def __new__(cls):
#         raise TypeError("Это статический класс, он не может создавать объекты")
#
#
# def staticclass(cls):
#     """Не работает"""
#     class _Class(StaticClass, cls):
#         pass
#     return _Class


def inner_function():
    frame = inspect.currentframe()
    local_vars = frame.f_back.f_locals
    del frame
    return local_vars


def protectedmethod(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        stack = inspect.stack()
        for frame in stack:
            caller = frame.frame
            if caller.f_locals.get('self') is args[0]:
                return method(*args, **kwargs)
        raise EncapsulationError("Это защищенный метод")
    return wrapper


def privatemethod(method):
    """Пока что работает только как защищенный метод"""
    return protectedmethod(method)


def supermethod(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        getattr(super(type(self), self), method.__name__, empty_function)(*args, **kwargs)
        return method(self, *args, **kwargs)
    return wrapper


def supermethod_post(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        output = method(self, *args, **kwargs)
        getattr(super(type(self), self), method.__name__, empty_function)(*args, **kwargs)
        return output
    return wrapper


def superonlymethod(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return getattr(super(type(self), self), method.__name__, empty_function)(*args, **kwargs)
    return wrapper


def addattr(instance, attr_name, value):
    if not hasattr(instance, attr_name):
        setattr(instance, attr_name, value)


def update_attrs_from_dict(instance, **attrs):
    for attr_name, value in attrs.items():
        setattr(instance, attr_name, value)


def add_attrs_from_dict(instance, **attrs):
    for attr_name, value in attrs.items():
        addattr(instance, attr_name, value)


def setattr_if_is_none(instance, attr_name, value):
    if getattr(instance, attr_name, None) is None:
        addattr(instance, attr_name, value)


def set_attrs_if_is_none(instance, **attrs):
    for attr_name, value in attrs.items():
        setattr_if_is_none(instance, attr_name, value)


def getattrs(instance, *attr_names, only_values: bool = False, is_tuple: bool = False, default=None):
    output = dict()
    for attr_name in attr_names:
        output[attr_name] = getattr(instance, attr_name, default)
    return get_from_dict(output, *output.keys(), is_tuple=is_tuple, only_values=only_values, default=default)


def getattr_strict(obj, name: str):
    if hasattr(obj, name): return getattr(obj, name)
    elif isinstance(obj, type):
        raise AttributeError(f"type object '{obj.__name__}' has no attribute '{name}'")
    raise AttributeError(f"{obj.__class__.__name__} object has no attribute '{name}'")


def getattr_plus(obj, tree: Sequence[str], default=None, *, dict_mode: bool = False, catch_errors: bool = True):
    if isinstance(tree, str): tree = tree.split('.')
    if len(tree) == 0:
        return default
    elif len(tree) == 1:
        key = tree[0]
        if dict_mode:
            try: return obj[key]
            except KeyError as error:
                if not catch_errors: raise error
        else:
            try: return getattr_strict(obj, key)
            except AttributeError as error:
                if not catch_errors: raise error
    else:
        output = obj
        for i, level in enumerate(tree):
            if dict_mode:
                try: output = output[level]
                except KeyError:
                    if not catch_errors: raise KeyError(f'{level} in level {i}')
                    break
            else:
                try: output = getattr_strict(output, level)
                except AttributeError:
                    if not catch_errors: raise AttributeError(f'{level} in level {i}')
                    break
                output = getattr(output, level)
        else: return output
    return default


def check_type(value, typing):
    try:
        check_type_strict(value, typing)
        return True
    except (TypeError, TypeCheckError):
        return False


def get_own_attributes(obj):
    all_attrs = set(dir(obj))
    parent_attrs = set()

    cls = obj.__class__
    for parent in cls.__bases__:
        if parent != object:
            parent_attrs.update(dir(parent))

    return all_attrs - parent_attrs
