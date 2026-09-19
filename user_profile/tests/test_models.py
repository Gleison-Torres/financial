from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from user_profile.models import EmailChangeRequest


class TestEmailChangeRequestModel(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='gleison',
            email='gleison@email.com'
        )

    def test_email_change_request_is_created_correctly(self):
        email_change_request = EmailChangeRequest.objects.create(
            user=self.user,
            new_email='novo@email.com'
        )

        self.assertEqual(email_change_request.user, self.user)
        self.assertEqual(email_change_request.new_email, 'novo@email.com')
        self.assertIsNotNone(email_change_request.created_at)

    def test_email_change_request_str(self):
        email_change_request = EmailChangeRequest.objects.create(user=self.user, new_email='novo@email.com')

        self.assertEqual(str(email_change_request), 'gleison -> novo@email.com')

    def test_user_cannot_have_more_than_one_email_change_request(self):
        EmailChangeRequest.objects.create(
            user=self.user,
            new_email='primeiro@email.com'
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                EmailChangeRequest.objects.create(
                    user=self.user,
                    new_email='segundo@email.com'
                )

    def test_email_change_request_is_deleted_when_user_is_deleted(self):
        email_change_request = EmailChangeRequest.objects.create(
            user=self.user,
            new_email='novo@email.com'
        )

        request_id = email_change_request.pk

        self.user.delete()

        self.assertFalse(EmailChangeRequest.objects.filter(pk=request_id).exists())