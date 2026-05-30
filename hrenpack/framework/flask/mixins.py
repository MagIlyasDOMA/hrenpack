"""
Flask application mixins for templates and static files.

Provides MultiTemplateAndStaticMixin for handling multiple template and static folders.

Примеси приложений Flask для шаблонов и статических файлов.

Предоставляет MultiTemplateAndStaticMixin для работы с несколькими папками шаблонов и статических файлов.
"""

import os
from flask import Blueprint, send_from_directory
from jinja2 import FileSystemLoader, ChoiceLoader

from hrenpack.typings import PathLike


class MultiTemplateAndStaticMixin:
    """
    Mixin for Flask applications that adds support for multiple template and static folders.

    Примесь для Flask приложений, добавляющая поддержку нескольких папок шаблонов и статических файлов.

    Example:
        class MyApp(MultiTemplateAndStaticMixin, Flask):
            def __init__(self, name):
                super().__init__(name)
                self.add_template_folder('custom_templates')
                self.add_static_folder('custom_static', 'assets')
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize mixin attributes.

        Инициализирует атрибуты примеси.
        """
        super().__init__(*args, **kwargs)
        self._template_folders = list()
        self._static_folders = list()
        self._static_folders_blueprints = list()

    def add_template_folder(self, folder_path: PathLike):
        """
        Add a template folder to the Jinja2 loader.

        Добавляет папку с шаблонами в загрузчик Jinja2.

        Args:
            folder_path (PathLike): Path to template folder / Путь к папке с шаблонами
        """
        if os.path.exists(folder_path) and folder_path not in self._template_folders:
            self._template_folders.append(str(folder_path))
            self._update_template_loader()

    def add_static_folder(self, name: str, folder_path: PathLike):
        """
        Add a static folder accessible via blueprint.

        Добавляет папку со статическими файлами через blueprint.

        Args:
            name (str): Blueprint name (also used for URL prefix) / Имя blueprint (также используется для URL)
            folder_path (PathLike): Path to static folder / Путь к папке со статическими файлами
        """
        if os.path.exists(folder_path) and folder_path not in self._static_folders:
            self._static_folders.append(str(folder_path))
            blueprint = Blueprint(name, self.import_name, static_folder=folder_path, static_url_path=f'/static/{name}')
            self._static_folders_blueprints.append(blueprint)
            self.register_blueprint(blueprint)

    def serve_static(self, filename):
        """
        Static file handler that searches all registered static folders.

        Обработчик для статических файлов, ищущий во всех зарегистрированных папках.

        Args:
            filename (str): Requested filename / Запрошенное имя файла

        Returns:
            Response: Static file response / Ответ со статическим файлом
        """
        # Search in additional folders
        for static_folder in self._static_folders:
            file_path = os.path.join(static_folder, filename)
            if os.path.exists(file_path):
                directory = os.path.dirname(file_path)
                actual_filename = os.path.basename(file_path)
                return send_from_directory(directory, actual_filename)

        # If not found, use Flask's default logic
        return super().send_static_file(filename)

    def _update_template_loader(self):
        """
        Update Jinja2 loader to include all template folders.

        Обновляет загрузчик шаблонов Jinja2 с учетом всех папок.
        """
        all_template_folders = [self.template_folder] + self._template_folders
        existing_folders = [f for f in all_template_folders if f and os.path.exists(f)]

        loaders = [FileSystemLoader(folder) for folder in existing_folders]
        if hasattr(self, 'jinja_loader') and self.jinja_loader:
            loaders.append(self.jinja_loader)

        self.jinja_loader = ChoiceLoader(loaders)
