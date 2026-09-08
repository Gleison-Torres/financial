from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from user_profile.models import EmailChangeRequest
from user_profile.tokens import email_change_token


class TestConfirmEmailChangeView(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='gleison',
            email='antigo@email.com'
        )

        self.email_change_request = EmailChangeRequest.objects.create(
            user=self.user,
            new_email='novo@email.com'
        )

        self.uid = urlsafe_base64_encode(
            force_bytes(self.email_change_request.pk)
        )

        self.token = email_change_token.make_token(
            self.email_change_request
        )

        self.url = reverse(
            'confirm_email_change',
            kwargs={
                'uidb64': self.uid,
                'token': self.token
            }
        )

    def test_confirm_email_change_with_valid_token_changes_email(self):
        response = self.client.get(self.url)

        self.user.refresh_from_db()

        self.assertEqual(self.user.email, 'novo@email.com')

    def test_confirm_email_change_deletes_request_after_confirmation(self):
        request_id = self.email_change_request.pk

        self.client.get(self.url)

        self.assertFalse(EmailChangeRequest.objects.filter(pk=request_id).exists())

    def test_confirm_email_change_with_valid_token_returns_success_template(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_change/successful_email_change.html')

    def test_confirm_email_change_with_invalid_uid_returns_unsuccessful_template(self):
        url = reverse(
            'confirm_email_change',
            kwargs={
                'uidb64': 'uid-invalido',
                'token': self.token
            }
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_change/unsuccessful_email_change.html')

    def test_confirm_email_change_with_invalid_token_does_not_change_email(self):
        url = reverse(
            'confirm_email_change',
            kwargs={
                'uidb64': self.uid,
                'token': 'token-invalido'
            }
        )

        response = self.client.get(url)

        self.user.refresh_from_db()

        self.assertEqual(self.user.email, 'antigo@email.com')
        self.assertTrue(EmailChangeRequest.objects.filter(pk=self.email_change_request.pk).exists())
        self.assertTemplateUsed(response, 'email_change/unsuccessful_email_change.html')