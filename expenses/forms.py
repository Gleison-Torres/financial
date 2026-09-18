from django import forms

from .models import Expense


class ExpenseForm(forms.Form):

    title = forms.CharField(
        max_length=100
    )

    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01
    )

    date = forms.DateField()

    category = forms.ChoiceField(
        choices=Expense.CATEGORY_CHOICES
    )

    is_installment = forms.BooleanField(
        required=False
    )

    installments = forms.IntegerField(
        required=False,
        min_value=2,
        max_value=48
    )

    has_interest = forms.BooleanField(
        required=False
    )

    installment_amount = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0.01
    )

    def clean(self):
        cleaned_data = super().clean()

        is_installment = cleaned_data.get('is_installment')
        installments = cleaned_data.get('installments')
        has_interest = cleaned_data.get('has_interest')
        installment_amount = cleaned_data.get('installment_amount')

        if is_installment and not installments:
            self.add_error(
                'installments',
                'Informe o número de parcelas.'
            )

        if is_installment and has_interest and not installment_amount:
            self.add_error(
                'installment_amount',
                'Informe o valor de cada parcela.'
            )

        return cleaned_data