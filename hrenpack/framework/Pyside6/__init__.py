import os
import sys
from glob import glob
from typing import Union, Optional
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pathlike_typing import PathLike
from hrenpack.listwork import split_list
from hrenpack.framework.Pyside6.variables import file_dialog_templates


def messagebox(title: str, message: str, icon: Union[QIcon, str, None] = None):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)

    if icon is not None:
        icon = icon if type(icon) is QIcon else QIcon(icon)
        msg.setWindowIcon(icon)

    msg.exec()


def remove_text_and_stylesheet(widget: QWidget):
    widget.setStyleSheet("")
    try:
        widget.setText("")
    except AttributeError:
        pass


def objects_enable(*objects: QObject):
    for o in objects:
        o.setEnabled(True)


def objects_disable(*objects: QObject):
    for o in objects:
        o.setEnabled(False)


def exit(window: QWidget) -> None:
    window.close()
    sys.exit(0)


def file_dialog_read(parent, *file_types: str, title: str = "Выберите файл", directory: str = '/',
                     selected_filter: int = 0, all_files: bool = True) -> Optional[str]:
    file_types = list(file_types)
    if all_files:
        file_types.append(file_dialog_templates.all)
    dialog = QFileDialog()
    options = dialog.options()
    filters = split_list(file_types, ';;')
    sf = file_types[selected_filter]
    filename = dialog.getOpenFileName(parent, title, directory, filters, sf, options)[0]
    return filename if filename else None


def file_dialog_save(parent, *file_types: str, title: str = "Выберите файл", directory: str = '/',
                     selected_filter: int = 0, all_files: bool = True) -> Optional[str]:
    file_types = list(file_types)
    if all_files:
        file_types.append(file_dialog_templates.all)
    dialog = QFileDialog()
    options = dialog.options()
    filters = split_list(file_types, ';;')
    sf = file_types[selected_filter]
    filename = dialog.getSaveFileName(parent, title, directory, filters, sf, options)[0]
    return filename


def add_fonts(directory: PathLike, root_only: bool = False):
    fonts = glob(f'{directory}/*.otf') + glob(f'{directory}/*.ttf')
    if not root_only:
        fonts += glob(f'{directory}/static/*.otf') + glob(f'{directory}/static/*.ttf')
    for font in fonts:
        QFontDatabase.addApplicationFont(font)
