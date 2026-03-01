import re
from typing import Optional
from bs4 import BeautifulSoup, Comment


class HTMLSanitizer:
    def __init__(self, html_content: Optional[str] = None):
        self.html_content = html_content

        # Список опасных тегов
        self.dangerous_tags = [
            'script', 'iframe', 'frame', 'frameset', 'object', 'embed',
            'applet', 'video', 'audio', 'canvas', 'form', 'input',
            'textarea', 'select', 'button', 'link', 'meta', 'base',
            'style'  # style удаляем, так как будем чистить CSS отдельно
        ]

        # Опасные протоколы в ссылках
        self.dangerous_protocols = ['javascript:', 'data:', 'vbscript:']

        # Опасные CSS-свойства
        self.dangerous_css_properties = [
            'position', 'top', 'right', 'bottom', 'left', 'z-index',
            'float', 'flex', 'grid', 'overflow', 'opacity', 'transform',
            'transition', 'animation', 'box-shadow', 'text-shadow',
            'background-image', 'background-attachment', 'background-size',
            'content', 'cursor', 'pointer-events', 'filter'
        ]

        # События, которые нужно удалить
        self.event_handlers = [
            'onclick', 'ondblclick', 'onmousedown', 'onmousemove',
            'onmouseout', 'onmouseover', 'onmouseup', 'onkeydown',
            'onkeypress', 'onkeyup', 'onload', 'onerror', 'onfocus',
            'onblur', 'onsubmit', 'onreset', 'onchange', 'onselect'
        ]

    def sanitize_css(self, style_value):
        """Очистка CSS-свойств"""
        if not style_value:
            return ""

        # Разбиваем CSS на отдельные правила
        rules = style_value.split(';')
        safe_rules = []

        for rule in rules:
            rule = rule.strip()
            if not rule:
                continue

            # Проверяем, содержит ли правило опасное свойство
            dangerous = False
            for prop in self.dangerous_css_properties:
                if rule.lower().startswith(prop):
                    dangerous = True
                    break

            if not dangerous:
                safe_rules.append(rule)

        return '; '.join(safe_rules)

    def sanitize_url(self, url):
        """Проверка и очистка URL"""
        if not url:
            return ""

        url_lower = url.lower().strip()
        for protocol in self.dangerous_protocols:
            if url_lower.startswith(protocol):
                return "#"  # Заменяем опасные ссылки на пустую ссылку

        return url

    def sanitize_html(self, html_content):
        """Основной метод очистки HTML"""
        # Парсим HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. Удаляем опасные теги
        for tag in self.dangerous_tags:
            for element in soup.find_all(tag):
                element.decompose()

        # 2. Обрабатываем оставшиеся теги
        for tag in soup.find_all(True):  # True означает все теги
            # Удаляем обработчики событий
            for event in self.event_handlers:
                if tag.has_attr(event):
                    del tag[event]

            # Очищаем атрибуты href и src
            if tag.has_attr('href'):
                tag['href'] = self.sanitize_url(tag['href'])

            if tag.has_attr('src'):
                tag['src'] = self.sanitize_url(tag['src'])

            # Очищаем CSS в атрибуте style
            if tag.has_attr('style'):
                tag['style'] = self.sanitize_css(tag['style'])

        # 3. Удаляем комментарии (могут содержать опасный код)
        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        return str(soup)

    def sanitize(self):
        return self.sanitize_html(self.html_content)

    def __call__(self, html_content):
        return self.sanitize_html(html_content)
