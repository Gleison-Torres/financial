from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from expenses.models import Expense
from expenses.services import create_expense, create_installment_expenses


class ExpenseOperationViewBase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='view_user', password='Teste123!')
        self.other_user = get_user_model().objects.create_user(username='other_view_user', password='Teste123!')

    def make_simple(self, user=None):
        return create_expense(user=user or self.user, title='Mercado',
                              amount=Decimal('150.00'), date=date(2026, 10, 7),
                              category='alimentacao')

    def make_installments(self, user=None):
        return create_installment_expenses(user=user or self.user, title='Notebook',
                                           amount=Decimal('1200.00'), date=date(2026, 10, 7),
                                           category='compras', installments=3)

    def edit_data(self, **overrides):
        data = {'title': 'Despesa alterada', 'amount': '900.00',
                'date': '2026-11-15', 'category': 'compras'}
        data.update(overrides)
        return data


class DeleteExpenseViewTest(ExpenseOperationViewBase):
    def test_login_required(self):

        expense = self.make_simple()
        response = self.client.post(reverse('delete_expenses', args=[expense.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
        self.assertTrue(Expense.objects.filter(pk=expense.pk).exists())

    def test_get_not_allowed(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_expenses', args=[expense.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Expense.objects.filter(pk=expense.pk).exists())

    def test_delete_simple_post(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_expenses', args=[expense.pk]))

        self.assertRedirects(response, reverse('my_expenses'))
        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())

    def test_delete_installment_post_removes_group_only(self):

        installments = self.make_installments()
        preserved = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_expenses', args=[installments[1].pk]))

        self.assertRedirects(response, reverse('my_expenses'))
        self.assertFalse(Expense.objects.filter(installment_group=installments[0].installment_group).exists())
        self.assertTrue(Expense.objects.filter(pk=preserved.pk).exists())

    def test_cannot_delete_another_users_expense(self):

        expense = self.make_simple(user=self.other_user)
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_expenses', args=[expense.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Expense.objects.filter(pk=expense.pk).exists())

    def test_nonexistent_expense_returns_404(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_expenses', args=[999999]))

        self.assertEqual(response.status_code, 404)


class EditExpenseViewTest(ExpenseOperationViewBase):
    def test_login_required(self):

        expense = self.make_simple()
        response = self.client.get(reverse('edit_expenses', args=[expense.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_get_simple_prefills_form(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_expenses', args=[expense.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['expense'], expense)
        form = response.context['form']
        self.assertEqual(form.initial['title'], 'Mercado')
        self.assertEqual(form.initial['amount'], Decimal('150.00'))
        self.assertFalse(form.initial['is_installment'])

    def test_get_installments_prefills_total_and_first_date(self):

        installments = self.make_installments()
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_expenses', args=[installments[1].pk]))

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.initial['amount'], Decimal('1200.00'))
        self.assertEqual(form.initial['date'], date(2026, 10, 7))
        self.assertTrue(form.initial['is_installment'])
        self.assertEqual(form.initial['installments'], 3)

    def test_post_simple_to_simple(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[expense.pk]), self.edit_data())

        self.assertRedirects(response, reverse('my_expenses'))
        expense.refresh_from_db()
        self.assertEqual(expense.title, 'Despesa alterada')
        self.assertEqual(expense.amount, Decimal('900.00'))
        self.assertEqual(Expense.objects.count(), 1)

    def test_post_simple_to_installments(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[expense.pk]),
                                    self.edit_data(is_installment='on', installments='3'))

        self.assertRedirects(response, reverse('my_expenses'))
        self.assertEqual(Expense.objects.count(), 3)
        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())
        self.assertEqual(list(Expense.objects.order_by('installment_number').values_list('amount', flat=True)),
                         [Decimal('300.00')] * 3)

    def test_post_installments_to_simple(self):

        installments = self.make_installments()
        group = installments[0].installment_group
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[installments[1].pk]), self.edit_data())

        self.assertRedirects(response, reverse('my_expenses'))
        self.assertFalse(Expense.objects.filter(installment_group=group).exists())
        self.assertEqual(Expense.objects.count(), 1)
        self.assertIsNone(Expense.objects.get().installment_group)

    def test_post_installments_to_installments(self):

        installments = self.make_installments()
        group = installments[0].installment_group
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[installments[0].pk]),
                                    self.edit_data(is_installment='on', installments='2'))

        self.assertRedirects(response, reverse('my_expenses'))
        self.assertFalse(Expense.objects.filter(installment_group=group).exists())
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(list(Expense.objects.order_by('installment_number').values_list('amount', flat=True)),
                         [Decimal('450.00')] * 2)

    def test_post_installments_with_interest(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[expense.pk]),
                                    self.edit_data(is_installment='on', installments='3',
                                                   has_interest='on', installment_amount='350.00'))

        self.assertRedirects(response, reverse('my_expenses'))
        self.assertEqual(list(Expense.objects.order_by('installment_number').values_list('amount', flat=True)),
                         [Decimal('350.00')] * 3)

    def test_invalid_post_keeps_expense_and_renders_errors(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[expense.pk]),
                                    self.edit_data(amount='-1'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal('150.00'))

    def test_missing_installment_count_is_invalid(self):

        expense = self.make_simple()
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[expense.pk]),
                                    self.edit_data(is_installment='on'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('installments', response.context['form'].errors)
        self.assertEqual(Expense.objects.count(), 1)

    def test_cannot_get_another_users_expense(self):

        expense = self.make_simple(user=self.other_user)
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_expenses', args=[expense.pk]))

        self.assertEqual(response.status_code, 404)

    def test_cannot_edit_another_users_expense(self):
        expense = self.make_simple(user=self.other_user)
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_expenses', args=[expense.pk]), self.edit_data())

        self.assertEqual(response.status_code, 404)
        expense.refresh_from_db()

        self.assertEqual(expense.title, 'Mercado')

    def test_nonexistent_expense_returns_404(self):

        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_expenses', args=[999999]))

        self.assertEqual(response.status_code, 404)
