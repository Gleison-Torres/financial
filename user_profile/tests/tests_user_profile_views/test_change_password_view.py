from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

from user_profile.forms import ChangePasswordForm


class TestChangePasswordView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Teste_1980',
            email='teste@mail.com',
            password='Senha@123'
        )

        self.url = reverse('change_password')

        self.form_data = {
            'current_password': 'Senha@123',
            'password': 'NovaSenha@2026',
            'confirm_password': 'NovaSenha@2026'
        }

    def test_change_password_redirects_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,f"{reverse('login')}?next={self.url}")

    def test_change_password_get_returns_correct_template_and_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ChangePasswordForm)

    def test_change_password_valid_post_changes_password(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.form_data)

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('NovaSenha@2026'))

        self.assertRedirects(response, reverse('profile'))

    def test_change_password_keeps_user_authenticated(self):
        self.client.force_login(self.user)

        self.client.post(self.url, self.form_data)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    def test_change_password_invalid_post_does_not_change_password(self):
        self.client.force_login(self.user)

        self.form_data['current_password'] = 'SenhaErrada@123'

        response = self.client.post(self.url, self.form_data)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password('Senha@123'))
        self.assertIn('current_password', response.context['form'].errors)

    def test_change_password_success_message(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.form_data)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]),'Senha alterada com sucesso.')