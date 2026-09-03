from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.forms import ChangePasswordForm


class TestChangePasswordForm(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='Teste_1980',
            email='teste@mail.com',
            password='Senha@123'
        )

        self.form_data = {
            'current_password': 'Senha@123',
            'password': 'Teste@2026',
            'confirm_password': 'Teste@2026'
        }

    def test_change_password_form_valid(self):
        form = ChangePasswordForm(self.user, self.form_data)
        self.assertTrue(form.is_valid())

    def test_current_password_incorrect(self):
        self.form_data['current_password'] = 'SenhaIncorreta@123'
        form = ChangePasswordForm(self.user, self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('current_password', form.errors)
        self.assertEqual(form.errors['current_password'][0], 'Senha atual incorreta.')

    def test_new_password_cannot_match_the_current_password(self):
        self.form_data['password'] = 'Senha@123'
        self.form_data['confirm_password'] = 'Senha@123'

        form = ChangePasswordForm(self.user, self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A nova senha deve ser diferente da senha atual.')
        self.assertEqual(form.errors['confirm_password'][0], 'A nova senha deve ser diferente da senha atual.')

    def test_password_and_confirm_password_do_not_match(self):
        self.form_data['confirm_password'] = 'SenhaDiferente@123'

        form = ChangePasswordForm(self.user, self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)
        self.assertEqual(form.errors['password'][0], 'As senhas não coincidem.')
        self.assertEqual(form.errors['confirm_password'][0], 'As senhas não coincidem.')

