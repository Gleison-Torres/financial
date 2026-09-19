from django.test import SimpleTestCase
from django.urls import reverse, resolve

from expenses.views import add_new_expenses


class ExpenseUrlsTest(SimpleTestCase):

    def test_new_expenses_url(self):
        url = reverse('new_expenses')

        self.assertEqual(url, '/expenses/new-expenses/')

    def test_new_expenses_url_resolves_correct_view(self):
        resolver = resolve('/expenses/new-expenses/')

        self.assertEqual(resolver.func, add_new_expenses)