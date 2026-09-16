from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login', redirect_field_name='next')
def home(request):
    first_name = request.user.first_name.split()[0]
    return render(request, 'home.html', {'first_name': first_name})

