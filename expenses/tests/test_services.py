from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.test import TestCase

from expenses.models import Expense
from expenses.services import (
    create_expense,
    create_installment_expenses,
    create_expenses_batch,
    get_installment_summary,
    delete_expense,
    update_expense
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

    def test_get_installment_summary_first_installment(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='Mesa',
            amount=Decimal('500.00'),
            date=date(2026, 8, 10),
            category='compras',
            installments=5
        )

        summary = get_installment_summary(expenses[0])

        self.assertEqual(summary['expense'], expenses[0])
        self.assertEqual(summary['total_amount'], Decimal('500.00'))
        self.assertEqual(summary['remaining_amount'], Decimal('500.00'))

    def test_get_installment_summary_middle_installment(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='Mesa',
            amount=Decimal('500.00'),
            date=date(2026, 8, 10),
            category='compras',
            installments=5
        )

        summary = get_installment_summary(expenses[1])

        self.assertEqual(summary['expense'].installment_number, 2)
        self.assertEqual(summary['total_amount'], Decimal('500.00'))
        self.assertEqual(summary['remaining_amount'], Decimal('400.00'))

    def test_get_installment_summary_last_installment(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='Mesa',
            amount=Decimal('500.00'),
            date=date(2026, 8, 10),
            category='compras',
            installments=5
        )

        summary = get_installment_summary(expenses[4])

        self.assertEqual(summary['expense'].installment_number, 5)
        self.assertEqual(summary['total_amount'], Decimal('500.00'))
        self.assertEqual(summary['remaining_amount'], Decimal('100.00'))

    def test_get_installment_summary_respects_installment_rounding(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='TV 4K LG',
            amount=Decimal('3000.55'),
            date=date(2026, 9, 16),
            category='compras',
            installments=10
        )

        summary = get_installment_summary(expenses[8])

        self.assertEqual(summary['expense'].installment_number, 9)
        self.assertEqual(summary['total_amount'], Decimal('3000.55'))
        self.assertEqual(summary['remaining_amount'], Decimal('600.15'))

    def test_get_installment_summary_with_interest(self):
        expenses = create_installment_expenses(
            user=self.user,
            title='Notebook',
            amount=Decimal('3000.00'),
            date=date(2026, 9, 16),
            category='compras',
            installments=10,
            installment_amount=Decimal('350.00')
        )

        summary = get_installment_summary(expenses[3])

        self.assertEqual(summary['expense'].installment_number, 4)
        self.assertEqual(summary['total_amount'], Decimal('3500.00'))
        self.assertEqual(summary['remaining_amount'], Decimal('2450.00'))


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


class DeleteExpenseServiceTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='delete_user', password='Teste123!')
        self.other_user = get_user_model().objects.create_user(username='other_delete_user', password='Teste123!')

    def make_simple(self, user=None, title='Mercado'):
        return create_expense(user=user or self.user, title=title,
                              amount=Decimal('150.00'), date=date(2026, 10, 7),
                              category='alimentacao')

    def make_installments(self, user=None, title='Notebook'):
        return create_installment_expenses(user=user or self.user, title=title,
                                           amount=Decimal('1200.00'), date=date(2026, 10, 7),
                                           category='compras', installments=3)

    def test_delete_simple_expense(self):

        expense = self.make_simple()
        delete_expense(expense)

        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())

    def test_delete_simple_preserves_other_expenses(self):

        expense = self.make_simple()
        preserved = self.make_simple(title='Padaria')
        other = self.make_simple(user=self.other_user)
        delete_expense(expense)

        self.assertCountEqual(Expense.objects.values_list('pk', flat=True), [preserved.pk, other.pk])

    def test_delete_one_installment_deletes_entire_group(self):

        installments = self.make_installments()
        group = installments[0].installment_group
        delete_expense(installments[1])

        self.assertFalse(Expense.objects.filter(installment_group=group).exists())

    def test_delete_installments_preserves_other_groups_and_users(self):

        installments = self.make_installments()
        preserved_group = self.make_installments(title='Celular')
        other_user_group = self.make_installments(user=self.other_user)
        simple = self.make_simple()
        delete_expense(installments[2])

        self.assertEqual(Expense.objects.count(), 7)
        self.assertTrue(Expense.objects.filter(pk=simple.pk).exists())
        self.assertEqual(Expense.objects.filter(installment_group=preserved_group[0].installment_group).count(), 3)
        self.assertEqual(Expense.objects.filter(installment_group=other_user_group[0].installment_group).count(), 3)


class UpdateExpenseServiceTest(TestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(username='update_user', password='Teste123!')
        self.other_user = get_user_model().objects.create_user(username='other_update_user', password='Teste123!')

    def make_simple(self, user=None, title='Mercado'):
        return create_expense(user=user or self.user, title=title,
                              amount=Decimal('150.00'), date=date(2026, 10, 7),
                              category='alimentacao')

    def make_installments(self, user=None, title='Notebook'):
        return create_installment_expenses(user=user or self.user, title=title,
                                           amount=Decimal('1200.00'), date=date(2026, 10, 7),
                                           category='compras', installments=3)

    def update(self, expense, **overrides):
        data = dict(title='Atualizada', amount=Decimal('900.00'),
                    date=date(2026, 11, 15), category='compras',
                    is_installment=False, installments=None, installment_amount=None)
        data.update(overrides)

        return update_expense(expense=expense, **data)

    def test_simple_to_simple_updates_same_record(self):
        expense = self.make_simple()
        result = self.update(expense)
        expense.refresh_from_db()

        self.assertEqual(result.pk, expense.pk)
        self.assertEqual(expense.title, 'Atualizada')
        self.assertEqual(expense.amount, Decimal('900.00'))
        self.assertEqual(expense.date, date(2026, 11, 15))
        self.assertEqual(expense.category, 'compras')
        self.assertIsNone(expense.installment_group)
        self.assertEqual(Expense.objects.count(), 1)

    def test_simple_to_installments(self):
        expense = self.make_simple()
        old_id = expense.pk
        result = self.update(expense, is_installment=True, installments=3)

        self.assertFalse(Expense.objects.filter(pk=old_id).exists())
        self.assertEqual(len(result), 3)
        self.assertEqual([item.amount for item in result], [Decimal('300.00')] * 3)
        self.assertEqual([item.installment_number for item in result], [1, 2, 3])
        self.assertEqual([item.date for item in result],
                         [date(2026, 11, 15), date(2026, 12, 15), date(2027, 1, 15)])
        self.assertEqual(Expense.objects.count(), 3)
        self.assertEqual(len({item.installment_group for item in result}), 1)

    def test_installments_to_simple(self):

        installments = self.make_installments()
        old_group = installments[0].installment_group
        result = self.update(installments[1])

        self.assertFalse(Expense.objects.filter(installment_group=old_group).exists())
        self.assertEqual(Expense.objects.count(), 1)
        self.assertIsNone(result.installment_group)
        self.assertEqual(result.amount, Decimal('900.00'))
        self.assertEqual(result.title, 'Atualizada')

    def test_installments_to_installments_replaces_group(self):

        installments = self.make_installments()
        old_group = installments[0].installment_group
        result = self.update(installments[1], is_installment=True, installments=2)

        self.assertFalse(Expense.objects.filter(installment_group=old_group).exists())
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual([item.amount for item in result], [Decimal('450.00')] * 2)
        self.assertNotEqual(result[0].installment_group, old_group)

    def test_installments_to_installments_with_custom_amount(self):

        installments = self.make_installments()
        result = self.update(installments[0], is_installment=True, installments=3,
                             installment_amount=Decimal('350.00'))

        self.assertEqual([item.amount for item in result], [Decimal('350.00')] * 3)
        self.assertEqual(Expense.objects.count(), 3)

    def test_editing_one_group_preserves_other_expenses(self):
        installments = self.make_installments()
        other_group = self.make_installments(title='Celular')
        other_user_group = self.make_installments(user=self.other_user)
        simple = self.make_simple()
        self.update(installments[0], is_installment=True, installments=2)

        self.assertEqual(Expense.objects.count(), 9)
        self.assertTrue(Expense.objects.filter(pk=simple.pk).exists())
        self.assertEqual(Expense.objects.filter(installment_group=other_group[0].installment_group).count(), 3)
        self.assertEqual(Expense.objects.filter(installment_group=other_user_group[0].installment_group).count(), 3)

    def test_invalid_conversion_rolls_back_deleted_simple(self):
        expense = self.make_simple()

        expense_id = expense.pk

        with self.assertRaises(ValueError):
            self.update(expense, is_installment=True, installments=49)

        self.assertTrue(Expense.objects.filter(pk=expense_id).exists()
)
        self.assertEqual(Expense.objects.count(), 1)

    def test_invalid_conversion_rolls_back_deleted_installments(self):
        installments = self.make_installments()
        group = installments[0].installment_group

        with self.assertRaises(ValueError):
            self.update(installments[1], is_installment=True, installments=49)

        self.assertEqual(Expense.objects.filter(installment_group=group).count(), 3)

    def test_simple_update_does_not_change_another_users_record(self):

        other = self.make_simple(user=self.other_user)
        expense = self.make_simple()
        self.update(expense)
        other.refresh_from_db()

        self.assertEqual(other.title, 'Mercado')
        self.assertEqual(other.amount, Decimal('150.00'))