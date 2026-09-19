from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core import mail

from user_profile.models import EmailChangeRequest
from user_profile.services import send_email_change_confirmation


class TestEmailChangeService(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison',
            email='gleison@email.com'
        )

        self.email_change_request = EmailChangeRequest.objects.create(
            user=self.user,
            new_email='novo@email.com'
        )

        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_send_email_change_confirmation_sends_email(self):
        send_email_change_confirmation(self.request, self.email_change_request)

        self.assertEqual(len(mail.outbox), 1)

    def test_email_is_sent_to_new_email_address(self):
        send_email_change_confirmation(self.request, self.email_change_request)

        email = mail.outbox[0]

        self.assertEqual(email.to, ['novo@email.com'])

    def test_email_has_correct_subject(self):
        send_email_change_confirmation(self.request, self.email_change_request)

        email = mail.outbox[0]

        self.assertEqual(email.subject, 'Confirme a alteração do seu e-mail')

    def test_email_body_contains_confirmation_link(self):
        send_email_change_confirmation(self.request, self.email_change_request)

        email = mail.outbox[0]

        self.assertIn('/profile/confirm-email/', email.body)