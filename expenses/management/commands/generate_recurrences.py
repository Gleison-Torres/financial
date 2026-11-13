
from django.core.management.base import BaseCommand
from django.utils import timezone

from expenses.services import generate_monthly_recurring_expenses


class Command(BaseCommand):
    help = 'Gera as despesas recorrentes do mês atual.'

    def handle(self, *args, **options):

        today = timezone.localdate()

        created_expenses = generate_monthly_recurring_expenses(
            year=today.year,
            month=today.month
        )

        total = len(created_expenses)

        self.stdout.write(
            self.style.SUCCESS(
                f'{total} despesa(s) recorrente(s) gerada(s).'
            )
        )
