from django.shortcuts import render


def add_new_expenses(request):
    return render(request, 'new_expenses.html')
