from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from expenses.models import Expense
from expenses.services import create_installment_expenses


class MyExpensesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison'
        )

        self.url = reverse('my_expenses')

    def test_my_expenses_requires_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}"
        )

    def test_my_expenses_authenticated_user_can_access_page(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_expenses.html')

    def test_my_expenses_only_shows_logged_user_expenses(self):
        other_user = User.objects.create_user(
            username='outro'
        )

        Expense.objects.create(
            user=self.user,
            title='Minha despesa',
            amount=Decimal('100.00'),
            date=date(2026, 9, 10),
            category='compras'
        )

        Expense.objects.create(
            user=other_user,
            title='Despesa de outro usuário',
            amount=Decimal('500.00'),
            date=date(2026, 9, 10),
            category='compras'
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        expenses = response.context['expenses']

        self.assertEqual(expenses.count(), 1)
        self.assertEqual(
            expenses.first().title,
            'Minha despesa'
        )

    def test_my_expenses_filters_expenses_by_month(self):
        Expense.objects.create(
            user=self.user,
            title='Despesa setembro',
            amount=Decimal('100.00'),
            date=date(2026, 9, 10),
            category='compras'
        )

        Expense.objects.create(
            user=self.user,
            title='Despesa outubro',
            amount=Decimal('200.00'),
            date=date(2026, 10, 10),
            category='compras'
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        expenses = response.context['expenses']

        self.assertEqual(expenses.count(), 1)
        self.assertEqual(
            expenses.first().title,
            'Despesa setembro'
        )

    def test_my_expenses_calculates_month_total_and_count(self):
        Expense.objects.create(
            user=self.user,
            title='Mercado',
            amount=Decimal('600.00'),
            date=date(2026, 9, 10),
            category='alimentacao'
        )

        Expense.objects.create(
            user=self.user,
            title='Internet',
            amount=Decimal('100.00'),
            date=date(2026, 9, 15),
            category='outros'
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        self.assertEqual(
            response.context['month_total'],
            Decimal('700.00')
        )
        self.assertEqual(
            response.context['month_count'],
            2
        )

    def test_my_expenses_orders_expenses_by_date_descending(self):
        Expense.objects.create(
            user=self.user,
            title='Mais antiga',
            amount=Decimal('100.00'),
            date=date(2026, 9, 5),
            category='outros'
        )

        Expense.objects.create(
            user=self.user,
            title='Mais recente',
            amount=Decimal('200.00'),
            date=date(2026, 9, 25),
            category='outros'
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        expenses = list(response.context['expenses'])

        self.assertEqual(
            expenses[0].title,
            'Mais recente'
        )
        self.assertEqual(
            expenses[1].title,
            'Mais antiga'
        )

    def test_my_expenses_includes_installment_summary(self):
        create_installment_expenses(
            user=self.user,
            title='Mesa',
            amount=Decimal('500.00'),
            date=date(2026, 8, 10),
            category='compras',
            installments=5
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        summaries = response.context['installment_summaries']

        self.assertEqual(len(summaries), 1)

        summary = summaries[0]

        self.assertEqual(
            summary['expense'].installment_number,
            2
        )
        self.assertEqual(
            summary['expense'].total_installments,
            5
        )
        self.assertEqual(
            summary['total_amount'],
            Decimal('500.00')
        )
        self.assertEqual(
            summary['remaining_amount'],
            Decimal('400.00')
        )

    def test_my_expenses_does_not_include_simple_expense_in_installment_summaries(self):
        Expense.objects.create(
            user=self.user,
            title='Mercado',
            amount=Decimal('200.00'),
            date=date(2026, 9, 10),
            category='alimentacao'
        )

        self.client.force_login(self.user)

        response = self.client.get(
            self.url,
            {
                'year': 2026,
                'month': 9
            }
        )

        self.assertEqual(
            len(response.context['installment_summaries']),
            0
        )

    def test_my_expenses_calculates_previous_and_next_month(self):
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

    def test_my_expenses_month_navigation_handles_year_change(self):
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