from accounts.forms import PasswordValidatorMixin
from django import forms
from django.core.exceptions import ValidationError


class ChangePasswordForm(PasswordValidatorMixin, forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current = self.cleaned_data.get('current_password')

        if not self.user.check_password(current):
            raise ValidationError('Senha atual incorreta.')

        return current

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise ValidationError({
                'password': 'As senhas não coincidem.',
                'confirm_password': 'As senhas não coincidem.'
            })

        if password and self.user.check_password(password):
            raise ValidationError({
                'password': 'A nova senha deve ser diferente da senha atual.',
                'confirm_password': 'A nova senha deve ser diferente da senha atual.'
            })

        return cleaned_data