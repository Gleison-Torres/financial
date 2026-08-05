from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from .services import send_activation_email


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                first_name=form.cleaned_data['fullname'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                is_active=False
            )

            send_activation_email(request, user=user)
            messages.info(request, 'Verifique sua caixa de entrada para ativar sua conta.')

        return render(request, 'register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def activate_account(request, uidb64, token):
    pass


def login(request):
    return render(request, 'login.html')
