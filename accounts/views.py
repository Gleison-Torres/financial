from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            User.objects.create_user(
                first_name=form.cleaned_data['fullname'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            messages.success(request, 'Cadastrado com sucesso!')
        return redirect('login')

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    return render(request, 'login.html')
