import uuid
from decimal import Decimal, ROUND_DOWN

from dateutil.relativedelta import relativedelta
from django.db import transaction

from .models import Expense


def create_expense(user, title, amount, date, category):
    expense = Expense.objects.create(
        user=user,
        title=title,
        amount=amount,
        date=date,
        category=category
    )

    return expense


@transaction.atomic
def create_installment_expenses(user, title, amount, date, category, installments, installment_amount=None):
    if installments < 2 or installments > 48:
        raise ValueError(
            'O número de parcelas deve estar entre 2 e 48.'
        )

    if amount <= 0:
        raise ValueError(
            'O valor da despesa deve ser maior que zero.'
        )

    if installment_amount is not None and installment_amount <= 0:
        raise ValueError(
            'O valor da parcela deve ser maior que zero.'
        )

    installment_group = uuid.uuid4()

    has_custom_installment_amount = installment_amount is not None

    if installment_amount is None:
        installment_amount = (
                amount / Decimal(installments)
        ).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    expenses = []

    for installment_number in range(1, installments + 1):
        installment_date = date + relativedelta(
            months=installment_number - 1
        )

        current_amount = installment_amount

        if (
                not has_custom_installment_amount
                and installment_number == installments
        ):
            current_amount = amount - (
                    installment_amount * Decimal(installments - 1)
            )

        expense = Expense(
            user=user,
            title=title,
            amount=current_amount,
            date=installment_date,
            category=category,
            installment_number=installment_number,
            total_installments=installments,
            installment_group=installment_group
        )

        expenses.append(expense)

    Expense.objects.bulk_create(expenses)

    return expenses


@transaction.atomic
def create_expenses_batch(user, expenses_data):
    created_expenses = []

    for expense_data in expenses_data:
        installments = expense_data.get('installments')

        if installments:
            expenses = create_installment_expenses(
                user=user,
                title=expense_data['title'],
                amount=expense_data['amount'],
                date=expense_data['date'],
                category=expense_data['category'],
                installments=installments,
                installment_amount=expense_data.get('installment_amount')
            )

            created_expenses.extend(expenses)

        else:
            expense = create_expense(
                user=user,
                title=expense_data['title'],
                amount=expense_data['amount'],
                date=expense_data['date'],
                category=expense_data['category']
            )

            created_expenses.append(expense)

    return created_expenses