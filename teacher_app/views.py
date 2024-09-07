import ast
from django.shortcuts import render, redirect
from teacher_app.forms import TaskForm, TestForm
from user_app.models import Test, UserTest
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#------------------Teachers Functional----------------------#

@login_required()
def teachers_home(request):
    return render(request, 'teacher_app/teachers_home.html', context={'active_block': '', 'title': 'Главная страница'})


@login_required()
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.save()

            messages.success(request, 'Задание успешно добавлено!')

            return redirect('add-task')
    else:
        form = TaskForm()

    context = {
        'title': 'Добавление задания',
        'form': form,
        'active_block': 'Добавить задание',
    }

    return render(request, "teacher_app/add_task.html", context=context)


@login_required()
def add_test(request):
    if request.method == "POST":
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.save()

            messages.success(request, 'Тест успешно создан!')

            return redirect('add-test')
    else:
        form = TestForm()

    context = {
        'title': 'Добавление теста',
        'form': form,
        'active_block': 'Добавить к/р',
    }

    return render(request, "teacher_app/add_test.html", context=context)


@login_required()
def show_classes(request):
    all_classes = Group.objects.all()

    context = {
        'title': 'Классы',
        'classes': all_classes,
        'active_block': 'Мои классы',
    }

    return render(request, 'teacher_app/show_classes.html', context=context)


@login_required()
def show_tests(request, class_id):
    tests = Test.objects.filter(group_id=class_id)


    context = {
        'title': 'Тесты',
        'tests': tests,
        'class_id': class_id,
        'active_block': 'Мои классы',
    }

    return render(request, 'teacher_app/show_tests.html', context=context)


# help func
# возвращает список id пользователей принадлежащих конкретной группе 
def get_users_in_group(group_id):
    try:
        group = Group.objects.get(id=group_id)
        users = group.user_set.all()
        return users
    except ObjectDoesNotExist:
        return None


@login_required()
def show_result_detail(request, class_id, title):
    # id всех пользователей входящих в конкретную группу
    users_id = [user.id for user in get_users_in_group(class_id)]

    # тесты пользователей соответсвующие одному названию теста и разным пользователям входящих в эту группу
    usertests = UserTest.objects.filter(title=title, user_id__in=users_id)


    # отбираю записи из таблицы Test по названию и получаю строковое представление списка номеров заданий и с помощью функции ast.literal_eval() преобразую эту строку в список, а затем узнаю кол-во элеменотов с помощью len() 
    count_tasks = len(ast.literal_eval(Test.objects.get(title=title).task_numbers))



    context = {
        'title': 'Результаты класса',
        'usertests': usertests,
        'count_tasks': count_tasks, 
        'active_block': 'Мои классы',
    }

    return render(request, 'teacher_app/show_result_detail.html', context=context)

