from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core import mail
from accounts.services import send_activation_email


class TestEmailServices(TestCase):
    """
        Testes responsáveis por validar o comportamento do serviço
        de envio de email de ativação de conta.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        self.user = User.objects.create_user(
            username='gleison1989',
            email='gleison@email.com',
            password='Senha@123',
            is_active=False
        )

    def test_send_activation_email(self):

        send_activation_email(self.request, self.user)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]

        self.assertEqual(email.subject, 'Ative sua conta')
        self.assertEqual(email.to, ['gleison@email.com'])
        self.assertEqual(email.content_subtype, 'html')
        self.assertIn(self.user.username, email.body)
        self.assertIn('testserver', email.body)
