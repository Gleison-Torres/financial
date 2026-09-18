from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ExpenseForm
from .services import (
    create_expense,
    create_installment_expenses,
)


@login_required(login_url='login')
def add_new_expenses(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if data['is_installment']:
                create_installment_expenses(
                    user=request.user,
                    title=data['title'],
                    amount=data['amount'],
                    date=data['date'],
                    category=data['category'],
                    installments=data['installments'],
                    installment_amount=(
                        data['installment_amount']
                        if data['has_interest']
                        else None
                    )
                )

            else:
                create_expense(
                    user=request.user,
                    title=data['title'],
                    amount=data['amount'],
                    date=data['date'],
                    category=data['category']
                )

            messages.success(request, 'Despesa cadastrada com sucesso.')

            return redirect('new_expenses')

    else:
        form = ExpenseForm()

    return render(request, 'new_expenses.html', {'form': form})