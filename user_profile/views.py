from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import ChangePasswordForm, EditProfileForms
from django.contrib import messages
from .models import EmailChangeRequest
from .services import send_email_change_confirmation
from .tokens import email_change_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


@login_required(login_url='login', redirect_field_name='next')
def user_profile(request):
    return render(request, 'user_profile.html')


@login_required(login_url='login', redirect_field_name='next')
def edit_profile(request):

    if request.method == 'POST':
        form = EditProfileForms(request.user, request.POST)
        if form.is_valid():
            user = request.user

            user.first_name = form.cleaned_data['fullname']
            user.username = form.cleaned_data['username']

            new_email = form.cleaned_data['email']

            user.save()

            if new_email.lower() != user.email.lower():
                email_change_request, _ = EmailChangeRequest.objects.update_or_create(
                    user=user,
                    defaults={'new_email': new_email}
                )

                send_email_change_confirmation(request, email_change_request)

                messages.info(request, 'Enviamos uma confirmação para o novo e-mail.')
                return redirect('profile')
            else:
                messages.success(request, 'Perfil atualizado com sucesso.')
                return redirect('profile')

    else:

        form = EditProfileForms(
            request.user,
            initial={
                'fullname': request.user.first_name,
                'username': request.user.username,
                'email': request.user.email,
            }
        )

    return render(request, 'edit_profile.html', {'form': form})


def confirm_email_change(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        email_change_request = EmailChangeRequest.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, EmailChangeRequest.DoesNotExist):
        return render(request,'email_change/unsuccessful_email_change.html')

    if not email_change_token.check_token(email_change_request, token):
        return render(request,'email_change/unsuccessful_email_change.html')

    user = email_change_request.user

    user.email = email_change_request.new_email
    user.save()

    email_change_request.delete()

    return render(request, 'email_change/successful_email_change.html')


@login_required(login_url='login', redirect_field_name='next')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()

            update_session_auth_hash(request, request.user)

            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('profile')

    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'change_password.html', {'form': form})
