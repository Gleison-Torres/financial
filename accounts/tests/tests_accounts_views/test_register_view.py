from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.forms import RegisterForm


class TestRegisterView(TestCase):

    def setUp(self):
        self.form_data = {
            'fullname': 'Gleison Torres Loiola',
            'username': 'gleison1989',
            'email': 'gleison@email.com',
            'password': 'Senha@123',
            'confirm_password': 'Senha@123',
        }

    def test_register_get(self):
        """
        Verifica se a página de cadastro é exibida
        corretamente através de uma requisição GET.
        """

        response = self.client.get(reverse('register'))

        # Verifica se a página respondeu corretamente.
        self.assertEqual(response.status_code, 200)

        # Verifica se o template correto foi utilizado.
        self.assertTemplateUsed(response, 'register.html')

        # Verifica se a view enviou um RegisterForm para o template.
        self.assertIsInstance(
            response.context['form'],
            RegisterForm
        )

    @patch('accounts.views.send_activation_email')
    def test_register_post_creates_user(self, mock_send_email):
        """
        Verifica se um usuário é criado quando o formulário
        é enviado com dados válidos.
        """

        response = self.client.post(
            reverse('register'),
            data=self.form_data
        )

        # Verifica se o usuário foi criado no banco.
        self.assertTrue(
            User.objects.filter(
                username='gleison1989'
            ).exists()
        )

        # Recupera o usuário criado.
        user = User.objects.get(username='gleison1989')

        # Verifica os dados salvos.
        self.assertEqual(
            user.first_name,
            'Gleison Torres Loiola'
        )

        self.assertEqual(
            user.email,
            'gleison@email.com'
        )

        # O usuário deve começar desativado.
        self.assertFalse(user.is_active)

        # A senha não deve ser armazenada em texto puro.
        self.assertNotEqual(
            user.password,
            'Senha@123'
        )

        # Verifica se a senha realmente pode ser validada pelo Django.
        self.assertTrue(
            user.check_password('Senha@123')
        )

        # Verifica se o serviço de envio de e-mail foi chamado
        # exatamente uma vez.
        mock_send_email.assert_called_once_with(
            response.wsgi_request,
            user=user
        )

        # Verifica se a resposta utilizou o template correto.
        self.assertTemplateUsed(response, 'register.html')

    @patch('accounts.views.send_activation_email')
    def test_register_post_shows_message(self, mock_send_email):
        """
        Verifica se a mensagem informando que o e-mail
        de ativação foi enviado é adicionada.
        """

        response = self.client.post(
            reverse('register'),
            data=self.form_data
        )

        # Obtém as mensagens geradas durante a requisição.
        messages = list(
            get_messages(response.wsgi_request)
        )

        # Verifica o conteúdo da mensagem.
        self.assertEqual(
            str(messages[0]),
            'Verifique sua caixa de entrada para ativar sua conta.'
        )

    @patch('accounts.views.send_activation_email')
    def test_register_post_invalid_data_does_not_create_user(
        self,
        mock_send_email
    ):
        """
        Verifica se dados inválidos não criam um usuário
        e não disparam o envio do e-mail.
        """

        invalid_data = self.form_data.copy()

        # Deixa o fullname vazio para tornar o formulário inválido.
        invalid_data['fullname'] = ''

        response = self.client.post(
            reverse('register'),
            data=invalid_data
        )

        # Nenhum usuário deve ter sido criado.
        self.assertEqual(
            User.objects.count(),
            0
        )

        # O serviço de e-mail não deve ser chamado.
        mock_send_email.assert_not_called()

        # O formulário deve continuar presente na resposta.
        self.assertIsInstance(
            response.context['form'],
            RegisterForm
        )

        # O formulário deve estar inválido.
        self.assertFalse(
            response.context['form'].is_valid()
        )

        # O template correto deve continuar sendo utilizado.
        self.assertTemplateUsed(
            response,
            'register.html'
        )
