import warnings
from typing import Optional, Union
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QStackedWidget, QWidget, QMainWindow, QDialog
from hrenpack.kwargswork import exclude_nones
from hrenpack.typings import NullStr


class QScreenManager(QStackedWidget):
    def __init__(self, parent=None, *, currentIndex: Optional[int] = None, count: Optional[int] = None):
        super().__init__(parent, **exclude_nones(currentIndex=currentIndex, count=count))
        self._screens = dict()
        self._ui_loader = QUiLoader()
        self._default_screen_name: NullStr = None
        self._current_screen_name: NullStr = None

    def add_screen(self, screen: Union[type, QWidget], name: str, setup_ui: bool = True):
        if isinstance(screen, type):
            if not setup_ui:
                warnings.warn(
                    'The setup_ui argument is ignored if a class rather than an object is passed as the screen argument.',
                    UserWarning, 2
                )
            if not issubclass(screen, QWidget):
                class Screen(QWidget, screen):
                    pass
            else:
                Screen = screen
            screen = Screen()
            screen.setupUi(screen)
        if not isinstance(screen, QWidget):
            raise TypeError("screen is not a QWidget")
        self.addWidget(screen)
        screen.name = name
        if setup_ui: screen.setupUi(screen)
        is_empty = not bool(self._screens)
        self._screens[name] = screen
        if is_empty:
            self.default_screen = name
            self.current_screen = name

    def remove_screen(self, name: str):
        screen = self._screens.get(name)
        if screen:
            self.removeWidget(screen)
            del self._screens[name]

    @property
    def all_screens(self) -> dict[str, QWidget]:
        return self._screens

    @property
    def current_screen(self) -> QWidget:
        return self._screens[self._current_screen_name]

    @property
    def current_screen_name(self) -> str:
        return self._current_screen_name

    @current_screen.setter
    def current_screen(self, name: str):
        self._current_screen_name = name
        self.setCurrentWidget(self._screens[name])

    @property
    def default_screen(self) -> QWidget:
        return self._screens[self._default_screen_name]

    @property
    def default_screen_name(self) -> str:
        return self._default_screen_name

    @default_screen.setter
    def default_screen(self, name: str):
        self._default_screen_name = name

    def default(self):
        self.current_screen = self.default_screen_name


class ScreenWindowMixin:
    def __init__(self, *args, **kwargs):
        self._screen_manager = QScreenManager(self)

    def add_screen(self, screen: Union[type, QWidget], name: str, setup_ui: bool = True):
        self._screen_manager.add_screen(screen, name, setup_ui)

    def remove_screen(self, name: str):
        self._screen_manager.remove_screen(name)

    @property
    def all_screens(self) -> dict[str, QWidget]:
        return self._screen_manager.all_screens

    @property
    def current_screen(self) -> QWidget:
        return self._screen_manager.current_screen

    @property
    def current_screen_name(self) -> str:
        return self._screen_manager.current_screen_name

    @current_screen.setter
    def current_screen(self, name: str):
        self._screen_manager.current_screen = name

    @property
    def default_screen(self) -> QWidget:
        return self._screen_manager.default_screen

    @property
    def default_screen_name(self) -> str:
        return self._screen_manager.default_screen_name

    @default_screen.setter
    def default_screen(self, name: str):
        self._screen_manager.default_screen = name

    def default(self):
        self._screen_manager.default()


class QScreenWindow(ScreenWindowMixin, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        ScreenWindowMixin.__init__(self)


class QScreenMainWindow(ScreenWindowMixin, QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        ScreenWindowMixin.__init__(self)


class QScreenDialog(ScreenWindowMixin, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        ScreenWindowMixin.__init__(self)
