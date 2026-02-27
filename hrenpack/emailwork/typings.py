from typing import Literal

__all__ = ['InputProtocol', 'OutputProtocol', 'MailProtocol']

InputProtocol = Literal['pop', 'imap']
OutputProtocol = Literal['smtp']
MailProtocol = Literal['imap', 'pop', 'smtp']
