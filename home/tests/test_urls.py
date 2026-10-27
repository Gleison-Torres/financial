from django.test import TestCase
from django.urls import reverse, resolve
from home.views import home


class TestHomeUrls(TestCase):

    def test_url_home_is_correct(self):
        self.assertEqual(reverse('home'), '/')

    def test_home_url_resolves_to_correct_view(self):
        view = resolve(reverse('home'))
        self.assertIs(view.func, home)