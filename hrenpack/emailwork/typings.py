from typing import Literal

__all__ = ['InputProtocol', 'OutputProtocol', 'MailProtocol', 'EncryptionType']

InputProtocol = Literal['pop', 'imap']
OutputProtocol = Literal['smtp']
MailProtocol = Literal['imap', 'pop', 'smtp']
EncryptionType = Literal['no', 'starttls', 'ssl']
