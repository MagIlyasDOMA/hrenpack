"""
PySide6 stylesheet utilities.

Provides hren_styles function for applying consistent light/dark theme styles.

Утилиты стилей PySide6.

Предоставляет функцию hren_styles для применения единообразных стилей светлой/темной темы.
"""

from typing import Optional
from PySide6.QtWidgets import QWidget
from hrenpack.typings import ThemeType
from hrenpack.windows_registry import get_system_theme


def hren_styles(widget: QWidget, theme: Optional[ThemeType] = None, selective: bool = False):
    """
    Apply Hrenpack default styles to widget.

    Применяет стандартные стили Hrenpack к виджету.

    Args:
        widget (QWidget): Widget to style / Виджет для стилизации
        theme (Optional[ThemeType]): 'light' or 'dark', auto-detected if None / 'light' или 'dark'
        selective (bool): Apply background only to specific widgets (QMainWindow, QDialog, QWidget:window), default False / Применять фон только к определенным виджетам

    Example:
        class MyWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                hren_styles(self)  # Auto-detect system theme

        # Force dark theme
        hren_styles(my_widget, theme='dark')

        # Selective mode for better performance
        hren_styles(self, selective=True)
    """
    if not theme:
        theme = get_system_theme()
    styles = dict(background='#ededed', foreground='#121212', button='#121212') if theme == 'light' \
        else dict(background='#202020', foreground='#ededed', button='#ededed')
    styles['widgets'] = 'QMainWindow, QDialog, QWidget:window' if selective else 'QWidget'
    widget.setStyleSheet('''{widgets} {{
    background: {background};
}}

QWidget {{
    color: {foreground};
}}

QPushButton {{
    background: {button};
    color: {background};
    border: none;
	border-radius: 10px;
}}
'''.format(**styles))
