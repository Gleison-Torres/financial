from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('moradia', 'Moradia'),
        ('lazer', 'Lazer'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('compras', 'Compras'),
        ('outros', 'Outros'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    title = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date = models.DateField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    is_paid = models.BooleanField(default=False)

    installment_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    total_installments = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    installment_group = models.UUIDField(
        null=True,
        blank=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    recurring_expense = models.ForeignKey(
        'RecurringExpense',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='occurrences'
    )

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recurring_expense', 'date'],
                name='unique_recurring_expense_date'
            )
        ]


class RecurringExpense(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recurring_expenses'
    )

    title = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=20,
        choices=Expense.CATEGORY_CHOICES
    )

    day_of_month = models.PositiveSmallIntegerField()

    start_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

