from django.shortcuts import render
from accounts.forms import RegisterForm


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            print('Formulário válido')
            # Criar usuário
            # return redirect(...)

        return render(request, 'register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    return render(request, 'login.html')
