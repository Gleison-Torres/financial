
from django.test import TestCase
from django.urls import reverse, resolve

from categories.views import my_categories


class TestCategoriesUrls(TestCase):

    def test_url_categories_is_correct(self):
        self.assertEqual(
            reverse('categories'),
            '/categories/my-categories/'
        )

    def test_categories_url_resolves_to_correct_view(self):
        view = resolve(reverse('categories'))

        self.assertIs(
            view.func,
            my_categories
        )
