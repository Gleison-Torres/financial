from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required

from .services import get_monthly_expenses_by_category_page


@login_required(login_url='login')
def my_categories(request):
    today = timezone.localdate()

    year = today.year
    month = today.month

    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        current_month = date(year, month, 1)

    except (ValueError, TypeError):
        current_month = date(today.year, today.month, 1)

    previous_month = current_month - relativedelta(months=1)
    next_month = current_month + relativedelta(months=1)

    # Verifica se o usuário selecionou um período personalizado
    start_date = parse_date(request.GET.get('start', ''))
    end_date = parse_date(request.GET.get('end', ''))

    custom_period = bool(start_date and end_date)

    # Busca as despesas do período ou do mês
    expenses = get_monthly_expenses_by_category_page(
        user=request.user,
        year=current_month.year,
        month=current_month.month,
        start_date=start_date if custom_period else None,
        end_date=end_date if custom_period else None
    )

    context = {
        'current_month': current_month,
        'previous_month': previous_month,
        'next_month': next_month,
        'expenses_json': expenses,
        'custom_period': custom_period,
        'start_date': start_date,
        'end_date': end_date,
        'filter_name': request.GET.get('q', ''),
        'filter_category': request.GET.get('category', ''),
    }

    return render(request, 'my_categories.html', context)