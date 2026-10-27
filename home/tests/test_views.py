from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class TestHomeView(TestCase):

    def setUp(self):
        self.url = reverse('home')

        self.user = User.objects.create_user(
            username='usuario_teste',
            email='teste@example.com',
            password='SenhaTeste123!',
            first_name='Carlos Eduardo'
        )

    def test_home_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}"
        )

    def test_home_returns_status_200_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'home.html')

    def test_home_displays_user_first_name(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.context['first_name'], 'Carlos')

    def test_home_uses_username_when_first_name_is_empty(self):
        self.user.first_name = ''
        self.user.save()

        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(
            response.context['first_name'],
            'usuario_teste'
        )