from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login', redirect_field_name='next')
def user_profile(request):
    return render(request, 'user_profile.html')