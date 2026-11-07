from expenses.models import Expense


def get_monthly_expenses_by_category_page(
    user,
    year,
    month,
    start_date=None,
    end_date=None
):
    expenses = Expense.objects.filter(user=user)

    if start_date and end_date:
        expenses = expenses.filter(
            date__range=(start_date, end_date)
        )
    else:
        expenses = expenses.filter(
            date__year=year,
            date__month=month
        )

    expenses = expenses.order_by('-date')

    expenses_data = [
        {
            'title': expense.title,
            'category': expense.get_category_display(),
            'date': expense.date.isoformat(),
            'amount': str(expense.amount),
            'is_paid': expense.is_paid,
        }
        for expense in expenses
    ]

    return expenses_data