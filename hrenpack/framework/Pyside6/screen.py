"""
Screen management for PySide6 applications.

Provides QScreenManager and screen window classes for managing multiple screens
with automatic window resizing and title updates.

Управление экранами для приложений PySide6.

Предоставляет QScreenManager и классы окон для управления несколькими экранами
с автоматическим изменением размера окна и обновлением заголовка.
"""

import warnings
from typing import Optional, Union
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QStackedWidget, QWidget, QMainWindow, QDialog, QVBoxLayout, QFrame
from hrenpack.kwargswork import exclude_nones
from hrenpack.typings import NullStr


class QScreenManager(QStackedWidget):
    """
    Screen manager for PySide6 applications with automatic window adaptation.

    Менеджер экранов для приложений PySide6 с автоматической адаптацией окна.

    Args:
        parent: Parent widget / Родительский виджет
        currentIndex (Optional[int]): Initial screen index / Начальный индекс экрана
        count (Optional[int]): Initial screen count / Начальное количество экранов
        dont_change_geometry (bool): Prevent window resizing, default False / Запретить изменение размера окна
        dont_change_title (bool): Prevent window title updates, default False / Запретить обновление заголовка окна
        fixed_size (bool): Use setFixedSize instead of resize, default False / Использовать setFixedSize вместо resize
    """

    def __init__(self, parent=None, *, currentIndex: Optional[int] = None, count: Optional[int] = None,
                 dont_change_geometry: bool = False, dont_change_title: bool = False, **kwargs):
        super().__init__(parent, **exclude_nones(currentIndex=currentIndex, count=count))
        self._screens: dict[str, QWidget] = dict()
        self._dont_change_geometry = dont_change_geometry
        self._dont_change_title = dont_change_title
        self._ui_loader = QUiLoader()
        self._default_screen_name: NullStr = None
        self._current_screen_name: NullStr = None
        self._is_fixed_size = kwargs.get('fixed_size', False)
        self.__parent = self.parent()

    def add_screen(self, screen: Union[type, QWidget], name: str, setup_ui: bool = True):
        """
        Add a screen to the manager.

        Добавляет экран в менеджер.

        Args:
            screen (Union[type, QWidget]): Screen class or instance / Класс или экземпляр экрана
            name (str): Unique screen name / Уникальное имя экрана
            setup_ui (bool): Call setupUi on the screen, default True / Вызвать setupUi для экрана

        Raises:
            TypeError: If screen is not a QWidget / Если screen не является QWidget
        """
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
        if setup_ui:
            screen.setupUi(screen)
        is_empty = not bool(self._screens)
        self._screens[name] = screen
        if is_empty:
            self.default_screen = name
            self.current_screen = name

    def remove_screen(self, name: str):
        """
        Remove a screen from the manager.

        Удаляет экран из менеджера.

        Args:
            name (str): Screen name to remove / Имя экрана для удаления
        """
        screen = self._screens.get(name)
        if screen:
            self.removeWidget(screen)
            del self._screens[name]

    @property
    def all_screens(self) -> dict[str, QWidget]:
        """Get all screens as dictionary."""
        return self._screens

    @property
    def current_screen(self) -> QWidget:
        """Get current screen widget."""
        return self._screens[self._current_screen_name]

    @property
    def current_screen_name(self) -> str:
        """Get current screen name."""
        return self._current_screen_name

    def screen_resize(self):
        """Resize parent window to match current screen size."""
        if self._screens and not self._dont_change_geometry:
            resize = self._parent.resize if not self._is_fixed_size else self._parent.setFixedSize
            resize(self.current_screen.size())

    def screen_set_title(self):
        """Set parent window title from current screen."""
        if self._screens and not self._dont_change_title:
            self._parent.setWindowTitle(self.current_screen.windowTitle())

    def screen_update(self):
        """Update both size and title."""
        self.screen_resize()
        self.screen_set_title()

    @current_screen.setter
    def current_screen(self, name: str):
        """Set current screen by name."""
        self._current_screen_name = name
        self.setCurrentWidget(self._screens[name])
        self.screen_resize()
        self.screen_set_title()

    @property
    def default_screen(self) -> QWidget:
        """Get default screen widget."""
        return self._screens[self._default_screen_name]

    @property
    def default_screen_name(self) -> str:
        """Get default screen name."""
        return self._default_screen_name

    @default_screen.setter
    def default_screen(self, name: str):
        """Set default screen by name."""
        self._default_screen_name = name

    def default(self):
        """Switch to default screen."""
        self.current_screen = self.default_screen_name

    @property
    def _parent(self) -> QWidget:
        """Get parent window."""
        return self.__parent

    @_parent.setter
    def _parent(self, parent: QWidget):
        """Set parent window."""
        self.__parent = parent
        self.screen_update()


class ScreenWindowMixin:
    """
    Mixin for windows with screen management support.

    Примесь для окон с поддержкой управления экранами.

    Args:
        dont_change_geometry (bool): Prevent window resizing / Запретить изменение размера окна
        dont_change_title (bool): Prevent window title updates / Запретить обновление заголовка
        create_additional_container (bool): Create separate container widget, default False / Создать отдельный виджет-контейнер
    """

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

        self._screen_manager = QScreenManager(container, **kwargs)
        self._screen_manager._parent = self
        self.setLayout(self._central_widget)
        layout.addWidget(self._screen_manager)

    def add_screen(self, screen: Union[type, QWidget], name: str, setup_ui: bool = True):
        """Add screen to manager."""
        self._screen_manager.add_screen(screen, name, setup_ui)

    def remove_screen(self, name: str):
        """Remove screen from manager."""
        self._screen_manager.remove_screen(name)

    @property
    def all_screens(self) -> dict[str, QWidget]:
        """Get all screens."""
        return self._screen_manager.all_screens

    @property
    def current_screen(self) -> QWidget:
        """Get current screen."""
        return self._screen_manager.current_screen

    @property
    def current_screen_name(self) -> str:
        """Get current screen name."""
        return self._screen_manager.current_screen_name

    @current_screen.setter
    def current_screen(self, name: str):
        """Set current screen."""
        self._screen_manager.current_screen = name

    @property
    def default_screen(self) -> QWidget:
        """Get default screen."""
        return self._screen_manager.default_screen

    @property
    def default_screen_name(self) -> str:
        """Get default screen name."""
        return self._screen_manager.default_screen_name

    @default_screen.setter
    def default_screen(self, name: str):
        """Set default screen."""
        self._screen_manager.default_screen = name

    def default(self):
        """Switch to default screen."""
        self._screen_manager.default()

    def show(self):
        """Show window, raising error if no screens."""
        if not self.all_screens:
            raise RuntimeError('Screen manager is empty')
        super().show()


class QScreenWindow(ScreenWindowMixin, QWidget):
    """
    QWidget with screen management support.

    QWidget с поддержкой управления экранами.
    """

    def __init__(self, parent=None, *,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False, **kwargs):
        QWidget.__init__(self, parent)
        ScreenWindowMixin.__init__(
            self, dont_change_geometry=dont_change_geometry,
            dont_change_title=dont_change_title,
            create_additional_container=create_additional_container,
            **kwargs
        )


class QScreenMainWindow(ScreenWindowMixin, QMainWindow):
    """
    QMainWindow with screen management support.

    QMainWindow с поддержкой управления экранами.
    """

    def __init__(self, parent=None, *,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False, **kwargs):
        QMainWindow.__init__(self, parent)
        ScreenWindowMixin.__init__(
            self, dont_change_geometry=dont_change_geometry,
            dont_change_title=dont_change_title,
            create_additional_container=create_additional_container,
            **kwargs
        )


class QScreenDialog(ScreenWindowMixin, QDialog):
    """
    QDialog with screen management support.

    QDialog с поддержкой управления экранами.
    """

    def __init__(self, parent=None, *,
                 dont_change_geometry: bool = False,
                 dont_change_title: bool = False,
                 create_additional_container: bool = False, **kwargs):
        QDialog.__init__(self, parent)
        ScreenWindowMixin.__init__(
            self, dont_change_geometry=dont_change_geometry,
            dont_change_title=dont_change_title,
            create_additional_container=create_additional_container,
            **kwargs
        )


class BaseScreen(QWidget):
    """
    Base class for screens with parent access.

    Базовый класс для экранов с доступом к родителю.
    """

    @property
    def _parent(self) -> QWidget:
        """Get parent screen manager's parent window."""
        return self.parent()._parent

    @property
    def parent_(self):
        """Alias for _parent."""
        return self._parent
