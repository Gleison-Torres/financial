from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login', redirect_field_name='next')
def home(request):

    name_parts = request.user.first_name.split()

    first_name = (
        name_parts[0]
        if name_parts
        else request.user.username
    )

    return render(request, 'home.html', {'first_name': first_name})