from django.test import TestCase
from django.urls import reverse, resolve
from user_profile.views import user_profile, edit_profile, change_password


class TestUserProfileUrls(TestCase):

    def test_url_profile_is_correct(self):
        self.assertEqual(reverse('profile'), '/profile/')

    def test_url_edit_profile_is_correct(self):
        self.assertEqual(reverse('edit_profile'), '/profile/edit-profile/')

    def test_url_change_password_is_correct(self):
        self.assertEqual(reverse('change_password'), '/profile/change-password/')

    def test_profile_url_resolves_to_correct_view(self):
        view = resolve(reverse('profile'))
        self.assertIs(view.func, user_profile)

    def test_edit_profile_url_resolves_to_correct_view(self):
        view = resolve(reverse('edit_profile'))
        self.assertIs(view.func, edit_profile)

    def test_change_password_url_resolves_to_correct_view(self):
        view = resolve(reverse('change_password'))
        self.assertIs(view.func, change_password)