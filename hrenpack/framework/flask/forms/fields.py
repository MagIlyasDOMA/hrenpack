"""
WTForms custom fields for Flask applications.

Provides BooleanSelectField for boolean values with 'true'/'false' string representation.

Пользовательские поля WTForms для Flask приложений.

Предоставляет BooleanSelectField для булевых значений со строковым представлением 'true'/'false'.
"""

from wtforms import SelectField
from wtforms.validators import ValidationError


class BooleanSelectField(SelectField):
    """
    SelectField that accepts 'true'/'false' from HTML but returns bool in data.

    SelectField, который принимает 'true'/'false' из HTML, но возвращает bool в data.

    Args:
        label (str): Field label / Метка поля
        validators: List of validators / Список валидаторов
        false_label (str): Label for false option, default "False" / Метка для варианта false
        true_label (str): Label for true option, default "True" / Метка для варианта true
        **kwargs: Additional arguments for SelectField / Дополнительные аргументы для SelectField
    """

    def __init__(self, label='', validators=None,
                 false_label: str = "False",
                 true_label: str = "True",
                 **kwargs):
        # Set default choices
        choices = [('false', false_label), ('true', true_label)]

        # Allow overriding choices if needed
        if 'choices' not in kwargs:
            kwargs['choices'] = choices

        # Don't use coerce=bool as it doesn't work with 'true'/'false'
        kwargs.pop('coerce', None)

        super().__init__(label, validators, **kwargs)

        # Save text values for validation
        self.true_value = 'true'
        self.false_value = 'false'

    def process_formdata(self, valuelist):
        """
        Process form data, converting 'true'/'false' to bool.

        Обрабатывает данные из формы, преобразуя 'true'/'false' в bool.

        Args:
            valuelist: List of submitted values / Список отправленных значений

        Raises:
            ValidationError: If value is not 'true' or 'false' / Если значение не 'true' или 'false'
        """
        if valuelist:
            value = str(valuelist[0])
            # Convert string to bool
            if value == self.true_value:
                self.data = True
            elif value == self.false_value:
                self.data = False
            else:
                self.data = None
                raise ValidationError(f'Invalid value: {value}')

            # IMPORTANT: save raw_data for choices validation
            self.raw_data = [value]
        else:
            self.data = None
            self.raw_data = []

    def pre_validate(self, form):
        """
        Override validation to skip standard choices check.

        Переопределяем валидацию, чтобы пропустить стандартную проверку choices.

        Instead check that value is True or False.

        Args:
            form: Parent form / Родительская форма

        Raises:
            ValidationError: If value is not valid / Если значение невалидно
        """
        # Skip standard choices validation
        if self.data is not None and self.data in (True, False):
            return
        elif self.data is None and not self.raw_data:
            # Empty value
            pass
        else:
            raise ValidationError(self.gettext('Not a valid choice'))

    def _value(self):
        """
        Return value for HTML display.

        Возвращает значение для отображения в HTML.

        Returns:
            str: 'true', 'false', or empty string / 'true', 'false' или пустая строка
        """
        if self.data is True:
            return self.true_value
        elif self.data is False:
            return self.false_value
        return ''
