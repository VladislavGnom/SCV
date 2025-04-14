from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError



def login_view(request):   
    #from user_app.models import SubjectMain, SubjectParents, SubjectChildren, Question, Answer
    # for i, d in enumerate(data):
    #     try:
    #         Answer.objects.create(pk=i, question_id=d['question_id'], answer_text=d['answer_text'],)
    #     except IntegrityError as error:
    #         print(error)
    #         continue
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

    return render(request, 'authapp/login.html', context={'form': form, 'title': 'Вход в систему | Учебный проект'})
