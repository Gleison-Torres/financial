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

    def __str__(self):
        return self.title