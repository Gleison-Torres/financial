from django.test import TestCase
from accounts.forms import LoginForm
from django.contrib.auth.models import User


class TestLoginForms(TestCase):

    def setUp(self):

        User.objects.create_user(
            username='teste1989',
            email='teste@email.com',
            password='Senha@123'
        )

        self.form_data = {
            'username': 'teste1989',
            'password': 'Senha@123',
        }

    def test_inputs_required(self):

        self.form_data = {key: '' for key in self.form_data}
        form = LoginForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['username'][0], 'Este campo é obrigatório.')
        self.assertEqual(form.errors['password'][0], 'Este campo é obrigatório.')

    def test_login_is_invalid(self):

        self.form_data = {key: 'Teste@123' for key in self.form_data}
        form = LoginForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['username'][0], 'Usuário/e-mail ou senha incorretos.')
        self.assertEqual(form.errors['password'][0], 'Usuário/e-mail ou senha incorretos.')

    def test_login_with_email_is_valid(self):
        self.form_data['username'] = 'teste@email.com'
        form = LoginForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['user'].username, 'teste1989')

    def test_login_with_username_is_valid(self):
        form = LoginForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['user'].username, 'teste1989')
