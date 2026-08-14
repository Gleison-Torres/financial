from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestLogoutView(TestCase):

    def setUp(self):

        User.objects.create_user(
            username='teste1989',
            email='teste@mail.com',
            password='Senha@123'
        )

    def test_logout_with_post(self):
        self.client.login(
            username='teste1989',
            password='Senha@123'
        )

        response_home = self.client.get(reverse('home'))
        self.assertEqual(response_home.wsgi_request.user.is_authenticated, True)

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_logout_with_get_returns_404(self):

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 404)
