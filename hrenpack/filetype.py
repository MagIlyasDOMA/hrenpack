import mimetypes
from pathlike_typing import PathLike
from .cmd import get_extension
from .constants import MIME_TYPES, COMPOUND_EXTENSIONS


def get_mime_type(path: str):
    return mimetypes.guess_type(path)[0] or 'application/octet-stream'


def get_mime_type_extension(path: PathLike):
    path = str(path)
    for ext, mime in COMPOUND_EXTENSIONS.items():
        if path.endswith(ext): return mime
    return MIME_TYPES.get(get_extension(path), 'application/octet-stream')


def get_mime_type_filetype(path: str):
    from filetype import guess
    kind = guess(path)
    if kind is None:
        return 'application/octet-stream'
    return kind.mime


def get_mime_type_magic(path: str):
    from puremagic import from_file
    return from_file(path, True)


if __name__ == '__main__':
    print(get_mime_type('d.cpp'))
