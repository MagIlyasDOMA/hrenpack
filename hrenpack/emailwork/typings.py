from typing import Literal, Protocol, Optional, NotRequired, TypedDict
from pathlike_typing import PathLike

__all__ = ['InputProtocol', 'OutputProtocol', 'MailProtocol', 'EncryptionType',
           'EMLSearchMode', 'MessageItems', 'AttachmentData', 'UsersList', 'EMLData', 'MessageData']

InputProtocol = Literal['pop', 'imap']
OutputProtocol = Literal['smtp']
MailProtocol = Literal['imap', 'pop', 'smtp']
EncryptionType = Literal['no', 'starttls', 'ssl']

EMLSearchMode = Literal['from', 'to', 'subject', 'attachments', 'everywhere']
MessageItems = Literal['path', 'data', 'from_', 'to', 'subject', 'text_plain', 'text_html', 'attachments']
UsersList = list[tuple[str, str]]


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


class EMLData(Protocol):
    @property
    def from_(self) -> UsersList: ...

    @property
    def to(self) -> UsersList: ...

    @property
    def subject(self) -> str: ...

    @property
    def text_plain(self) -> list[str]: ...

    @property
    def text_html(self) -> list[str]: ...

    @property
    def attachments(self) -> list[AttachmentData]: ...


class MessageData(TypedDict):
    path: PathLike
    data: NotRequired[EMLData]
    from_: UsersList
    to: UsersList
    subject: str
    text_plain: str
    text_html: str
    attachments: list[AttachmentData]
