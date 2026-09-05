from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestUserProfileView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Nome Completo',
            username='Teste_1990',
            email='teste@mail.com.br',
        )

    def test_profile_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_authenticated_user_returns_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')