from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense
from .forms import ExpenseForm
from .services import (
    create_expense,
    create_installment_expenses,
    get_installment_summary,
    delete_expense,
    update_expense,
    update_payment_status
)

from datetime import date

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum

from django.views.decorators.http import require_POST


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

    pending_expenses = expenses.filter(is_paid=False)

    month_total = pending_expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    month_count = pending_expenses.count()

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


@login_required(login_url='login')
@require_POST
def delete_expenses(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    delete_expense(expense)

    messages.success(request, 'Despesa deletada com sucesso!')

    return redirect('my_expenses')


@login_required(login_url='login')
def edit_expenses(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            update_expense(
                expense=expense,
                title=data['title'],
                amount=data['amount'],
                date=data['date'],
                category=data['category'],
                is_installment=data['is_installment'],
                installments=data['installments'],
                installment_amount=(
                    data['installment_amount']
                    if data['has_interest']
                    else None
                )
            )

            messages.success(
                request,
                'Despesa atualizada com sucesso!'
            )

            return redirect('my_expenses')

    else:
        if expense.installment_group is not None:
            installment_group = Expense.objects.filter(
                user=request.user,
                installment_group=expense.installment_group
            )

            total_amount = installment_group.aggregate(
                total=Sum('amount')
            )['total'] or 0

            first_installment = installment_group.order_by(
                'installment_number'
            ).first()

            form = ExpenseForm(
                initial={
                    'title': expense.title,
                    'amount': total_amount,
                    'date': first_installment.date,
                    'category': expense.category,
                    'is_installment': True,
                    'installments': expense.total_installments,
                }
            )

        else:
            form = ExpenseForm(
                initial={
                    'title': expense.title,
                    'amount': expense.amount,
                    'date': expense.date,
                    'category': expense.category,
                    'is_installment': False,
                }
            )

    return render(request, 'edit_expenses.html', {'form': form, 'expense': expense})


@login_required(login_url='login')
@require_POST
def change_payment_status(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    update_payment_status(
        expense=expense,
        is_paid=not expense.is_paid
    )

    messages.success(request, 'Status de pagamento atualizado com sucesso!')

    return redirect('my_expenses')