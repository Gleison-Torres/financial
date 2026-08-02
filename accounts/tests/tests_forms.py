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

    def test_register_form_passwords_must_match(self):
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
        self.assertEqual(form.errors['password'][0], 'As senhas não coincidem.')
        self.assertEqual(form.errors['confirm_password'][0], 'As senhas não coincidem.')

    def test_register_form_password_must_have_minimum_8_characters(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Ab@12',
            'confirm_password': 'Ab@12',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve possuir pelo menos 8 caracteres.')

    def test_register_form_password_must_have_uppercase(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'senha@123',
            'confirm_password': 'senha@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos uma letra maiúscula.')

    def test_register_form_password_must_have_numbers(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha@abc',
            'confirm_password': 'Senha@abc',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos um número.')

    def test_register_form_password_must_have_special_character(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha1234',
            'confirm_password': 'Senha1234',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos um caractere especial.')

    def test_register_form_password_must_have_lowercase(self):
        form = RegisterForm(data={
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'SENHA@123',
            'confirm_password': 'SENHA@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos uma letra minúscula.')

    def test_register_form_username_must_be_unique(self):
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
        self.assertEqual(form.errors['username'][0], 'Este nome de usuário já está em uso.')

    def test_register_form_email_must_be_unique(self):
        User.objects.create_user(
            username='gleison1980',
            email='teste@email.com',
            password='Senha@123'
        )

        form = RegisterForm(data={
            'fullname': 'Outro Usuário',
            'username': 'gleison1989',
            'email': 'teste@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Este e-mail já está cadastrado.')

    def test_register_form_fullname_is_required(self):
        form = RegisterForm(data={
            'fullname': '',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('fullname', form.errors)
        self.assertEqual(form.errors['fullname'][0], 'Este campo é obrigatório.')

