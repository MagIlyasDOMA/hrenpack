from typing import Literal

__all__ = ['InputProtocol', 'OutputProtocol', 'MailProtocol', 'EncryptionType',
           'EMLSearchMode', 'MessageItems']

InputProtocol = Literal['pop', 'imap']
OutputProtocol = Literal['smtp']
MailProtocol = Literal['imap', 'pop', 'smtp']
EncryptionType = Literal['no', 'starttls', 'ssl']

EMLSearchMode = Literal['from', 'to', 'subject', 'everywhere']
MessageItems = Literal['path', 'data']
