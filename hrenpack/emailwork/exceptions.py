from hrenpack.exceptions import convert_exception_to_str


class ProtocolNotInitialized(Exception):
    pass


class FolderNotFound(Exception):
    pass


class DownloadError(Exception):
    def __init__(self, exception, *args):
        if isinstance(exception, Exception):
            first_arg = convert_exception_to_str(exception)
        else: first_arg = exception
        super().__init__(first_arg, *args)

