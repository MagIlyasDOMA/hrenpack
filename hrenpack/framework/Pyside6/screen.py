from typing import Optional
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QStackedWidget, QWidget


class QScreenManager(QStackedWidget):
    def __init__(self, parent, *, currentIndex: Optional[int] = None, count: Optional[int] = None):
        super().__init__(parent, currentIndex=currentIndex, count=count)
        self._ui_loader = QUiLoader()

    def add_screen(self, screen):
        if isinstance(screen, type):
            if not issubclass(screen, QWidget):
                class Screen(QWidget, screen):
                    pass
            else:
                Screen = screen
            screen = Screen()
        if not isinstance(screen, QWidget):
            raise TypeError("screen is not a QWidget")
        self.addWidget(screen)

