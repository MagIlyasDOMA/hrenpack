from typing import Callable
from django.core.exceptions import ValidationError


class ConditionValidatorConstructor:
    def __init__(self, condition_func: Callable, message: str):
        self.condition_func = condition_func
        self.message = message

    def __call__(self, value):
        if self.condition_func(value): raise ValidationError(self.message)
        return value
