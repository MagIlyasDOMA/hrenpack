import email, warnings, os, mailparser, typing
from datetime import datetime
from email.policy import default as default_policy
from pathlib import Path
from typing import Optional, Literal, Iterator, List
from imapclient import IMAPClient
from pathlike_typing import PathLike
from ..classes import frozendict
from ..exceptions import ExtraArgumentsWarning
from .exceptions import ProtocolNotInitialized, FolderNotFound, DownloadError
from .typings import *

__all__ = ['MailClient', 'ServerConfig', 'LocalFileFinder']


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


class LocalFileFinder:
    class Message:
        __slots__ = ['path', 'data']
        path: PathLike
        data: EMLData

        def __init__(self, path: PathLike):
            object.__setattr__(self, 'path', Path(path))
            object.__setattr__(self, 'data', mailparser.parse_from_file(str(path)))

        def __setattr__(self, name, value):
            if hasattr(self, name):
                raise AttributeError(f"Cannot modify immutable object attribute '{name}'")
            super().__setattr__(name, value)

        def __delattr__(self, name):
            raise AttributeError(f"Cannot delete attribute '{name}' from immutable object")

        def __getitem__(self, item: MessageItems):
            if item in self.keys():
                return getattr(self, item)
            raise KeyError(item)

        @property
        def text_plain(self) -> str: return '\n'.join(self.data.text_plain)

        @property
        def text_html(self) -> str: return '\n'.join(self.data.text_html)

        def keys(self): return typing.get_args(MessageItems)

        def values(self): return dict(self).values()

        def items(self): return dict(self).items()

        def __iter__(self): return iter(self.keys())

        def __len__(self) -> int: return len(self.keys())

        def __eq__(self, other) -> bool:
            return isinstance(other, LocalFileFinder.Message) and dict(self) == dict(other)

        def __hash__(self): return hash(frozendict(self))

        @property
        def subject(self) -> str: return self.data.subject

        @property
        def from_(self) -> UsersList: return tuple(self.data.from_)

        @property
        def to(self) -> UsersList: return tuple(self.data.to)

        @property
        def attachments(self) -> tuple[AttachmentData]:
            return tuple(map(frozendict, self.data.attachments)) # type: ignore

        def corresponds(self, search_line: str, search_mode: EMLSearchMode) -> bool:
            return LocalFileFinder.message_check(self, search_line, search_mode)


    def __init__(self, directory: PathLike):
        self.directory = Path(directory)

    @staticmethod
    def _search_mode_is(current: EMLSearchMode, needed: EMLSearchMode) -> bool:
        return current in (needed, 'everywhere')

    @staticmethod
    def _test_kwargs(kwargs: dict):
        if kwargs: warnings.warn('Found extra kwargs', ExtraArgumentsWarning, 2)

    @classmethod
    def _message_check(cls, message: LocalFileFinder.Message,
                       search_line: str, search_mode: EMLSearchMode) -> bool:
        if cls._search_mode_is(search_mode, 'from'):
            senders = dict(message.from_)
            if search_line in (*senders.keys(), *senders.values()): return True
        elif cls._search_mode_is(search_mode, 'to'):
            receivers = dict(message.to)
            if search_line in (*receivers.keys(), *receivers.values()): return True
        elif cls._search_mode_is(search_mode, 'subject'):
            if search_line in message.subject: return True
        elif cls._search_mode_is(search_mode, 'attachments'):
            for attachment in message.attachments:
                if search_line in attachment['filename']: return True
        else:
            if search_line in message.text_html or search_line in message.text_plain:
                return True
        return False

    @classmethod
    def file_check(cls, file: PathLike, search_line: str, search_mode: EMLSearchMode, **kwargs):
        cls._test_kwargs(kwargs)
        return cls._message_check(cls.Message(file), search_line, search_mode)

    @classmethod
    def message_check(cls, message: LocalFileFinder.Message, search_line: str, search_mode: EMLSearchMode, **kwargs):
        cls._test_kwargs(kwargs)
        return cls._message_check(message, search_line, search_mode)

    def search(self, search_line: str, search_mode: EMLSearchMode, **kwargs):
        self._test_kwargs(kwargs)
        if not os.path.isdir(self.directory):
            raise FileNotFoundError(self.directory)
        for message in self.all():
            if self._message_check(message, search_line, search_mode): yield message

    def search_all(self, search_line: str, search_mode: EMLSearchMode, **kwargs) -> list[Message]:
        return list(self.search(search_line, search_mode, **kwargs))

    def all(self):
        for eml_file in self.directory.rglob('*.eml'): yield self.Message(eml_file)
