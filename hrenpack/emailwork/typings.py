"""
Type hints for email module.

Provides Protocol and TypedDict types for email data structures.

Подсказки типов для модуля email.

Предоставляет Protocol и TypedDict типы для структур данных email.
"""

from typing import Literal, Protocol, Optional, NotRequired, TypedDict, Union
from pathlike_typing import PathLike

__all__ = ['InputProtocol', 'OutputProtocol', 'MailProtocol', 'EncryptionType',
           'EMLSearchMode', 'MessageItems', 'AttachmentData', 'UsersList', 'EMLData', 'MessageData']

InputProtocol = Literal['pop', 'imap']
"""Input email protocols."""
OutputProtocol = Literal['smtp']
"""Output email protocols."""
MailProtocol = Literal['imap', 'pop', 'smtp']
"""All email protocols."""
EncryptionType = Literal['no', 'starttls', 'ssl']
"""Email encryption types."""

EMLSearchMode = Literal['from', 'to', 'subject', 'attachments', 'everywhere']
"""Search modes for email messages."""
MessageItems = Literal['path', 'data', 'from_', 'to', 'subject', 'text_plain', 'text_html', 'attachments']
"""Available message attributes."""
UsersList = tuple[tuple[str, str]]
"""Tuple of (email, name) pairs."""


AttachmentData = TypedDict(
    'AttachmentData',
    {
        'binary': bool,
        'charset': Optional[str],
        'content-disposition': str,
        'content-id': str,
        'content_transfer_encoding': str,
        'filename': str,
        'mail_content_type': str
    },
)
"""
Attachment metadata.

Метаданные вложения.

Attributes:
    binary (bool): Whether attachment is binary / Является ли вложение бинарным
    charset (Optional[str]): Character encoding / Кодировка символов
    content-disposition (str): Content disposition / Расположение содержимого
    content-id (str): Content ID / ID содержимого
    content_transfer_encoding (str): Transfer encoding / Кодировка передачи
    filename (str): Attachment filename / Имя файла вложения
    mail_content_type (str): MIME content type / MIME тип содержимого
"""


class EMLData(Protocol):
    """
    Protocol for parsed email data.

    Protocol для разобранных email данных.
    """

    @property
    def from_(self) -> UsersList:
        """Email sender(s)."""
        ...

    @property
    def to(self) -> UsersList:
        """Email recipient(s)."""
        ...

    @property
    def subject(self) -> str:
        """Email subject."""
        ...

    @property
    def text_plain(self) -> list[str]:
        """Plain text content."""
        ...

    @property
    def text_html(self) -> list[str]:
        """HTML content."""
        ...

    @property
    def attachments(self) -> list[AttachmentData]:
        """Attachments list."""
        ...


class MessageData(TypedDict):
    """
    Message data structure for searching.

    Структура данных сообщения для поиска.

    Attributes:
        path (PathLike): Path to .eml file / Путь к .eml файлу
        data (NotRequired[EMLData]): Parsed email data / Разобранные email данные
        from_ (UsersList): Sender(s) / Отправитель(и)
        to (UsersList): Recipient(s) / Получатель(и)
        subject (str): Subject / Тема
        text_plain (NotRequired[str]): Plain text content / Текст в формате plain
        text_html (NotRequired[str]): HTML content / HTML содержимое
        attachments (NotRequired[Union[list[AttachmentData], list[str]]]): Attachments / Вложения
    """
    path: PathLike
    data: NotRequired[EMLData]
    from_: UsersList
    to: UsersList
    subject: str
    text_plain: NotRequired[str]
    text_html: NotRequired[str]
    attachments: NotRequired[Union[list[AttachmentData], list[str]]]
