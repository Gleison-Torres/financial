from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Expense
from .forms import ExpenseForm
from .services import (
    create_expense,
    create_installment_expenses,
    get_installment_summary,
)

from datetime import date

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum


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

            return redirect('my_expenses')

    else:
        form = ExpenseForm()

    return render(request, 'new_expenses.html', {'form': form})


@login_required(login_url='login')
def my_expenses(request):
    today = timezone.localdate()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    current_month = date(year, month, 1)

    previous_month = current_month - relativedelta(months=1)
    next_month = current_month + relativedelta(months=1)

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=current_month.year,
        date__month=current_month.month
    ).order_by('-date')

    month_total = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    month_count = expenses.count()

    installment_expenses = expenses.filter(
        installment_number__isnull=False
    )

    installment_summaries = [
        get_installment_summary(expense)
        for expense in installment_expenses
    ]

    context = {
        'expenses': expenses,
        'current_month': current_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'month_total': month_total,
        'month_count': month_count,
        'installment_summaries': installment_summaries,
    }

    return render(request, 'my_expenses.html', context)

