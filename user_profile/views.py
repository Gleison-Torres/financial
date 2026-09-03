from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from . forms import ChangePasswordForm
from django.contrib import messages


@login_required(login_url='login', redirect_field_name='next')
def user_profile(request):
    return render(request, 'user_profile.html')


@login_required(login_url='login', redirect_field_name='next')
def edit_profile(request):
    if request.method == 'POST':
        # Implementar atualização de dados.
        form = request.POST
        print(form.get('fullName'), form.get('email'), form.get('username'))
    return render(request, 'edit_profile.html')


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

    return render(request,'change_password.html', {'form': form})


