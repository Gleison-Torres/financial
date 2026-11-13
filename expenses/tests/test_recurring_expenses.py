
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase

from expenses.models import Expense, RecurringExpense
from expenses.services import (
    create_recurring_expense,
    create_recurring_occurrence,
    generate_monthly_recurring_expenses,
    get_recurring_occurrence_date,
)


class RecurringExpenseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='usuario_teste',
            password='senha_teste'
        )

    def create_recurring(self, **kwargs):
        defaults = {
            'user': self.user,
            'title': 'Despesa recorrente teste',
            'amount': Decimal('100.00'),
            'category': 'lazer',
            'day_of_month': 10,
            'start_date': date(2026, 1, 10),
        }

        defaults.update(kwargs)

        return RecurringExpense.objects.create(**defaults)

    # 1. Criação da regra e da primeira ocorrência

    def test_create_recurring_expense_creates_first_occurrence(self):

        recurring, expense = create_recurring_expense(
            user=self.user,
            title='Internet',
            amount=Decimal('120.00'),
            date=date(2026, 11, 13),
            category='lazer'
        )

        self.assertIsInstance(recurring, RecurringExpense)
        self.assertIsInstance(expense, Expense)

        self.assertEqual(recurring.user, self.user)
        self.assertEqual(recurring.title, 'Internet')
        self.assertEqual(recurring.amount, Decimal('120.00'))
        self.assertEqual(recurring.day_of_month, 13)
        self.assertEqual(recurring.start_date, date(2026, 11, 13))
        self.assertTrue(recurring.is_active)

        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.title, 'Internet')
        self.assertEqual(expense.amount, Decimal('120.00'))
        self.assertEqual(expense.date, date(2026, 11, 13))
        self.assertEqual(expense.recurring_expense, recurring)

    # 2. Impedir criação de recorrência com valor inválido

    def test_create_recurring_expense_rejects_zero_or_negative_amount(self):

        invalid_amounts = [
            Decimal('0.00'),
            Decimal('-10.00'),
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    create_recurring_expense(
                        user=self.user,
                        title='Despesa inválida',
                        amount=amount,
                        date=date(2026, 11, 13),
                        category='lazer'
                    )

        self.assertEqual(RecurringExpense.objects.count(), 0)
        self.assertEqual(Expense.objects.count(), 0)

    # 3. Calcular corretamente a data de cada ocorrência

    def test_get_recurring_occurrence_date_preserves_original_day(self):

        recurring = self.create_recurring(
            day_of_month=31,
            start_date=date(2026, 1, 31)
        )

        test_cases = [
            (2027, 1, date(2027, 1, 31)),
            (2027, 2, date(2027, 2, 28)),
            (2027, 3, date(2027, 3, 31)),
            (2027, 4, date(2027, 4, 30)),
        ]

        for year, month, expected_date in test_cases:
            with self.subTest(year=year, month=month):

                occurrence_date = get_recurring_occurrence_date(
                    recurring,
                    year,
                    month
                )

                self.assertEqual(occurrence_date, expected_date)

    # 4. Criar uma ocorrência mensal

    def test_create_recurring_occurrence_creates_expense(self):

        recurring = self.create_recurring()

        expense = create_recurring_occurrence(
            recurring,
            2026,
            2
        )

        self.assertIsNotNone(expense)
        self.assertEqual(expense.recurring_expense, recurring)
        self.assertEqual(expense.date, date(2026, 2, 10))
        self.assertEqual(expense.title, recurring.title)
        self.assertEqual(expense.amount, recurring.amount)

    # 5. Não criar ocorrência antes da data de início

    def test_create_recurring_occurrence_respects_start_date(self):

        recurring = self.create_recurring(
            start_date=date(2026, 3, 15),
            day_of_month=15
        )

        expense = create_recurring_occurrence(
            recurring,
            2026,
            2
        )

        self.assertIsNone(expense)

        self.assertEqual(
            Expense.objects.filter(
                recurring_expense=recurring
            ).count(),
            0
        )

    # 6. Não criar ocorrência para recorrência inativa

    def test_create_recurring_occurrence_rejects_inactive_recurring(self):

        recurring = self.create_recurring(is_active=False)

        with self.assertRaises(ValueError):
            create_recurring_occurrence(
                recurring,
                2026,
                2
            )

        self.assertEqual(
            Expense.objects.filter(
                recurring_expense=recurring
            ).count(),
            0
        )

    # 7. Impedir duplicidade de ocorrência

    def test_create_recurring_occurrence_does_not_duplicate_expense(self):

        recurring = self.create_recurring()

        first_expense = create_recurring_occurrence(
            recurring,
            2026,
            2
        )

        second_expense = create_recurring_occurrence(
            recurring,
            2026,
            2
        )

        self.assertEqual(first_expense.id, second_expense.id)

        self.assertEqual(
            Expense.objects.filter(
                recurring_expense=recurring,
                date=date(2026, 2, 10)
            ).count(),
            1
        )

    # 8. Gerar ocorrências de todas as regras ativas

    def test_generate_monthly_recurring_expenses_creates_occurrences(self):

        recurring = self.create_recurring()

        created_expenses = generate_monthly_recurring_expenses(
            2026,
            2
        )

        self.assertEqual(len(created_expenses), 1)

        expense = created_expenses[0]

        self.assertEqual(expense.recurring_expense, recurring)
        self.assertEqual(expense.date, date(2026, 2, 10))

    # 9. Não gerar ocorrências duplicadas ao executar novamente

    def test_generate_monthly_recurring_expenses_is_idempotent(self):

        recurring = self.create_recurring()

        first_run = generate_monthly_recurring_expenses(
            2026,
            2
        )

        second_run = generate_monthly_recurring_expenses(
            2026,
            2
        )

        self.assertEqual(len(first_run), 1)
        self.assertEqual(len(second_run), 0)

        self.assertEqual(
            Expense.objects.filter(
                recurring_expense=recurring,
                date=date(2026, 2, 10)
            ).count(),
            1
        )

    # 10. Não gerar ocorrências para regras inativas

    def test_generate_monthly_recurring_expenses_ignores_inactive_rules(self):

        recurring = self.create_recurring(is_active=False)

        created_expenses = generate_monthly_recurring_expenses(
            2026,
            2
        )

        self.assertEqual(len(created_expenses), 0)

        self.assertEqual(
            Expense.objects.filter(
                recurring_expense=recurring
            ).count(),
            0
        )

    # 11. Respeitar a data de início na geração mensal

    def test_generate_monthly_recurring_expenses_respects_start_date(self):

        recurring = self.create_recurring(
            start_date=date(2026, 3, 10),
            day_of_month=10
        )

        created_expenses = generate_monthly_recurring_expenses(
            2026,
            2
        )

        self.assertEqual(len(created_expenses), 0)

        self.assertEqual(
            Expense.objects.filter(
                recurring_expense=recurring
            ).count(),
            0
        )

    # 12. Garantir unicidade no banco de dados

    def test_database_prevents_duplicate_recurring_expenses(self):

        recurring = self.create_recurring()

        Expense.objects.create(
            user=self.user,
            title=recurring.title,
            amount=recurring.amount,
            date=date(2026, 2, 10),
            category=recurring.category,
            recurring_expense=recurring
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Expense.objects.create(
                    user=self.user,
                    title=recurring.title,
                    amount=recurring.amount,
                    date=date(2026, 2, 10),
                    category=recurring.category,
                    recurring_expense=recurring
                )
