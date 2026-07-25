from django.shortcuts import render


def register(request):
    for data in request.POST:
        print(data)
    return render(request, 'register.html')
