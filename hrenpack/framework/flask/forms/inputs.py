# Hrenpack v2.0.0
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from typing import Literal, Optional, Union
from hrenpack.listwork import dict_slice
from hrenpack.encapsulation import AbstractClass, abstractmethod
from ..decorators import safe
from .mixins import InputAttrsMixin
from .typings import InputTypeExtended, SimpleList, InputType


class InputTypeError(Exception):
    def __init__(self, name, input_type, *attrs, lang: str = 'en'):
        self.name = name
        self.input_type = input_type
        self.lang = lang
        self.attrs = list(attrs)

    def _format_attrs(self):
        if not self.attrs:
            return ""

        if len(self.attrs) == 1:
            return str(self.attrs[0])

        sep = ' и ' if self.lang == 'ru' else ' and '
        return ', '.join(map(str, self.attrs[:-1])) + sep + str(self.attrs[-1])

    def __str__(self):
        formatted_attrs = self._format_attrs()

        if self.lang == 'ru':
            if formatted_attrs:
                return f"Поле {self.name} имеет тип {self.input_type} и не поддерживает атрибуты {formatted_attrs}"
            else:
                return f"Поле {self.name} имеет тип {self.input_type}"
        else:
            if formatted_attrs:
                return f'Input {self.name} is of type {self.input_type} and does not support attributes {formatted_attrs}'
            else:
                return f'Input {self.name} is of type {self.input_type}'



class BaseInput(AbstractClass):
    @abstractmethod
    def __init__(self, name: str, label: Optional[str] = None, disabled: bool = False,
                 required: bool = False, autofocus: bool = False, class_: Optional[str] = None,
                 lang: str = 'en', **kwargs):
        self.name = name
        self.label = label
        self.disabled = disabled
        self.required = required
        self.autofocus = autofocus
        self.lang = lang
        self.class_ = kwargs.get('class_', kwargs.get('class', None))

    @abstractmethod
    def render(self):
        pass


class Input(BaseInput):
    """Объединенный класс для создания HTML input и textarea элементов"""

    NOTTEXT_INPUT_TYPES = {'checkbox', 'radio', 'file', 'hidden', 'button', 'submit', 'reset', 'image'}
    TEXTAREA_ONLY_ATTRS = {'rows', 'cols', 'wrap'}

    def __init__(self, name: str, type: InputTypeExtended = 'text', label: Optional[str] = None,
                 value: Optional[str] = None, disabled: bool = False, required: bool = False,
                 readonly: bool = False, autofocus: bool = False, lang: str = 'en', **kwargs):
        super().__init__(name, label, disabled, required, autofocus, lang)

        # Основные атрибуты BaseInput
        self.value = value
        self.readonly = readonly
        self.type = type

        # Определяем HTML тег на основе типа
        self.html_tag = 'textarea' if type == 'textarea' else 'input'

        # Атрибуты InputAttrsMixin
        self.checked = False
        self.placeholder = None
        self.minlength = None
        self.maxlength = None
        self.step = None
        self.multiple = False
        self.accept = None

        # Атрибуты textarea
        self.rows = None
        self.cols = None
        self.wrap = None

        # Внутренние атрибуты
        self._forbidden_attrs = list()

        # Инициализация атрибутов из kwargs
        self._init_attrs(kwargs)

        # Проверка правил валидации атрибутов (только для input)
        if self.html_tag == 'input':
            self._validate_attributes()

    def _init_attrs(self, kwargs):
        """Инициализация дополнительных атрибутов"""
        self.use_br = kwargs.get('use_br', False)
        self.before_label = kwargs.get('before_label', False)
        self.without_label = kwargs.get('without_label', False)

        # Установка атрибутов из InputAttrsMixin
        self.checked = kwargs.get('checked', False)
        self.placeholder = kwargs.get('placeholder', None)
        self.minlength = kwargs.get('minlength', None)
        self.maxlength = kwargs.get('maxlength', None)
        self.step = kwargs.get('step', None)
        self.multiple = kwargs.get('multiple', False)
        self.accept = kwargs.get('accept', None)

        # Установка атрибутов textarea
        self.rows = kwargs.get('rows', None)
        self.cols = kwargs.get('cols', None)
        self.wrap = kwargs.get('wrap', None)

    def _validate_attributes(self):
        """Проверка валидности атрибутов для текущего типа input"""
        self._add_rule('checkbox', 'radio', required=self.required, __setattr__=False)
        self._add_rule('checkbox', 'radio', checked=self.checked, __type__='whitelist')
        self._add_rule('hidden', autofocus=self.autofocus, __setattr__=False)
        self._add_rule(*self.NOTTEXT_INPUT_TYPES,
                       **dict_slice(self.__dict__, 'placeholder', 'minlength', 'maxlength', 'pattern'))
        self._add_rule('number', 'range', 'date', dict_slice(self.__dict__, 'min', 'max'), type__='whitelist')
        self._add_rule('number', 'range', step=self.step, type__='whitelist')
        self._add_rule('file', dict_slice(self.__dict__, 'multiple', 'accept'), type__='whitelist')

        # Обработка accept атрибута
        self.accept = self.__init_accept(self.accept)

        if self._forbidden_attrs:
            raise InputTypeError(self.name, self.type, *self._forbidden_attrs, lang=self.lang)

    @staticmethod
    def __format_dicts(lst: tuple):
        """Форматирование словарей в кортеже"""
        lst = list(lst)
        dct = dict()
        for el in lst:
            if type(el) is dict:
                dct.update(el)
                lst.remove(el)
        return lst, dct

    def _add_rule(self, *types: Union[InputType, dict],
                  setattr__: bool = True,
                  type__: Literal['blacklist', 'whitelist'] = 'blacklist', **values):
        """Добавление правила валидации атрибутов"""
        types, dct = self.__format_dicts(types)
        values.update(dct)
        rule = self.type in types if type__ == 'blacklist' else self.type not in types

        if rule:
            for attr_name, attr_value in values.items():
                if attr_value is not None and attr_value is not False:
                    self._forbidden_attrs.append(attr_name)
        elif setattr__:
            for attr_name, attr_value in values.items():
                setattr(self, attr_name, attr_value)

    @staticmethod
    def __init_accept(accept: Union[str, SimpleList]):
        """Инициализация accept атрибута"""
        if accept is not None:
            if isinstance(accept, SimpleList):
                for i in range(len(accept)):
                    el = accept[i]
                    if el[0] != '.':
                        accept[i] = '.' + el
                return ', '.join(accept)
            elif isinstance(accept, str):
                return accept
            raise TypeError
        return None

    @property
    def input_attrs(self):
        """Список всех input атрибутов"""
        base_attrs = ['required', 'readonly', 'disabled', 'class_', 'placeholder',
                      'minlength', 'maxlength', 'checked', 'multiple', 'accept']

        if self.html_tag == 'input':
            base_attrs.extend(['pattern', 'min', 'max', 'step'])
        elif self.html_tag == 'textarea':
            base_attrs.extend(['rows', 'cols', 'wrap'])

        return base_attrs

    @property
    def id(self):
        """Генерация ID элемента"""
        return 'id_' + self.name

    def _create_input_element(self) -> str:
        """Создание HTML строки input элемента"""
        html = f'<input type="{self.type}" name="{self.name}" id="{self.id}"'

        if self.value is not None:
            html += f' value="{self.value}"'
        if self.placeholder is not None:
            html += f' placeholder="{self.placeholder}"'
        if self.class_ is not None:
            html += f' class="{self.class_}"'

        # Булевые атрибуты
        if self.disabled:
            html += ' disabled'
        if self.required:
            html += ' required'
        if self.readonly:
            html += ' readonly'
        if self.autofocus:
            html += ' autofocus'
        if self.checked:
            html += ' checked'
        if self.multiple:
            html += ' multiple'

        # Числовые и строковые атрибуты
        attrs_to_check = {
            'minlength': self.minlength,
            'maxlength': self.maxlength,
            'step': self.step,
            'min': getattr(self, 'min', None),
            'max': getattr(self, 'max', None),
            'pattern': getattr(self, 'pattern', None),
            'accept': self.accept
        }

        for attr_name, attr_value in attrs_to_check.items():
            if attr_value is not None:
                html += f' {attr_name}="{attr_value}"'

        html += '>'
        return html

    def _create_textarea_element(self) -> str:
        """Создание HTML строки textarea элемента"""
        html = f'<textarea name="{self.name}" id="{self.id}"'

        # Атрибуты textarea
        if self.placeholder is not None:
            html += f' placeholder="{self.placeholder}"'
        if self.minlength is not None:
            html += f' minlength="{self.minlength}"'
        if self.maxlength is not None:
            html += f' maxlength="{self.maxlength}"'
        if self.rows is not None:
            html += f' rows="{self.rows}"'
        if self.cols is not None:
            html += f' cols="{self.cols}"'
        if self.wrap is not None:
            html += f' wrap="{self.wrap}"'
        if self.class_ is not None:
            html += f' class="{self.class_}"'

        # Булевые атрибуты
        if self.disabled:
            html += ' disabled'
        if self.required:
            html += ' required'
        if self.readonly:
            html += ' readonly'
        if self.autofocus:
            html += ' autofocus'

        html += '>'

        # Добавляем значение textarea
        if self.value is not None:
            html += self.value

        html += '</textarea>'
        return html

    def _create_input(self) -> str:
        """Создание HTML элемента в зависимости от типа"""
        if self.html_tag == 'textarea':
            return self._create_textarea_element()
        else:
            return self._create_input_element()

    @safe
    def render(self) -> str:
        """Рендеринг полного HTML элемента с label"""
        label_text = self.label if self.label is not None else self.name.capitalize()
        label = f'<label for="{self.id}">{label_text}</label>\n{"<br>" if self.use_br else ""}' if not self.without_label else ''
        input_html = self._create_input()
        return (input_html + label) if self.before_label else (label + input_html)

    def __str__(self):
        return self.render()


class ComboBoxInput(BaseInput):
    def __init__(self, name: str, label: str = None, autofocus: bool = False, disabled: bool = False,
                 required: bool = False, values: Optional[dict] = None, **kwargs):
        super().__init__(name, label, disabled, required, autofocus, **kwargs)
        empty = kwargs.get('empty', None)
        if empty is not None:
            values[''] = empty
        self.values = values

    @safe
    def render(self) -> str:
        html = '<select>\n'
        for value, text in self.values.items():
            html += f'<option value="{value}">{text}</option>\n'
        html += '</select>'
        return html


class InputGroup:
    def __init__(self, *inputs: BaseInput, rewrite_attrs: bool = False, **kwargs):
        self.inputs = list(inputs)
        self.rewrite_attrs = rewrite_attrs
        self.kwargs = kwargs
        self.do_rewrite_attrs()

    def do_rewrite_attrs(self):
        if self.rewrite_attrs:
            for input in self.inputs:
                for attr_name, attr_value in self.kwargs.items():
                    setattr(input, attr_name, attr_value)

    def add(self, input: Input):
        if self.rewrite_attrs:
            for attr_name, attr_value in self.kwargs.items():
                setattr(input, attr_name, attr_value)
        self.inputs.append(input)

    def __iter__(self):
        return iter(self.inputs)

    def __len__(self):
        return len(self.inputs)

    @safe
    def as_p(self) -> str:
        html = ''
        for input in self.inputs:
            html += f'<p>\n{input.render()}\n</p>\n'
        return html
