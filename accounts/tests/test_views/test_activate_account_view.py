from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.token import account_activation_token


class TestActivateAccountView(TestCase):

    def setUp(self):
        """
        Cria um usuario inativo para ser utilizado
        em todos os testes da view.
        """
        self.user = get_user_model().objects.create_user(
            username='gleison1989',
            email='gleison@email.com',
            password='Senha@123',
            is_active=False
        )

    def test_activate_account_with_valid_token(self):
        """
        Deve ativar o usuario quando uid e token forem válidos.
        """

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)

        response = self.client.get(
            reverse(
                'activate',
                kwargs={
                    'uidb64': uid,
                    'token': token,
                }
            )
        )

        self.user.refresh_from_db()

        self.assertTrue(self.user.is_active)

        self.assertTemplateUsed(
            response,
            'activation/successful_account_activation.html'
        )

    def test_activate_account_with_invalid_token(self):
        """
        Não deve ativar o usuario quando o token for inválido.
        """

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.get(
            reverse(
                'activate',
                kwargs={
                    'uidb64': uid,
                    'token': 'token-invalido',
                }
            )
        )

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_active)

        self.assertTemplateUsed(response, 'activation/unsuccessful_account_activation.html')

    def test_activate_account_with_invalid_uid(self):
        """
        Deve exibir a página de falha quando o uid for inválido.
        """

        response = self.client.get(
            reverse(
                'activate',
                kwargs={
                    'uidb64': 'uid-invalido',
                    'token': 'qualquer-token'
                }
            )
        )

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_active)

        self.assertTemplateUsed(response, 'activation/unsuccessful_account_activation.html')

    def test_activate_account_when_user_is_already_active(self):
        """
        Mesmo que o usuario já esteja ativo,
        a página de sucesso deve ser exibida.
        """

        self.user.is_active = True
        self.user.save()

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)

        response = self.client.get(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

        self.user.refresh_from_db()

        self.assertTrue(self.user.is_active)

        self.assertTemplateUsed(response, 'activation/successful_account_activation.html')