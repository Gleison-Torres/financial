import string
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RegisterForm(forms.Form):

    fullname = forms.CharField(
        required=True,
        max_length=100
    )

    username = forms.CharField(
        required=True,
        min_length=3,
        max_length=30
    )

    email = forms.EmailField(
        required=True,
        max_length=250
    )

    password = forms.CharField(
        required=True,
        strip=False,
    )

    confirm_password = forms.CharField(
        required=True,
        strip=False,
    )

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError(
                    {'password': 'As senhas não coincidem.',
                     'confirm_password': 'As senhas não coincidem.'}
                )
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError('A senha deve possuir pelo menos 8 caracteres.')

        if not any(char.isupper() for char in password):
            raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')

        if not any(char.islower() for char in password):
            raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')

        if not any(char.isdigit() for char in password):
            raise ValidationError('A senha deve conter pelo menos um número.')

        if not any(char in string.punctuation for char in password):
            raise ValidationError('A senha deve conter pelo menos um caractere especial.')

        return password

    def clean_email(self):
        email_data = self.cleaned_data.get('email')
        if User.objects.filter(email=email_data).exists():
            raise ValidationError('Este e-mail já está cadastrado.')
        return email_data

    def clean_username(self):
        username_data = self.cleaned_data.get('username')
        if User.objects.filter(username=username_data).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username_data
