"""
File system utilities for Pyside6 applications.

Provides functions for file dialogs, font loading, and widget manipulation.

Утилиты файловой системы для приложений Pyside6.

Предоставляет функции для диалогов файлов, загрузки шрифтов и манипуляции виджетами.
"""

import os
import sys
from glob import glob
from typing import Union, Optional
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pathlike_typing import PathLike
from hrenpack.framework.Pyside6.variables import file_dialog_templates


def messagebox(title: str, message: str, icon: Union[QIcon, str, None] = None):
    """
    Show a message box.

    Показывает окно сообщения.

    Args:
        title (str): Window title / Заголовок окна
        message (str): Message text / Текст сообщения
        icon (Union[QIcon, str, None]): Window icon, optional / Иконка окна
    """
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)

    if icon is not None:
        icon = icon if type(icon) is QIcon else QIcon(icon)
        msg.setWindowIcon(icon)

    msg.exec()


def remove_text_and_stylesheet(widget: QWidget):
    """
    Remove text and stylesheet from widget.

    Удаляет текст и стили из виджета.

    Args:
        widget (QWidget): Widget to clear / Виджет для очистки
    """
    widget.setStyleSheet("")
    try:
        widget.setText("")
    except AttributeError:
        pass


def objects_enable(*objects: QObject):
    """
    Enable multiple Qt objects.

    Включает несколько Qt объектов.

    Args:
        *objects: Qt objects to enable / Qt объекты для включения
    """
    for o in objects:
        o.setEnabled(True)


def objects_disable(*objects: QObject):
    """
    Disable multiple Qt objects.

    Отключает несколько Qt объектов.

    Args:
        *objects: Qt objects to disable / Qt объекты для отключения
    """
    for o in objects:
        o.setEnabled(False)


def exit(window: QWidget) -> None:
    """
    Close window and exit application.

    Закрывает окно и завершает приложение.

    Args:
        window (QWidget): Window to close / Окно для закрытия
    """
    window.close()
    sys.exit(0)


def file_dialog_read(parent, *file_types: str, title: str = "Select file", directory: str = '/',
                     selected_filter: int = 0, all_files: bool = True) -> Optional[str]:
    """
    Open file dialog for reading.

    Открывает диалог выбора файла для чтения.

    Args:
        parent: Parent widget / Родительский виджет
        *file_types: File type filters (e.g., "Images (*.png *.jpg)") / Фильтры типов файлов
        title (str): Dialog title / Заголовок диалога
        directory (str): Initial directory / Начальная директория
        selected_filter (int): Index of initially selected filter / Индекс выбранного фильтра
        all_files (bool): Add "All files (*)" option, default True / Добавить опцию "Все файлы (*)"

    Returns:
        Optional[str]: Selected file path or None if cancelled / Путь к выбранному файлу
    """
    file_types = list(file_types)
    if all_files:
        file_types.append(file_dialog_templates.all)
    dialog = QFileDialog()
    options = dialog.options()
    filters = ';;'.join(file_types)
    sf = file_types[selected_filter]
    filename = dialog.getOpenFileName(parent, title, directory, filters, sf, options)[0]
    return filename if filename else None


def file_dialog_save(parent, *file_types: str, title: str = "Select file", directory: str = '/',
                     selected_filter: int = 0, all_files: bool = True) -> Optional[str]:
    """
    Open file dialog for saving.

    Открывает диалог выбора файла для сохранения.

    Args:
        parent: Parent widget / Родительский виджет
        *file_types: File type filters / Фильтры типов файлов
        title (str): Dialog title / Заголовок диалога
        directory (str): Initial directory / Начальная директория
        selected_filter (int): Index of initially selected filter / Индекс выбранного фильтра
        all_files (bool): Add "All files (*)" option, default True / Добавить опцию "Все файлы (*)"

    Returns:
        Optional[str]: Selected file path or None if cancelled / Путь к выбранному файлу
    """
    file_types = list(file_types)
    if all_files:
        file_types.append(file_dialog_templates.all)
    dialog = QFileDialog()
    options = dialog.options()
    filters = ';;'.join(file_types)
    sf = file_types[selected_filter]
    filename = dialog.getSaveFileName(parent, title, directory, filters, sf, options)[0]
    return filename


def add_fonts(directory: PathLike, root_only: bool = False):
    """
    Add fonts from directory to application.

    Добавляет шрифты из директории в приложение.

    Args:
        directory (PathLike): Directory containing font files / Директория с файлами шрифтов
        root_only (bool): Only search root directory, not 'static' subfolder, default False / Искать только в корневой директории
    """
    fonts = glob(f'{directory}/*.otf') + glob(f'{directory}/*.ttf')
    if not root_only:
        fonts += glob(f'{directory}/static/*.otf') + glob(f'{directory}/static/*.ttf')
    for font in fonts:
        QFontDatabase.addApplicationFont(font)
