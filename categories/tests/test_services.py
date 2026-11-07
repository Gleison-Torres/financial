
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from expenses.models import Expense
from categories.services import get_monthly_expenses_by_category_page


class GetMonthlyExpensesByCategoryPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison'
        )

        self.other_user = User.objects.create_user(
            username='outro'
        )

    def create_expense(
        self,
        title,
        amount,
        expense_date,
        category='outros',
        is_paid=False,
        user=None
    ):
        return Expense.objects.create(
            user=user or self.user,
            title=title,
            amount=Decimal(amount),
            date=expense_date,
            category=category,
            is_paid=is_paid
        )

    def test_filters_expenses_by_month_and_year(self):
        self.create_expense(
            title='Despesa setembro',
            amount='100.00',
            expense_date=date(2026, 9, 10)
        )

        self.create_expense(
            title='Despesa outubro',
            amount='200.00',
            expense_date=date(2026, 10, 10)
        )

        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9
        )

        self.assertEqual(len(expenses), 1)
        self.assertEqual(
            expenses[0]['title'],
            'Despesa setembro'
        )

    def test_filters_expenses_by_custom_date_range(self):
        self.create_expense(
            title='Despesa janeiro',
            amount='100.00',
            expense_date=date(2026, 1, 10)
        )

        self.create_expense(
            title='Despesa fevereiro',
            amount='200.00',
            expense_date=date(2026, 2, 10)
        )

        self.create_expense(
            title='Despesa março',
            amount='300.00',
            expense_date=date(2026, 3, 10)
        )

        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 2, 28)
        )

        self.assertEqual(len(expenses), 2)

        titles = [expense['title'] for expense in expenses]

        self.assertIn('Despesa janeiro', titles)
        self.assertIn('Despesa fevereiro', titles)
        self.assertNotIn('Despesa março', titles)

    def test_returns_only_logged_user_expenses(self):
        self.create_expense(
            title='Minha despesa',
            amount='100.00',
            expense_date=date(2026, 9, 10)
        )

        self.create_expense(
            title='Despesa de outro usuário',
            amount='500.00',
            expense_date=date(2026, 9, 10),
            user=self.other_user
        )

        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9
        )

        self.assertEqual(len(expenses), 1)
        self.assertEqual(
            expenses[0]['title'],
            'Minha despesa'
        )

    def test_orders_expenses_by_date_descending(self):
        self.create_expense(
            title='Despesa mais antiga',
            amount='100.00',
            expense_date=date(2026, 9, 5)
        )

        self.create_expense(
            title='Despesa mais recente',
            amount='200.00',
            expense_date=date(2026, 9, 25)
        )

        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9
        )

        self.assertEqual(
            expenses[0]['title'],
            'Despesa mais recente'
        )

        self.assertEqual(
            expenses[1]['title'],
            'Despesa mais antiga'
        )

    def test_includes_paid_and_pending_expenses(self):
        self.create_expense(
            title='Despesa paga',
            amount='100.00',
            expense_date=date(2026, 9, 10),
            is_paid=True
        )

        self.create_expense(
            title='Despesa pendente',
            amount='200.00',
            expense_date=date(2026, 9, 15),
            is_paid=False
        )

        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9
        )

        self.assertEqual(len(expenses), 2)

        paid_status = [expense['is_paid'] for expense in expenses]

        self.assertIn(True, paid_status)
        self.assertIn(False, paid_status)

    def test_returns_empty_list_when_no_expenses_exist(self):
        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9
        )

        self.assertEqual(expenses, [])

    def test_returns_expenses_with_expected_data_structure(self):
        self.create_expense(
            title='Supermercado',
            amount='350.00',
            expense_date=date(2026, 9, 15),
            category='alimentacao',
            is_paid=False
        )

        expenses = get_monthly_expenses_by_category_page(
            user=self.user,
            year=2026,
            month=9
        )

        self.assertEqual(
            expenses[0],
            {
                'title': 'Supermercado',
                'category': 'Alimentação',
                'date': '2026-09-15',
                'amount': '350.00',
                'is_paid': False
            }
        )
