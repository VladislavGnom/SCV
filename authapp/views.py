from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login



def login_view(request):    
    form = LoginForm()
    data = request.GET
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('scv-home')
        else:
            messages.info(request, "Такой пользователь не найден, попробуйте ещё раз!")

    return render(request, 'authapp/login.html', context={'form': form})
