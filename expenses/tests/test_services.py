from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from expenses.models import Expense
from expenses.services import (
    create_expense,
    create_installment_expenses,
    create_expenses_batch
)


class ExpenseServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison',
            password='Teste123!'
        )

    def test_create_expense(self):
        expense = create_expense(
            user=self.user,
            title='Mercado',
            amount=Decimal('600.00'),
            date=date(2026, 9, 16),
            category='alimentacao'
        )

        self.assertEqual(Expense.objects.count(), 1)

        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.title, 'Mercado')
        self.assertEqual(expense.amount, Decimal('600.00'))
        self.assertEqual(expense.date, date(2026, 9, 16))
        self.assertEqual(expense.category, 'alimentacao')

        self.assertIsNone(expense.installment_number)
        self.assertIsNone(expense.total_installments)
        self.assertIsNone(expense.installment_group)

    def test_create_installment_expenses_without_interest(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='TV 4K LG',
            amount=Decimal('3000.55'),
            date=date(2026, 9, 16),
            category='compras',
            installments=10
        )

        self.assertEqual(len(expenses), 10)
        self.assertEqual(Expense.objects.count(), 10)

        self.assertEqual(expenses[0].installment_number, 1)
        self.assertEqual(expenses[9].installment_number, 10)

        self.assertEqual(expenses[0].total_installments, 10)
        self.assertEqual(expenses[9].total_installments, 10)

        self.assertEqual(expenses[0].date, date(2026, 9, 16))

        self.assertEqual(expenses[1].date, date(2026, 10, 16))

        self.assertEqual(expenses[9].date, date(2027, 6, 16))

        group = expenses[0].installment_group

        self.assertIsNotNone(group)

        for expense in expenses:
            self.assertEqual(
                expense.installment_group,
                group
            )

        self.assertEqual(expenses[0].amount, Decimal('300.05'))

        self.assertEqual(expenses[9].amount, Decimal('300.10'))

        total = sum(
            expense.amount
            for expense in expenses
        )

        self.assertEqual(total, Decimal('3000.55'))

    def test_create_installment_expenses_with_interest(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='TV 4K LG',
            amount=Decimal('3000.55'),
            date=date(2026, 9, 16),
            category='compras',
            installments=10,
            installment_amount=Decimal('350.00')
        )

        self.assertEqual(len(expenses), 10)
        self.assertEqual(Expense.objects.count(), 10)

        for expense in expenses:
            self.assertEqual(
                expense.amount,
                Decimal('350.00')
            )

        total = sum(
            expense.amount
            for expense in expenses
        )

        self.assertEqual(total, Decimal('3500.00'))

    def test_invalid_installments(self):
        for installments in [0, 1, 49]:
            with self.subTest(installments=installments):
                with self.assertRaises(ValueError):
                    create_installment_expenses(
                        user=self.user,
                        title='TV',
                        amount=Decimal('3000.00'),
                        date=date(2026, 9, 16),
                        category='compras',
                        installments=installments
                    )

        self.assertEqual(Expense.objects.count(), 0)

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            create_installment_expenses(
                user=self.user,
                title='TV',
                amount=Decimal('-100.00'),
                date=date(2026, 9, 16),
                category='compras',
                installments=10
            )

        self.assertEqual(Expense.objects.count(), 0)

    def test_invalid_installment_amount(self):
        with self.assertRaises(ValueError):
            create_installment_expenses(
                user=self.user,
                title='TV',
                amount=Decimal('3000.00'),
                date=date(2026, 9, 16),
                category='compras',
                installments=10,
                installment_amount=Decimal('-50.00')
            )

        self.assertEqual(Expense.objects.count(), 0)

    def test_installment_dates_at_end_of_month(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='Notebook',
            amount=Decimal('3000.00'),
            date=date(2026, 1, 31),
            category='compras',
            installments=3
        )

        self.assertEqual(expenses[0].date, date(2026, 1, 31))

        self.assertEqual(expenses[1].date, date(2026, 2, 28))

        self.assertEqual(expenses[2].date, date(2026, 3, 31))


class CreateExpensesBatchTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison',
            password='Teste123!'
        )

    def test_create_expenses_batch(self):
        expenses_data = [
            {
                'title': 'TV 4K LG',
                'amount': Decimal('3000.55'),
                'date': date(2026, 9, 16),
                'category': 'compras',
                'installments': 10,
            },
            {
                'title': 'Mercado parcelado',
                'amount': Decimal('3000.50'),
                'date': date(2026, 9, 16),
                'category': 'alimentacao',
                'installments': 10,
            },
            {
                'title': 'Mercado',
                'amount': Decimal('600.00'),
                'date': date(2026, 9, 16),
                'category': 'alimentacao',
            },
        ]

        created_expenses = create_expenses_batch(
            user=self.user,
            expenses_data=expenses_data
        )

        self.assertEqual(len(created_expenses), 21)

        self.assertEqual(Expense.objects.count(), 21)

        tv_expenses = Expense.objects.filter(
            title='TV 4K LG'
        )

        market_installments = Expense.objects.filter(
            title='Mercado parcelado'
        )

        market_expense = Expense.objects.get(
            title='Mercado'
        )

        self.assertEqual(
            tv_expenses.count(),
            10
        )

        self.assertEqual(
            market_installments.count(),
            10
        )

        self.assertEqual(
            market_expense.amount,
            Decimal('600.00')
        )

        self.assertIsNone(
            market_expense.installment_number
        )

        self.assertIsNone(
            market_expense.total_installments
        )

        self.assertIsNone(
            market_expense.installment_group
        )

    def test_create_expenses_batch_with_interest(self):
        expenses_data = [
            {
                'title': 'Notebook',
                'amount': Decimal('3000.00'),
                'date': date(2026, 9, 16),
                'category': 'compras',
                'installments': 10,
                'installment_amount': Decimal('350.00'),
            }
        ]

        created_expenses = create_expenses_batch(
            user=self.user,
            expenses_data=expenses_data
        )

        self.assertEqual(
            len(created_expenses),
            10
        )

        self.assertEqual(
            Expense.objects.count(),
            10
        )

        for expense in created_expenses:
            self.assertEqual(
                expense.amount,
                Decimal('350.00')
            )

        total = sum(
            expense.amount
            for expense in created_expenses
        )

        self.assertEqual(
            total,
            Decimal('3500.00')
        )

    def test_create_expenses_batch_rollback_on_error(self):
        expenses_data = [
            {
                'title': 'Mercado',
                'amount': Decimal('600.00'),
                'date': date(2026, 9, 16),
                'category': 'alimentacao',
            },
            {
                'title': 'TV inválida',
                'amount': Decimal('3000.00'),
                'date': date(2026, 9, 16),
                'category': 'compras',
                'installments': 49,
            },
        ]

        with self.assertRaises(ValueError):
            create_expenses_batch(
                user=self.user,
                expenses_data=expenses_data
            )

        self.assertEqual(
            Expense.objects.count(),
            0
        )