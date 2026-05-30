"""
Predefined file dialog templates for PySide6 applications.

Provides common file type filters for QFileDialog.

Предопределенные шаблоны диалогов файлов для приложений PySide6.

Предоставляет общие фильтры типов файлов для QFileDialog.
"""

from hrenpack.classes import DictObject

file_dialog_templates = DictObject(
    dict(
        images="Images (*.jpg *.jpeg *.png *.tif *.tiff)",
        all="All files (*)",
        txt="Text document (*.txt)",
        srt="SRT subtitles (*.srt)"
    )
)
"""
File dialog filter templates.

Шаблоны фильтров диалога файлов.

Example:
    from hrenpack.framework.Pyside6.variables import file_dialog_templates

    filename = QFileDialog.getOpenFileName(
        parent, 
        "Open File", 
        "/", 
        file_dialog_templates.images
    )
"""
