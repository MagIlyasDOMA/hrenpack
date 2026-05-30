"""
HTML sanitization utilities for security.

Provides HTMLSanitizer class to remove dangerous tags, attributes, and scripts.

Утилиты для санитизации HTML в целях безопасности.

Предоставляет класс HTMLSanitizer для удаления опасных тегов, атрибутов и скриптов.
"""

import re
from typing import Optional
from bs4 import BeautifulSoup, Comment


class HTMLSanitizer:
    """
    HTML sanitizer that removes dangerous content.

    Санитайзер HTML, удаляющий опасное содержимое.

    Args:
        html_content (Optional[str]): HTML content to sanitize / HTML содержимое для очистки
    """

    def __init__(self, html_content: Optional[str] = None):
        self.html_content = html_content

        # List of dangerous tags
        self.dangerous_tags = [
            'script', 'iframe', 'frame', 'frameset', 'object', 'embed',
            'applet', 'video', 'audio', 'canvas', 'form', 'input',
            'textarea', 'select', 'button', 'link', 'meta', 'base',
            'style'  # style removed as we'll clean CSS separately
        ]

        # Dangerous protocols in links
        self.dangerous_protocols = ['javascript:', 'data:', 'vbscript:']

        # Dangerous CSS properties
        self.dangerous_css_properties = [
            'position', 'top', 'right', 'bottom', 'left', 'z-index',
            'float', 'flex', 'grid', 'overflow', 'opacity', 'transform',
            'transition', 'animation', 'box-shadow', 'text-shadow',
            'background-image', 'background-attachment', 'background-size',
            'content', 'cursor', 'pointer-events', 'filter'
        ]

        # Event handlers to remove
        self.event_handlers = [
            'onclick', 'ondblclick', 'onmousedown', 'onmousemove',
            'onmouseout', 'onmouseover', 'onmouseup', 'onkeydown',
            'onkeypress', 'onkeyup', 'onload', 'onerror', 'onfocus',
            'onblur', 'onsubmit', 'onreset', 'onchange', 'onselect'
        ]

    def sanitize_css(self, style_value):
        """
        Clean CSS properties, removing dangerous ones.

        Очищает CSS свойства, удаляя опасные.

        Args:
            style_value: CSS string to clean / Строка CSS для очистки

        Returns:
            str: Cleaned CSS / Очищенный CSS
        """
        if not style_value:
            return ""

        # Split CSS into individual rules
        rules = style_value.split(';')
        safe_rules = []

        for rule in rules:
            rule = rule.strip()
            if not rule:
                continue

            # Check if rule contains dangerous property
            dangerous = False
            for prop in self.dangerous_css_properties:
                if rule.lower().startswith(prop):
                    dangerous = True
                    break

            if not dangerous:
                safe_rules.append(rule)

        return '; '.join(safe_rules)

    def sanitize_url(self, url):
        """
        Check and clean URL, replacing dangerous protocols with '#'.

        Проверяет и очищает URL, заменяя опасные протоколы на '#'.

        Args:
            url: URL to sanitize / URL для очистки

        Returns:
            str: Sanitized URL or '#' for dangerous / Очищенный URL или '#' для опасных
        """
        if not url:
            return ""

        url_lower = url.lower().strip()
        for protocol in self.dangerous_protocols:
            if url_lower.startswith(protocol):
                return "#"  # Replace dangerous links with empty link

        return url

    def sanitize_html(self, html_content):
        """
        Main HTML sanitization method.

        Основной метод очистки HTML.

        Args:
            html_content: HTML content to sanitize / HTML содержимое для очистки

        Returns:
            str: Sanitized HTML / Очищенный HTML
        """
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. Remove dangerous tags
        for tag in self.dangerous_tags:
            for element in soup.find_all(tag):
                element.decompose()

        # 2. Process remaining tags
        for tag in soup.find_all(True):  # True means all tags
            # Remove event handlers
            for event in self.event_handlers:
                if tag.has_attr(event):
                    del tag[event]

            # Clean href and src attributes
            if tag.has_attr('href'):
                tag['href'] = self.sanitize_url(tag['href'])

            if tag.has_attr('src'):
                tag['src'] = self.sanitize_url(tag['src'])

            # Clean CSS in style attribute
            if tag.has_attr('style'):
                tag['style'] = self.sanitize_css(tag['style'])

        # 3. Remove comments (may contain dangerous code)
        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        return str(soup)

    def sanitize(self):
        """
        Sanitize the html_content passed during initialization.

        Очищает html_content, переданный при инициализации.

        Returns:
            str: Sanitized HTML / Очищенный HTML
        """
        return self.sanitize_html(self.html_content)

    def __call__(self, html_content):
        """
        Allow calling instance as a function.

        Позволяет вызывать экземпляр как функцию.

        Args:
            html_content: HTML content to sanitize / HTML содержимое для очистки

        Returns:
            str: Sanitized HTML / Очищенный HTML
        """
        return self.sanitize_html(html_content)
