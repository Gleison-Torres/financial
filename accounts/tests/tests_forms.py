from django.test import TestCase
from accounts.forms import RegisterForm
from django.contrib.auth.models import User


class TestRegisterForms(TestCase):

    def test_register_form_is_valid(self):

        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        })

        self.assertTrue(form.is_valid())

    def test_forms_passwords_must_match(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@321',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)

    def test_forms_password_must_have_minimum_8_characters(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Ab@12',
            'confirm_password': 'Ab@12',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_forms_password_must_have_uppercase(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'senha@123',
            'confirm_password': 'senha@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_forms_username_must_be_unique(self):
        User.objects.create_user(
            username='gleison1989',
            email='teste@email.com',
            password='Senha@123'
        )

        form = RegisterForm(data={
            'fullname': 'Outro Usuário',
            'username': 'gleison1989',
            'email': 'novo@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

