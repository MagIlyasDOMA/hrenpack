"""
Flask-WTF form mixins for enhanced rendering.

Provides DjangoStyleFormMixin for rendering forms as paragraphs.

Примеси форм Flask-WTF для улучшенного рендеринга.

Предоставляет DjangoStyleFormMixin для рендеринга форм в виде параграфов.
"""

from markupsafe import Markup


class DjangoStyleFormMixin:
    """
    Mixin that adds Django-style form rendering as <p> tags.

    Примесь, добавляющая рендеринг форм в стиле Django в виде тегов <p>.

    Example:
        class MyForm(DjangoStyleFormMixin, FlaskForm):
            name = StringField('Name')
            email = StringField('Email')

        In template:
            {{ form.as_p() }}
    """

    def as_p(self, include_hidden_fields: bool = True):
        """
        Render form as a sequence of <p> tags.

        Рендерит форму как последовательность тегов <p>.

        Args:
            include_hidden_fields (bool): Include hidden fields (CSRF, etc.), default True / Включить скрытые поля

        Returns:
            Markup: HTML markup with form fields wrapped in <p> tags / HTML разметка с полями формы в тегах <p>

        Example output:
            <p>
                <label for="name">Name</label>
                <input id="name" name="name" type="text">
            </p>
            <p>
                <label for="email">Email</label>
                <input id="email" name="email" type="text">
                <span class="helptext">Enter a valid email</span>
            </p>
        """
        html = []
        for field in self:
            # Skip hidden fields if requested
            if not include_hidden_fields and field.type in ['HiddenField', 'CSRFTokenField']:
                continue

            # Hidden fields are rendered without <p> wrapper
            if field.type in ['HiddenField', 'CSRFTokenField']:
                html.append(str(field))
            else:
                # Main field HTML
                field_html = [str(field.label), f'\t{field}']

                # For boolean fields, swap label and field order
                if field.type in ['BooleanField']:
                    field_html.reverse()

                # Add help text if present
                if hasattr(field, 'help_text') and field.help_text:
                    field_html.append(f'<span class="helptext">{field.help_text}</span>')

                # Add error messages if any
                if field.errors:
                    error_html = ['<ul class="errorlist">']
                    for error in field.errors:
                        error_html.append(f'<li>{error}</li>')
                    error_html.append('</ul>')
                    field_html.append(''.join(error_html))

                # Wrap in paragraph tags
                html.append(f'<p>\n\t{"\n".join(field_html)}\n</p>')

        return Markup('\n'.join(html))
