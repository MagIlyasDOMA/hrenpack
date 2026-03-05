def convert_exception_to_str(exception: Exception):
    return f'{exception.__class__.__name__}: {str(exception)}'


class ExtraArgumentsWarning(UserWarning):
    pass
