import uuid
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from expenses.models import Expense


class ExpenseModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison',
            password='Teste123!'
        )

        self.expense = Expense.objects.create(
            user=self.user,
            title='Supermercado',
            amount=Decimal('500.00'),
            date=date(2026, 9, 17),
            category='alimentacao'
        )

    def test_create_expense(self):
        self.assertEqual(
            Expense.objects.count(),
            1
        )

        self.assertEqual(
            self.expense.user,
            self.user
        )

        self.assertEqual(
            self.expense.title,
            'Supermercado'
        )

        self.assertEqual(
            self.expense.amount,
            Decimal('500.00')
        )

        self.assertEqual(
            self.expense.date,
            date(2026, 9, 17)
        )

        self.assertEqual(
            self.expense.category,
            'alimentacao'
        )

    def test_installment_fields_are_optional(self):
        self.assertIsNone(
            self.expense.installment_number
        )

        self.assertIsNone(
            self.expense.total_installments
        )

        self.assertIsNone(
            self.expense.installment_group
        )

    def test_create_installment_expense(self):
        installment_group = uuid.uuid4()

        expense = Expense.objects.create(
            user=self.user,
            title='Notebook',
            amount=Decimal('1000.00'),
            date=date(2026, 9, 17),
            category='compras',
            installment_number=1,
            total_installments=3,
            installment_group=installment_group
        )

        self.assertEqual(
            expense.installment_number,
            1
        )

        self.assertEqual(
            expense.total_installments,
            3
        )

        self.assertEqual(
            expense.installment_group,
            installment_group
        )

    def test_expense_string_representation(self):
        self.assertEqual(
            str(self.expense),
            'Supermercado'
        )

    def test_expense_category_display(self):
        self.assertEqual(
            self.expense.get_category_display(),
            'Alimentação'
        )

    def test_user_expenses_related_name(self):
        expenses = self.user.expenses.all()

        self.assertIn(
            self.expense,
            expenses
        )

    def test_delete_user_deletes_expenses(self):
        self.user.delete()

        self.assertEqual(
            Expense.objects.count(),
            0
        )

    def test_created_at_is_set_automatically(self):
        self.assertIsNotNone(
            self.expense.created_at
        )