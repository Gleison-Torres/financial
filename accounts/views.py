from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from .services import send_activation_email
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .token import account_activation_token


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
            # Envia email para ativação da conta.
            send_activation_email(request, user=user)
            messages.info(request, 'Verifique sua caixa de entrada para ativar sua conta.')

        return render(request, 'register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def activate_account(request, uidb64, token):
    user_model = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        return render(request, 'activation/unsuccessful_account_activation.html')

    if not account_activation_token.check_token(user, token):
        return render(request, 'activation/unsuccessful_account_activation.html')

    if not user.is_active:
        user.is_active = True
        user.save(update_fields=['is_active'])

    return render(request, 'activation/successful_account_activation.html')


def login(request):
    return render(request, 'login.html')
