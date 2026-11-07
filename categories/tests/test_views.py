
from datetime import date
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from categories.views import my_categories


class MyCategoriesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison'
        )

        self.url = reverse('categories')

    def test_my_categories_requires_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}"
        )

    def test_my_categories_authenticated_user_can_access_page(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_categories.html')

    @patch('categories.views.get_monthly_expenses_by_category_page')
    @patch('categories.views.timezone.localdate')
    def test_my_categories_uses_current_month_as_default(
        self,
        mock_localdate,
        mock_get_expenses
    ):
        mock_localdate.return_value = date(2026, 11, 5)
        mock_get_expenses.return_value = []

        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(
            response.context['current_month'],
            date(2026, 11, 1)
        )

        mock_get_expenses.assert_called_once_with(
            user=self.user,
            year=2026,
            month=11,
            start_date=None,
            end_date=None
        )

    @patch('categories.views.timezone.localdate')
    def test_my_categories_calculates_previous_and_next_month(
        self,
        mock_localdate
    ):
        mock_localdate.return_value = date(2026, 9, 15)

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        self.assertEqual(
            response.context['current_month'],
            date(2026, 9, 1)
        )

        self.assertEqual(
            response.context['previous_month'],
            date(2026, 8, 1)
        )

        self.assertEqual(
            response.context['next_month'],
            date(2026, 10, 1)
        )

    @patch('categories.views.timezone.localdate')
    def test_my_categories_month_navigation_handles_year_change(
        self,
        mock_localdate
    ):
        mock_localdate.return_value = date(2026, 12, 15)

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 12
            }
        )

        self.assertEqual(
            response.context['previous_month'],
            date(2026, 11, 1)
        )

        self.assertEqual(
            response.context['next_month'],
            date(2027, 1, 1)
        )

    @patch('categories.views.timezone.localdate')
    def test_my_categories_invalid_month_uses_current_month(
        self,
        mock_localdate
    ):
        mock_localdate.return_value = date(2026, 11, 5)

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 13
            }
        )

        self.assertEqual(
            response.context['current_month'],
            date(2026, 11, 1)
        )

    @patch('categories.views.get_monthly_expenses_by_category_page')
    def test_my_categories_filters_by_custom_date_range(
        self,
        mock_get_expenses
    ):
        mock_get_expenses.return_value = []

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'start': '2026-01-01',
                'end': '2026-03-31'
            }
        )

        self.assertTrue(response.context['custom_period'])

        self.assertEqual(
            response.context['start_date'],
            date(2026, 1, 1)
        )

        self.assertEqual(
            response.context['end_date'],
            date(2026, 3, 31)
        )

        mock_get_expenses.assert_called_once_with(
            user=self.user,
            year=response.context['current_month'].year,
            month=response.context['current_month'].month,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 3, 31)
        )

    @patch('categories.views.get_monthly_expenses_by_category_page')
    def test_my_categories_ignores_incomplete_custom_period(
        self,
        mock_get_expenses
    ):
        mock_get_expenses.return_value = []

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'start': '2026-01-01'
            }
        )

        self.assertFalse(response.context['custom_period'])

        self.assertIsNone(response.context['end_date'])

        mock_get_expenses.assert_called_once_with(
            user=self.user,
            year=response.context['current_month'].year,
            month=response.context['current_month'].month,
            start_date=None,
            end_date=None
        )

    def test_my_categories_preserves_name_and_category_filters(self):
        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'q': 'Supermercado',
                'category': 'alimentacao'
            }
        )

        self.assertEqual(
            response.context['filter_name'],
            'Supermercado'
        )

        self.assertEqual(
            response.context['filter_category'],
            'alimentacao'
        )

    @patch('categories.views.get_monthly_expenses_by_category_page')
    def test_my_categories_passes_expenses_to_template_context(
        self,
        mock_get_expenses
    ):
        expenses = [
            {
                'title': 'Supermercado',
                'category': 'Alimentação',
                'date': '2026-11-05',
                'amount': '350.00',
                'is_paid': False
            }
        ]

        mock_get_expenses.return_value = expenses

        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(
            response.context['expenses_json'],
            expenses
        )
