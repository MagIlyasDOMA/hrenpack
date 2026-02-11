from typing import Optional
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QStackedWidget


class QScreenWidget(QStackedWidget):
    def __init__(self, parent, *, currentIndex: Optional[int] = None, count: Optional[int] = None):
        super().__init__(parent, currentIndex=currentIndex, count=count)
        self._ui_loader = QUiLoader()

    def
