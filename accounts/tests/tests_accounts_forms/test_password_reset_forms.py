from django.test import TestCase
from accounts.forms import PasswordResetForm


class TestPasswordReset(TestCase):

    def setUp(self):

        self.form_data = {
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        }

    def test_password_reset_form_is_valid(self):
        form = PasswordResetForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_passwords_must_match(self):
        self.form_data['confirm_password'] = 'Senha@321'
        form = PasswordResetForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)
        self.assertEqual(form.errors['password'][0], 'As senhas não coincidem.')
        self.assertEqual(form.errors['confirm_password'][0], 'As senhas não coincidem.')

    def test_register_form_password_must_have_minimum_8_characters(self):
        self.form_data['password'] = 'Ab@12'
        self.form_data['confirm_password'] = 'Ab@12'

        form = PasswordResetForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve possuir pelo menos 8 caracteres.')

    def test_register_form_password_must_have_uppercase(self):
        self.form_data['password'] = 'senha@123'
        self.form_data['confirm_password'] = 'senha@123'

        form = PasswordResetForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos uma letra maiúscula.')

    def test_register_form_password_must_have_numbers(self):
        self.form_data['password'] = 'Senha@abc'
        self.form_data['confirm_password'] = 'Senha@abc'

        form = PasswordResetForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos um número.')

    def test_register_form_password_must_have_special_character(self):
        self.form_data['password'] = 'Senha1234'
        self.form_data['confirm_password'] = 'Senha1234'

        form = PasswordResetForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos um caractere especial.')

    def test_register_form_password_must_have_lowercase(self):
        self.form_data['password'] = 'SENHA@123'
        self.form_data['confirm_password'] = 'SENHA@123'

        form = PasswordResetForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'][0], 'A senha deve conter pelo menos uma letra minúscula.')


