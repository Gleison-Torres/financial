from django.test import TestCase

from expenses.forms import ExpenseForm


class ExpenseFormTest(TestCase):

    def test_valid_simple_expense(self):
        form = ExpenseForm(data={
            'title': 'Supermercado',
            'amount': '250.00',
            'date': '2026-09-18',
            'category': 'alimentacao',
        })

        self.assertTrue(form.is_valid())

    def test_valid_installment_expense_without_interest(self):
        form = ExpenseForm(data={
            'title': 'Notebook',
            'amount': '3000.00',
            'date': '2026-09-18',
            'category': 'compras',
            'is_installment': True,
            'installments': 10,
        })

        self.assertTrue(form.is_valid())

    def test_valid_installment_expense_with_interest(self):
        form = ExpenseForm(data={
            'title': 'Notebook',
            'amount': '3000.00',
            'date': '2026-09-18',
            'category': 'compras',
            'is_installment': True,
            'installments': 10,
            'has_interest': True,
            'installment_amount': '350.00',
        })

        self.assertTrue(form.is_valid())

    def test_installment_expense_requires_installments(self):
        form = ExpenseForm(data={
            'title': 'Notebook',
            'amount': '3000.00',
            'date': '2026-09-18',
            'category': 'compras',
            'is_installment': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Informe o número de parcelas.', form.errors['installments'])

    def test_installment_with_interest_requires_installment_amount(self):
        form = ExpenseForm(data={
            'title': 'Notebook',
            'amount': '3000.00',
            'date': '2026-09-18',
            'category': 'compras',
            'is_installment': True,
            'installments': 10,
            'has_interest': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Informe o valor de cada parcela.', form.errors['installment_amount'])

    def test_amount_must_be_greater_than_zero(self):
        form = ExpenseForm(data={
            'title': 'Supermercado',
            'amount': '0',
            'date': '2026-09-18',
            'category': 'alimentacao',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_installments_cannot_be_less_than_two(self):
        form = ExpenseForm(data={
            'title': 'Notebook',
            'amount': '3000.00',
            'date': '2026-09-18',
            'category': 'compras',
            'is_installment': True,
            'installments': 1,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('installments', form.errors)

    def test_installments_cannot_be_greater_than_48(self):
        form = ExpenseForm(data={
            'title': 'Notebook',
            'amount': '3000.00',
            'date': '2026-09-18',
            'category': 'compras',
            'is_installment': True,
            'installments': 49,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('installments', form.errors)

    def test_invalid_category(self):
        form = ExpenseForm(data={
            'title': 'Supermercado',
            'amount': '250.00',
            'date': '2026-09-18',
            'category': 'categoria_inexistente',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)