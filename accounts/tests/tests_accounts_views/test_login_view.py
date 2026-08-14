from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestLoginView(TestCase):

    def setUp(self):

        User.objects.create_user(
            username='teste1989',
            email='teste@email.com',
            password='Senha@123'
        )

    def test_get_return_200_for_user_anonymous(self):
        response_login = self.client.get(reverse('login'))
        response_register = self.client.get(reverse('register'))

        self.assertEqual(response_login.status_code, 200)
        self.assertEqual(response_register.status_code, 200)

    def test_user_authenticated_and_redirected_to_home(self):

        self.client.login(username='teste1989', password='Senha@123')

        response_login = self.client.get(reverse('login'))
        response_register = self.client.get(reverse('register'))

        self.assertRedirects(response_login, reverse('home'))
        self.assertRedirects(response_register, reverse('home'))

