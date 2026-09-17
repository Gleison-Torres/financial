from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'amount',
        'date',
        'category',
        'installment',
        'installment_group',
    )

    list_filter = (
        'category',
        'date',
    )

    search_fields = (
        'title',
        'user__username',
        'user__email',
    )

    ordering = (
        '-date',
    )

    @admin.display(description='Parcela')
    def installment(self, obj):
        if obj.installment_number and obj.total_installments:
            return f'{obj.installment_number}/{obj.total_installments}'

        return '-'