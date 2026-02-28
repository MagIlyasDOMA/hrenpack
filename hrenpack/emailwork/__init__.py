from typing import Optional
from imapclient import IMAPClient
from .typings import *


class ServerConfig:
    def __init__(self, host: str, port: int, email: str, password: str, encryption: EncryptionType = 'no'):
        self.host: str = host
        self.port: int = port
        self.email: str = email
        self.password: str = password
        self.encryption: EncryptionType = encryption


class ProtocolNotInitialized(Exception): pass


class MailClient:
    def __init__(self, pop_config: Optional[ServerConfig] = None,
                 imap_config: Optional[ServerConfig] = None,
                 smtp_config: Optional[ServerConfig] = None):
        self.pop_config = pop_config
        self._imap_init(imap_config)
        self.smtp_config = smtp_config

    def _imap_init(self, config: Optional[ServerConfig]):
        if config:
            self.imap_config = config
            self._imap_client = IMAPClient(config.host, config.port, True, config.encryption == 'ssl')
            if config.encryption == 'starttls': self._imap_client.starttls()
            self._imap_client.login(config.email, config.password)
        else:
            self.imap_config = None
            self._imap_client = None

    def _imap_required(self):
        if not self.imap_config:
            raise ProtocolNotInitialized('IMAP not initialized')

    def __construct_folders_dict(self):
        pass

    def get_folders_list(self, tree: bool = False, exclude_spam: bool = True, exclude_trash: bool = True,
                         exclude_drafts: bool = True) -> list:
        self._imap_required()
        pre_output = list()
        for dir_type, _, dir_name in self._imap_client.list_folders():
            if len(dir_type) > 0: dir_type = dir_type[0]
            if any((
                all((exclude_spam, dir_type == b'\\Spam')),
                all((exclude_trash, dir_type == b'\\Trash')),
                all((exclude_drafts, dir_type == b'\\Drafts'))
            )): continue
            pre_output.append(dir_name)
        # if tree: pass
        # else: return pre_output
        return pre_output

