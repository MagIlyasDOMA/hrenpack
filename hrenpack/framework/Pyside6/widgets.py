# Hrenpack v2.1.2
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from typing import Optional
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from hrenpack import ColorTyping


class BackgroundRubberBand(QRubberBand):
    def __init__(self, shape, parent=None,
                 background: Optional[ColorTyping] = None,
                 frameground: Optional[ColorTyping] = None):
        super().__init__(shape, parent)
        self.background = background
        self.frameground = frameground

    def paintEvent(self, event):
        painter = QPainter(self)
        background_color = QColor(*self.background)
        painter.fillRect(self.rect(), background_color)

        border_color = QColor(*self.frameground)
        painter.setPen(border_color)
        painter.drawRect(self.rect())
