from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

from user_profile.models import EmailChangeRequest


class TestEditProfileView(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='gleison',
            email='gleison@email.com',
            first_name='Gleison'
        )

        self.url = reverse('edit_profile')

        self.form_data = {
            'fullname': 'Gleison Torres',
            'username': 'gleison',
            'email': 'gleison@email.com'
        }

    def test_edit_profile_redirects_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_edit_profile_get_returns_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_edit_profile_get_loads_initial_user_data(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        form = response.context['form']

        self.assertEqual(form.initial['fullname'], 'Gleison'
        )
        self.assertEqual(form.initial['username'], 'gleison')
        self.assertEqual(form.initial['email'], 'gleison@email.com')

    def test_edit_profile_updates_user_data(self):
        self.client.force_login(self.user)

        self.form_data['fullname'] = 'Gleison Torres'
        self.form_data['username'] = 'gleison_torres'

        response = self.client.post(self.url, self.form_data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, 'Gleison Torres')
        self.assertEqual(self.user.username, 'gleison_torres')

        self.assertRedirects(response, reverse('profile'))

    def test_edit_profile_does_not_change_email_immediately(self):
        self.client.force_login(self.user)

        self.form_data['email'] = 'novo@email.com'

        self.client.post(self.url, self.form_data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.email, 'gleison@email.com')

    def test_edit_profile_creates_email_change_request(self):
        self.client.force_login(self.user)

        self.form_data['email'] = 'novo@email.com'

        self.client.post(self.url, self.form_data)

        email_request = EmailChangeRequest.objects.get(user=self.user)

        self.assertEqual(email_request.new_email, 'novo@email.com')

    def test_edit_profile_without_email_change_does_not_create_request(self):
        self.client.force_login(self.user)

        self.client.post(self.url, self.form_data)

        self.assertFalse(EmailChangeRequest.objects.filter(user=self.user).exists())

    def test_edit_profile_success_message_without_email_change(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.form_data)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), 'Perfil atualizado com sucesso.')

    def test_edit_profile_email_change_message(self):
        self.client.force_login(self.user)

        self.form_data['email'] = 'novo@email.com'

        response = self.client.post(self.url, self.form_data)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), 'Enviamos uma confirmação para o novo e-mail.')

    def test_edit_profile_invalid_form_does_not_update_user(self):
        User.objects.create_user(
            username='joao',
            email='joao@email.com'
        )

        self.client.force_login(self.user)

        self.form_data['username'] = 'joao'

        response = self.client.post(self.url, self.form_data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, 'gleison')
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)