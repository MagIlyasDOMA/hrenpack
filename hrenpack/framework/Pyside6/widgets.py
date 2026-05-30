"""
Custom PySide6 widgets.

Provides BackgroundRubberBand for custom-styled rubber band selection.

Пользовательские виджеты PySide6.

Предоставляет BackgroundRubberBand для выбора области с пользовательскими стилями.
"""

from typing import Optional
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import *
from pyqtcli import QCLIApplication
from hrenpack import ColorTyping


class BackgroundRubberBand(QRubberBand):
    """
    QRubberBand with custom background and border colors.

    QRubberBand с пользовательскими цветами фона и границы.

    Args:
        shape: Rubber band shape (QRubberBand.Rectangle or QRubberBand.Line) / Форма резиновой ленты
        parent: Parent widget / Родительский виджет
        background (Optional[ColorTyping]): RGB or RGBA background color / Цвет фона
        frameground (Optional[ColorTyping]): RGB or RGBA border color / Цвет границы

    Example:
        rubber_band = BackgroundRubberBand(
            QRubberBand.Rectangle,
            self,
            background=(100, 100, 255, 100),  # Semi-transparent blue
            frameground=(0, 0, 255)  # Solid blue border
        )
    """

    def __init__(self, shape, parent=None,
                 background: Optional[ColorTyping] = None,
                 frameground: Optional[ColorTyping] = None):
        super().__init__(shape, parent)
        self.background = background
        self.frameground = frameground

    def paintEvent(self, event):
        """
        Custom paint event with background and border.

        Пользовательское событие отрисовки с фоном и границей.

        Args:
            event: Paint event / Событие отрисовки
        """
        painter = QPainter(self)
        if self.background:
            background_color = QColor(*self.background)
            painter.fillRect(self.rect(), background_color)

        if self.frameground:
            border_color = QColor(*self.frameground)
            painter.setPen(border_color)
            painter.drawRect(self.rect())
