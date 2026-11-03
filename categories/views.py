from django.shortcuts import render


def my_categories(request):
    return render(request, 'my_categories.html')
