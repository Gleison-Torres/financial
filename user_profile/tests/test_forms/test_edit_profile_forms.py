from django.test import TestCase
from django.contrib.auth.models import User

from user_profile.forms import EditProfileForms


class TestEditProfileForms(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='gleison',
            email='gleison@email.com',
            first_name='Gleison'
        )

        self.other_user = User.objects.create_user(
            username='joao',
            email='joao@email.com'
        )

        self.form_data = {
            'fullname': 'Gleison Torres',
            'username': 'gleison',
            'email': 'gleison@email.com'
        }

    def test_edit_profile_form_valid(self):
        form = EditProfileForms(self.user, self.form_data)

        self.assertTrue(form.is_valid())

    def test_username_already_in_use(self):
        self.form_data['username'] = 'joao'

        form = EditProfileForms(
            self.user,
            self.form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0], 'Este nome de usuário já está em uso.')

    def test_email_already_in_use(self):
        self.form_data['email'] = 'joao@email.com'

        form = EditProfileForms(
            self.user,
            self.form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Este e-mail já está em uso.')

    def test_email_validation_is_case_insensitive(self):
        self.form_data['email'] = 'JOAO@EMAIL.COM'

        form = EditProfileForms(
            self.user,
            self.form_data
        )

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Este e-mail já está em uso.')