from django.test import TestCase
from accounts.forms import RegisterForm
from django.contrib.auth.models import User


class TestRegisterForms(TestCase):

    def setUp(self):

        User.objects.create_user(
            username='gleison1989',
            email='teste@email.com',
            password='Senha@123'
        )

        self.form_data = {
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        }

    def test_register_form_is_valid(self):
        # Evita conflito com o usuario criado no setUp.
        self.form_data['username'] = 'gleison1990'

        form = RegisterForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_passwords_must_match(self):
        self.form_data['confirm_password'] = 'Senha@321'
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)
        self.assertEqual(form.errors['password'][0], 'As senhas não coincidem.')
        self.assertEqual(form.errors['confirm_password'][0], 'As senhas não coincidem.')

    def test_register_form_password_must_have_minimum_8_characters(self):
        self.form_data['password'] = 'Ab@12'
        self.form_data['confirm_password'] = 'Ab@12'

        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve possuir pelo menos 8 caracteres.')

    def test_register_form_password_must_have_uppercase(self):
        self.form_data['password'] = 'senha@123'
        self.form_data['confirm_password'] = 'senha@123'

        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos uma letra maiúscula.')

    def test_register_form_password_must_have_numbers(self):
        self.form_data['password'] = 'Senha@abc'
        self.form_data['confirm_password'] = 'Senha@abc'

        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos um número.')

    def test_register_form_password_must_have_special_character(self):
        self.form_data['password'] = 'Senha1234'
        self.form_data['confirm_password'] = 'Senha1234'

        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos um caractere especial.')

    def test_register_form_password_must_have_lowercase(self):
        self.form_data['password'] = 'SENHA@123'
        self.form_data['confirm_password'] = 'SENHA@123'

        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos uma letra minúscula.')

    def test_register_form_username_must_be_unique(self):
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0], 'Este nome de usuário já está em uso.')

    def test_register_form_email_must_be_unique(self):
        self.form_data['email'] = 'teste@email.com'
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Este e-mail já está cadastrado.')

    def test_register_form_fullname_is_required(self):
        self.form_data['fullname'] = ''
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('fullname', form.errors)
        self.assertEqual(form.errors['fullname'][0], 'Este campo é obrigatório.')
