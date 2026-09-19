from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from expenses.forms import ExpenseForm


class AddNewExpensesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='gleison',
            email='gleison@email.com',
            password='Senha@123'
        )

        self.url = reverse('new_expenses')

        self.client.login(
            username='gleison',
            password='Senha@123'
        )

    def test_view_requires_login(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_get_returns_status_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'new_expenses.html'
        )

    def test_get_contains_expense_form(self):
        response = self.client.get(self.url)

        self.assertIsInstance(
            response.context['form'],
            ExpenseForm
        )

    @patch('expenses.views.create_expense')
    def test_post_creates_simple_expense(self, mock_create_expense):
        response = self.client.post(
            self.url,
            data={
                'title': 'Supermercado',
                'amount': '250.00',
                'date': '2026-09-18',
                'category': 'alimentacao',
            }
        )

        mock_create_expense.assert_called_once_with(
            user=self.user,
            title='Supermercado',
            amount=Decimal('250.00'),
            date=date(2026, 9, 18),
            category='alimentacao'
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('new_expenses')
        )

    @patch('expenses.views.create_installment_expenses')
    def test_post_creates_installment_expense_without_interest(
        self,
        mock_create_installment_expenses
    ):
        response = self.client.post(
            self.url,
            data={
                'title': 'Notebook',
                'amount': '3000.00',
                'date': '2026-09-18',
                'category': 'compras',
                'is_installment': 'on',
                'installments': '10',
            }
        )

        mock_create_installment_expenses.assert_called_once_with(
            user=self.user,
            title='Notebook',
            amount=Decimal('3000.00'),
            date=date(2026, 9, 18),
            category='compras',
            installments=10,
            installment_amount=None
        )

        self.assertRedirects(
            response,
            reverse('new_expenses')
        )

    @patch('expenses.views.create_installment_expenses')
    def test_post_creates_installment_expense_with_interest(
        self,
        mock_create_installment_expenses
    ):
        response = self.client.post(
            self.url,
            data={
                'title': 'Notebook',
                'amount': '3000.00',
                'date': '2026-09-18',
                'category': 'compras',
                'is_installment': 'on',
                'installments': '10',
                'has_interest': 'on',
                'installment_amount': '350.00',
            }
        )

        mock_create_installment_expenses.assert_called_once_with(
            user=self.user,
            title='Notebook',
            amount=Decimal('3000.00'),
            date=date(2026, 9, 18),
            category='compras',
            installments=10,
            installment_amount=Decimal('350.00')
        )

        self.assertRedirects(
            response,
            reverse('new_expenses')
        )

    @patch('expenses.views.create_expense')
    @patch('expenses.views.create_installment_expenses')
    def test_invalid_form_does_not_create_expense(
        self,
        mock_create_installment_expenses,
        mock_create_expense
    ):
        response = self.client.post(
            self.url,
            data={
                'title': 'Notebook',
                'amount': '3000.00',
                'date': '2026-09-18',
                'category': 'compras',
                'is_installment': 'on',
            }
        )

        self.assertEqual(response.status_code, 200)

        mock_create_expense.assert_not_called()
        mock_create_installment_expenses.assert_not_called()

        self.assertFalse(
            response.context['form'].is_valid()
        )

        self.assertIn(
            'installments',
            response.context['form'].errors
        )

    @patch('expenses.views.create_expense')
    def test_success_message_after_creating_expense(
        self,
        mock_create_expense
    ):
        response = self.client.post(
            self.url,
            data={
                'title': 'Supermercado',
                'amount': '250.00',
                'date': '2026-09-18',
                'category': 'alimentacao',
            }
        )

        messages = list(
            get_messages(response.wsgi_request)
        )

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            'Despesa cadastrada com sucesso.'
        )