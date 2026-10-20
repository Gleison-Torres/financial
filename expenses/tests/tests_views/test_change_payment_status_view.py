from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from expenses.models import Expense


class ChangePaymentStatusViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='payment_user',
            password='Teste123!'
        )

        self.expense = Expense.objects.create(
            user=self.user,
            title='Mercado',
            amount=Decimal('200.00'),
            date=date(2026, 10, 15),
            category='alimentacao'
        )

        self.url = reverse(
            'change_payment_status',
            args=[self.expense.id]
        )

        self.client.force_login(self.user)

    def test_mark_expense_as_paid(self):
        response = self.client.post(self.url)

        self.expense.refresh_from_db()

        self.assertTrue(self.expense.is_paid)
        self.assertRedirects(response, reverse('my_expenses'))

    def test_revert_expense_to_pending(self):
        self.expense.is_paid = True
        self.expense.save()

        response = self.client.post(self.url)

        self.expense.refresh_from_db()

        self.assertFalse(self.expense.is_paid)
        self.assertRedirects(response, reverse('my_expenses'))

    def test_unauthenticated_user_cannot_change_payment_status(self):
        self.client.logout()

        response = self.client.post(self.url)

        self.expense.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        self.assertFalse(self.expense.is_paid)

    def test_user_cannot_change_another_users_expense(self):
        other_user = get_user_model().objects.create_user(
            username='other_payment_user',
            password='Teste123!'
        )

        other_expense = Expense.objects.create(
            user=other_user,
            title='Notebook',
            amount=Decimal('1500.00'),
            date=date(2026, 10, 15),
            category='compras'
        )

        url = reverse(
            'change_payment_status',
            args=[other_expense.id]
        )

        response = self.client.post(url)

        other_expense.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(other_expense.is_paid)

    def test_get_request_is_not_allowed(self):
        response = self.client.get(self.url)

        self.expense.refresh_from_db()

        self.assertEqual(response.status_code, 405)
        self.assertFalse(self.expense.is_paid)