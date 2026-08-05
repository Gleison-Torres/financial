from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import register, login


class TestAccountsUrls(TestCase):

    def test_url_register_is_correct(self):
        self.assertEqual(reverse('register'), '/accounts/register/')

    def test_url_login_is_correct(self):
        self.assertEqual(reverse('login'), '/accounts/login/')

    def test_register_url_resolves_to_correct_view(self):
        view = resolve(reverse('register'))
        self.assertIs(view.func, register)

    def test_login_url_resolves_to_correct_view(self):
        view = resolve(reverse('login'))
        self.assertIs(view.func, login)
