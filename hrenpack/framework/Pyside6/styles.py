from typing import Optional
from PySide6.QtWidgets import QWidget
from hrenpack.typings import ThemeType
from hrenpack.windows_registry import get_system_theme


def hren_styles(widget: QWidget, theme: Optional[ThemeType] = None, selective: bool = False):
    if not theme: theme = get_system_theme()
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
