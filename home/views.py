from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from expenses.models import Expense
from expenses.services import get_monthly_financial_summary


@login_required(login_url='login', redirect_field_name='next')
def home(request):

    # Obtém o primeiro nome do usuário
    name_parts = request.user.first_name.split()

    first_name = (
        name_parts[0]
        if name_parts
        else request.user.username
    )

    # Obtém a data atual
    today = timezone.localdate()

    # Busca o resumo financeiro do mês atual
    financial_summary = get_monthly_financial_summary(
        user=request.user,
        year=today.year,
        month=today.month
    )

    # Busca as 4 despesas mais recentes do mês
    recent_expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    ).order_by('-date', '-id')[:4]

    # Dados enviados para o template
    context = {
        'first_name': first_name,
        'recent_expenses': recent_expenses,
        **financial_summary,
    }

    return render(request, 'home.html', context)