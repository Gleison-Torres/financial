from django.shortcuts import render
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta


def my_categories(request):
    today = timezone.localdate()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    current_month = date(year, month, 1)

    previous_month = current_month - relativedelta(months=1)
    next_month = current_month + relativedelta(months=1)

    context = {
        'current_month': current_month,
        'previous_month': previous_month,
        'next_month': next_month,
    }

    return render(request, 'my_categories.html', context)
