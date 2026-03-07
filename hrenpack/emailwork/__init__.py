import email, warnings
from datetime import datetime
from email.policy import default as default_policy
from pathlib import Path
from typing import Optional, Literal
from imapclient import IMAPClient
from pathlike_typing import PathLike
from .exceptions import ProtocolNotInitialized, FolderNotFound, DownloadError
from .typings import *

__all__ = ['MailClient', 'ServerConfig']


class ServerConfig:
    def __init__(self, host: str, port: int, email: str, password: str, encryption: EncryptionType = 'no'):
        self.host: str = host
        self.port: int = port
        self.email: str = email
        self.password: str = password
        self.encryption: EncryptionType = encryption


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
            self._imap_client = IMAPClient(config.host, config.port, ssl=config.encryption == 'ssl')
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

    def get_folder_uids(self, folder: str) -> list:
        self._imap_required()
        if folder not in self.get_folders_list(): raise FolderNotFound(folder)
        self._imap_client.select_folder(folder, readonly=True)
        return self._imap_client.search(['ALL'])

    def download_eml(self, directory: PathLike, folder: str, uid: str, is_root: bool = True,
                     naming: Literal['uid', 'subject', 'date', 'subject-date', 'subject-uid', 'custom'] = 'uid',
                     custom_filename: Optional[PathLike] = None):
        try:
            self._imap_required()
            download_folder = Path(directory)
            if is_root: download_folder /= folder
            download_folder.mkdir(parents=True, exist_ok=True)
            self._imap_client.select_folder(folder)
            message_data = self._imap_client.fetch([uid], ['RFC822'])

            if int(uid) in message_data:
                raw_data = message_data[int(uid)][b'RFC822']
                message = email.message_from_bytes(raw_data, policy=default_policy)
                filename = ''
                subject = message.get('Subject', uid)
                date = message.get('Date', datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
                match naming:
                    case 'uid': filename = uid
                    case 'subject': filename = subject
                    case 'date': filename = date
                    case 'subject-date': filename = f'{subject}_{date}'
                    case 'subject-uid': filename = f'{subject}_{uid}'
                    case 'custom': filename = custom_filename
                    case _:
                        warnings.warn("Unknown naming: {}".format(naming), UserWarning)
                        filename = uid
                filename += '.eml'
                path = download_folder / filename
                with open(path, 'wb') as file:
                    file.write(raw_data)
                return str(path)
            raise DownloadError("Message not found")
        except Exception as error:
            raise DownloadError(error)
