from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TestPasswordResetView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison1989',
            email='gleison@mail.com',
            password='Senha@123',
            is_active=True
        )

        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_get_valid_token_returns_200(self):
        response = self.client.get(reverse('password_reset', args=[self.uid, self.token]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'password_reset/password_reset.html')

    def test_get_context_contains_validlink_true(self):
        response = self.client.get(reverse('password_reset', args=[self.uid, self.token]))

        self.assertTrue(response.context['validlink'])

    def test_invalid_uid_returns_unsuccessful_template(self):
        response = self.client.get(reverse('password_reset', args=['uid_invalido', self.token]))

        self.assertTemplateUsed(response,'password_reset/unsuccessful_password_reset.html')

    def test_invalid_token_returns_unsuccessful_template(self):
        response = self.client.get(reverse('password_reset', args=[self.uid, 'token-invalido']))

        self.assertTemplateUsed(response, 'password_reset/unsuccessful_password_reset.html')

    def test_valid_post_changes_password(self):
        self.client.post(reverse('password_reset', args=[self.uid, self.token]), {
                'password': 'NovaSenha@123',
                'confirm_password': 'NovaSenha@123'
            }
        )

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('NovaSenha@123'))

    def test_valid_post_redirects_login(self):
        response = self.client.post(
            reverse(
                'password_reset',
                args=[self.uid, self.token]
            ),
            {
                'password': 'NovaSenha@123',
                'confirm_password': 'NovaSenha@123'
            }
        )

        self.assertRedirects(response, reverse('login'))

    def test_valid_post_shows_success_message(self):
        response = self.client.post(reverse('password_reset', args=[self.uid, self.token]), {
                'password': 'NovaSenha@123',
                'confirm_password': 'NovaSenha@123'
            }, follow=True
        )

        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertIn('Sua senha foi redefinida com sucesso.', str(messages[0]))

    def test_invalid_post_does_not_change_password(self):
        self.client.post(reverse('password_reset', args=[self.uid, self.token]), {
                'password': 'metal@123',
                'confirm_password': 'metal@123'
            }
        )

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('Senha@123'))

    def test_post_with_different_passwords_returns_errors(self):
        response = self.client.post(reverse('password_reset', args=[self.uid, self.token]), {
                'password': 'Metal@123',
                'confirm_password': 'Metal@321'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())