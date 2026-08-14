from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import LoginForm


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

    def test_get_returns_the_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')

    def test_get_context_contains_an_empty_form(self):
        response = self.client.get(reverse('login'))
        form = response.context['form']
        self.assertIsInstance(form, LoginForm)
        self.assertFalse(form.is_bound)  # form vazio, sem dados

    def test_valid_post_request_authenticates_user(self):

        self.client.post(reverse('login'), {
            'username': 'teste1989',
            'password': 'Senha@123',
        })

        # usuário foi autenticado de fato (checa a sessão)
        self.assertIn('_auth_user_id', self.client.session)

    def test_valid_post_redirect_to_home(self):

        response = self.client.post(reverse('login'), {
            'username': 'teste1989',
            'password': 'Senha@123',
        })

        self.assertRedirects(response, reverse('home'))

    def test_valid_post_show_message_success(self):

        response = self.client.post(reverse('login'), {
            'username': 'teste1989',
            'password': 'Senha@123',
        }, follow=True)  # follow=True pra seguir o redirect e capturar a mensagem

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Bem vindo', str(messages[0]))

    def test_invalid_post_authentication_failed(self):
        self.client.post(reverse('login'), {
            'username': 'usuario_inexistente',
            'password': 'senhaerrada',
        })

        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_post_returns_200_and_renders_form_with_errors(self):
        response = self.client.post(reverse('login'), {
            'username': 'usuario_inexistente',
            'password': 'senhaerrada',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertFalse(response.context['form'].is_valid())
