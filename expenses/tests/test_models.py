import uuid
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from expenses.models import Expense, RecurringExpense


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

    # 9. Criar uma regra de despesa recorrente
    def test_create_recurring_expense(self):
        recurring = RecurringExpense.objects.create(
            user=self.user,
            title='Internet',
            amount=Decimal('120.00'),
            category='lazer',
            day_of_month=10,
            start_date=date(2026, 9, 10)
        )

        self.assertEqual(recurring.user, self.user)
        self.assertEqual(recurring.title, 'Internet')
        self.assertEqual(recurring.amount, Decimal('120.00'))
        self.assertEqual(recurring.category, 'lazer')
        self.assertEqual(recurring.day_of_month, 10)
        self.assertEqual(recurring.start_date, date(2026, 9, 10))
        self.assertTrue(recurring.is_active)

    # 10. Testar representação textual da recorrência

    def test_recurring_expense_string_representation(self):
        recurring = RecurringExpense.objects.create(
            user=self.user,
            title='Internet',
            amount=Decimal('120.00'),
            category='lazer',
            day_of_month=10,
            start_date=date(2026, 9, 10)
        )

        self.assertEqual(str(recurring), 'Internet')

    # 11. Testar relacionamento reverso das recorrências

    def test_user_recurring_expenses_related_name(self):
        recurring = RecurringExpense.objects.create(
            user=self.user,
            title='Aluguel',
            amount=Decimal('1500.00'),
            category='moradia',
            day_of_month=10,
            start_date=date(2026, 9, 10)
        )

        self.assertIn(
            recurring,
            self.user.recurring_expenses.all()
        )

    # 12. Garantir que excluir o usuário exclui suas recorrências

    def test_delete_user_deletes_recurring_expenses(self):
        RecurringExpense.objects.create(
            user=self.user,
            title='Internet',
            amount=Decimal('120.00'),
            category='lazer',
            day_of_month=10,
            start_date=date(2026, 9, 10)
        )

        self.user.delete()

        self.assertEqual(
            RecurringExpense.objects.count(),
            0
        )