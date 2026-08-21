from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from .services import send_activation_email, send_password_reset_email
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import Http404
from .token import account_activation_token
from .decorators import anonymous_required
from django.contrib.auth.tokens import default_token_generator


@anonymous_required
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


@anonymous_required
def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            messages.success(request, f'Bem vindo {request.user}')
            return redirect('home')

        return render(request, 'login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')
    raise Http404('Página não encontrada!')


@anonymous_required
def password_reset_request(request):
    if request.method == 'POST':

        email = request.POST.get('email')

        user_model = get_user_model()

        user = user_model.objects.filter(email__iexact=email, is_active=True).first()

        if user is not None:
            send_password_reset_email(request, user)

        messages.info(
            request, 'Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.'
        )

        return redirect('login')
    return render(request, 'password_reset/password_reset_request.html')


def password_reset(request, uidb64, token):
    user_model = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        return render(request, 'password_reset/unsuccessful_password_reset.html', {'validlink': False})

    if not default_token_generator.check_token(user, token):
        return render(request, 'password_reset/unsuccessful_password_reset.html', {'validlink': False})

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, 'Sua senha foi redefinida com sucesso.')
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset/password_reset.html',{'validlink': True, 'form': form})
