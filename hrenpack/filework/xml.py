"""
XML/HTML file handling with BeautifulSoup integration.

Provides XMLParser, ParserMixin, and file classes for XML/HTML manipulation.

Обработка XML/HTML файлов с интеграцией BeautifulSoup.

Предоставляет XMLParser, ParserMixin и классы файлов для манипуляции XML/HTML.
"""

from typing import Callable, Optional, Union
from bs4 import BeautifulSoup
from hrenpack.filework import TextFile


def xml_save(func: Callable):
    """
    Decorator that auto-saves after method execution.

    Декоратор, автоматически сохраняющий после выполнения метода.

    Args:
        func: Method to decorate / Метод для декорирования

    Returns:
        callable: Wrapped method / Обернутый метод
    """

    def wrapper(self, *args, **kwargs):
        output = func(self, *args, **kwargs)
        # Avoid calling save if the method is save itself or prettify
        if func.__name__ not in ['save', 'prettify']:
            self.save()
        return output

    return wrapper


class XMLParser(BeautifulSoup):
    """
    Extended BeautifulSoup with tag deletion.

    Расширенный BeautifulSoup с удалением тегов.

    Args:
        markup: HTML/XML markup / Разметка HTML/XML
        features: Parser features / Особенности парсера
        builder: Tree builder / Построитель дерева
        parse_only: Parse only specific content / Парсить только определенное содержимое
        from_encoding: Source encoding / Исходная кодировка
        exclude_encodings: Encodings to exclude / Кодировки для исключения
        element_classes: Custom element classes / Пользовательские классы элементов
        **kwargs: Additional arguments / Дополнительные аргументы
    """

    def __init__(self, markup: str, features=None, builder=None, parse_only=None, from_encoding=None,
                 exclude_encodings=None, element_classes=None, **kwargs):
        super().__init__(markup, features, builder, parse_only, from_encoding,
                         exclude_encodings, element_classes, **kwargs)

    def del_tag(self, item: str):
        """
        Delete all tags with given name.

        Удаляет все теги с указанным именем.

        Args:
            item (str): Tag name to delete / Имя тега для удаления

        Returns:
            list: Deleted tags / Удаленные теги
        """
        tags = self.find_all(item)
        for tag in tags:
            tag.decompose()
        return tags


class ParserMixin:
    """
    Mixin that adds BeautifulSoup methods with auto-save.

    Примесь, добавляющая методы BeautifulSoup с автосохранением.

    Attributes:
        parser (XMLParser): XML/HTML parser / Парсер XML/HTML
    """
    parser: XMLParser

    @xml_save
    def append(self, tag):
        return self.parser.append(tag)

    @xml_save
    def childGenerator(self):
        return self.parser.childGenerator()

    @xml_save
    def clear(self, decompose=False):
        return self.parser.clear(decompose)

    @xml_save
    def copy_self(self):
        return self.parser.copy_self()

    @xml_save
    def decode(self, indent_level=None, eventual_encoding='utf-8', formatter='minimal', iterator=None, **kwargs):
        return self.parser.decode(indent_level, eventual_encoding, formatter, iterator, **kwargs)

    @xml_save
    def decode_contents(self, indent_level=None, eventual_encoding='utf-8', formatter='minimal'):
        return self.parser.decode_contents(indent_level, eventual_encoding, formatter)

    @xml_save
    def decompose(self):
        return self.parser.decompose()

    @xml_save
    def encode(self, encoding='utf-8', indent_level=None, formatter='minimal', errors="xmlcharrefreplace"):
        return self.parser.encode(encoding, indent_level, formatter, errors)

    @xml_save
    def encode_contents(self, indent_level=None, encoding='utf-8', formatter='minimal'):
        return self.parser.encode_contents(indent_level, encoding, formatter)

    @xml_save
    def endData(self, container_class=None):
        return self.parser.endData(container_class)

    @xml_save
    def extend(self, tags):
        return self.parser.extend(tags)

    @xml_save
    def extract(self, _self_index=None):
        return self.parser.extract(_self_index)

    def find(self, name=None, attrs=None, recursive=True, string=None, **kwargs):
        """
        Find first matching tag.

        Находит первый подходящий тег.
        """
        if attrs is None:
            attrs = {}
        return self.parser.find(name, attrs, recursive, string, **kwargs)

    def find_all(self, name=None, attrs=None, recursive: bool = True, string=None, limit: Optional[int] = None,
                 _stacklevel: int = 2, **kwargs):
        """
        Find all matching tags.

        Находит все подходящие теги.
        """
        if attrs is None:
            attrs = {}
        return self.parser.findAll(name, attrs, recursive, string, limit, _stacklevel, **kwargs)

    # Many more BeautifulSoup methods wrapped with @xml_save...

    @xml_save
    def del_tag(self, item):
        """Delete tags by name."""
        return self.parser.del_tag(item)


class ExtensibleMarkupLanguageFile(ParserMixin, TextFile):
    """
    XML file handler with BeautifulSoup integration.

    Обработчик XML файлов с интеграцией BeautifulSoup.

    Args:
        path (str): Path to XML file / Путь к XML файлу
        encoding (Union[str, int]): File encoding, default 'utf-8' / Кодировка файла
        **kwargs: Additional arguments for TextFile / Дополнительные аргументы
    """
    _default_parser: str = 'xml'

    def __init__(self, path: str, encoding: Union[str, int] = 'utf-8', **kwargs):
        super().__init__(path, encoding, **kwargs)
        self.parser = XMLParser(self.read(), kwargs.get('parser', self._default_parser))

    def save(self):
        """
        Save changes to file.

        Сохраняет изменения в файл.
        """
        self.rewrite(self.parser.prettify())


class HyperTextMarkupLanguageFile(ExtensibleMarkupLanguageFile):
    """
    HTML file handler with BeautifulSoup integration.

    Обработчик HTML файлов с интеграцией BeautifulSoup.
    """
    _default_parser = 'html.parser'
