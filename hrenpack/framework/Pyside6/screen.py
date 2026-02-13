import warnings
from typing import Optional, Union
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QStackedWidget, QWidget, QMainWindow, QDialog, QVBoxLayout, QFrame
from hrenpack.kwargswork import exclude_nones
from hrenpack.typings import NullStr


class QScreenManager(QStackedWidget):
    def __init__(self, parent=None, *, currentIndex: Optional[int] = None, count: Optional[int] = None,
                 dont_change_geometry: bool = False, dont_change_title: bool = False):
        super().__init__(parent, **exclude_nones(currentIndex=currentIndex, count=count))
        self._screens: dict[str, QWidget] = dict()
        self._dont_change_geometry = dont_change_geometry
        self._dont_change_title = dont_change_title
        self._ui_loader = QUiLoader()
        self._default_screen_name: NullStr = None
        self._current_screen_name: NullStr = None
        self.__parent = self.parent()

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

    def screen_resize(self):
        if self._screens and not self._dont_change_geometry:
            self._parent.resize(self.current_screen.size())

    def screen_set_title(self):
        if self._screens and not self._dont_change_title:
            self._parent.setWindowTitle(self.current_screen.windowTitle())

    def screen_update(self):
        self.screen_resize()
        self.screen_set_title()

    @current_screen.setter
    def current_screen(self, name: str):
        self._current_screen_name = name
        self.setCurrentWidget(self._screens[name])
        self.screen_resize()
        self.screen_set_title()

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

    @property
    def _parent(self) -> QWidget:
        return self.__parent

    @_parent.setter
    def _parent(self, parent: QWidget):
        self.__parent = parent
        self.screen_update()


class ScreenWindowMixin:
    def __init__(self, *args,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False,
                 **kwargs):
        self._central_widget = QVBoxLayout()
        self._dont_change_geometry = dont_change_geometry
        self._dont_change_title = dont_change_title

        if create_additional_container:
            self._container = QFrame()
            self._container_layout = QVBoxLayout()
            container = self._container
            layout = self._container_layout
            container.setLayout(layout)
            self._central_widget.addWidget(container)
        else:
            container = self
            layout = self._central_widget

        self._screen_manager = QScreenManager(container)
        self._screen_manager._parent = self
        self.setLayout(self._central_widget)
        layout.addWidget(self._screen_manager)

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
    def __init__(self, parent=None, *,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False):
        QWidget.__init__(self, parent)
        ScreenWindowMixin.__init__(
            self, dont_change_geometry=dont_change_geometry,
            dont_change_title=dont_change_title,
            create_additional_container=create_additional_container
        )


class QScreenMainWindow(ScreenWindowMixin, QMainWindow):
    def __init__(self, parent=None, *,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False):
        QMainWindow.__init__(self, parent)
        ScreenWindowMixin.__init__(
            self, dont_change_geometry=dont_change_geometry,
            dont_change_title=dont_change_title,
            create_additional_container=create_additional_container
        )


class QScreenDialog(ScreenWindowMixin, QDialog):
    def __init__(self, parent=None, *,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False):
        QDialog.__init__(self, parent)
        ScreenWindowMixin.__init__(
            self, dont_change_geometry=dont_change_geometry,
            dont_change_title=dont_change_title,
            create_additional_container=create_additional_container
        )
