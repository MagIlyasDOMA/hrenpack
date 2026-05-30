"""
Django form extensions.

Provides custom password change form with optional password validation.

Расширения форм Django.

Предоставляет пользовательскую форму смены пароля с опциональной валидацией.
"""

from django import forms
from django.contrib.auth import forms as auth_forms, password_validation


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    """
    Password change form with optional password fields.

    Форма смены пароля с опциональными полями пароля.

    Allows changing password only if both new password fields are filled.
    If only one field is filled, form is invalid.

    Позволяет изменить пароль только если оба поля нового пароля заполнены.
    Если заполнено только одно поле, форма невалидна.
    """
    old_password = forms.CharField(
        label="Old password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    password1 = forms.CharField(
        label="New password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Confirm password",
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def __bool__(self):
        """
        Check if form is empty (no password change requested).

        Проверяет, пуста ли форма (смена пароля не запрошена).

        Returns:
            bool: True if both password fields are empty / True если оба поля пароля пусты
        """
        cd = self.cleaned_data
        return not cd['new_password1'] and cd['new_password2']

    def is_valid(self):
        """
        Validate form.

        Валидирует форму.

        Returns:
            bool: True if form is valid / True если форма валидна
        """
        cd = self.cleaned_data
        if cd['password1'] and cd['password2']:
            pass
        elif cd['password1'] or cd['password2']:
            return False
        return super().is_valid()
