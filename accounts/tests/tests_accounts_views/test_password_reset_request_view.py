from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail


class TestPasswordResetRequestView(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='teste1989',
            email='teste@mail.com',
            password='Senha@123',
            is_active=True
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse('password_reset_request'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset/password_reset_request.html')

    def test_authenticated_user_is_redirected_to_home(self):

        self.client.login(username='teste1989', password='Senha@123')

        response = self.client.get(reverse('password_reset_request'))

        self.assertRedirects(response, reverse('home'))

    def test_post_with_existing_email_sends_email(self):
        response = self.client.post(reverse('password_reset_request'), {'email': 'teste@mail.com'})

        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, reverse('login'))

    def test_post_with_non_existing_email_does_not_send_email(self):
        response = self.client.post(
            reverse('password_reset_request'),
            {'email': 'naoexiste@email.com'}
        )

        self.assertEqual(len(mail.outbox), 0)
        self.assertRedirects(response, reverse('login'))

    def test_post_always_shows_generic_message(self):
        response = self.client.post(
            reverse('password_reset_request'),
            {'email': 'naoexiste@email.com'},
            follow=True
        )

        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            'Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.',
            str(messages[0])
        )