from typing import Optional, Union
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QStackedWidget, QWidget
from hrenpack.typings import NullStr


class QScreenManager(QStackedWidget):
    def __init__(self, parent, *, currentIndex: Optional[int] = None, count: Optional[int] = None):
        super().__init__(parent, currentIndex=currentIndex, count=count)
        self._screens = dict()
        self._ui_loader = QUiLoader()
        self._default_screen: NullStr = None
        self._current_screen: NullStr = None

    def add_screen(self, screen: Union[type, QWidget], name: str, setup_ui: bool = True):
        if isinstance(screen, type):
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
        self._screens[name] = screen

    def remove_screen(self, name: str):
        screen = self._screens.get(name)
        if screen:
            self.removeWidget(screen)
            del self._screens[name]

    @property
    def all_screens(self):
        return self._screens

    @property
    def current_screen(self):
        return self._screens[self._current_screen]

    @property
    def current_screen_name(self):
        return self._current_screen

    @current_screen.setter
    def current_screen(self, name: str):
        self._current_screen = name
        self.setCurrentWidget(self._screens[self._current_screen])
