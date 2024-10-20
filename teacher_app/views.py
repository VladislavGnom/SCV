import ast
from django.shortcuts import render, redirect
from teacher_app.forms import TaskForm, TestForm
from user_app.models import Test, UserTest, SubjectMain, SubjectParents, SubjectChildren, Question
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
    # if request.method == "POST":
    #     form = TestForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         new_task = form.save(commit=False)
    #         new_task.save()

    #         messages.success(request, 'Тест успешно создан!')

    #         return redirect('add-test')
    # else:
    #     form = TestForm()

    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subjects_main': SubjectMain.objects.all(),
    }

    return render(request, "teacher_app/add_test.html", context=context)


@login_required
def add_task_subject(request,  subject_main_id):
    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subject_main_id': subject_main_id,
        'subject_main_name': SubjectMain.objects.get(pk=subject_main_id).subject_main_name,
        'subjects_parents': SubjectParents.objects.filter(subject_main_id=subject_main_id),
    }

    return render(request, "teacher_app/add_test.html", context=context)

@login_required
def add_task_subject_parents(request, subject_main_id, subject_parent_id):
    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subject_main_id': subject_main_id,
        'subject_parent_id': subject_parent_id,
        'subject_main_name': SubjectMain.objects.get(pk=subject_main_id).subject_main_name,
        'subject_parent_name': SubjectParents.objects.get(pk=subject_parent_id).subject_parent_name,
        'subjects_children': SubjectChildren.objects.filter(subject_parent_id=subject_parent_id),
    }

    return render(request, "teacher_app/add_test.html", context=context)


@login_required
def add_task_subject_children(request, subject_main_id, subject_parent_id, subject_children_id):
    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subject_main_id': subject_main_id,
        'subject_parent_id': subject_parent_id,
        'subject_child_id': subject_children_id,
        'subject_main_name': SubjectMain.objects.get(pk=subject_main_id).subject_main_name,
        'subject_parent_name': SubjectParents.objects.get(pk=subject_parent_id).subject_parent_name,
        'subject_children_name': SubjectChildren.objects.get(pk=subject_children_id).subject_child_name,
        'questions': Question.objects.filter(subject_id=subject_main_id),
    }

    return render(request, "teacher_app/add_test.html", context=context)


@login_required
def add_task_question(request, subject_main_id, subject_parent_id, subject_children_id, question_id):
    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subject_main_id': subject_main_id,
        'subject_parent_id': subject_parent_id,
        'question_id': question_id,
        'subject_main_name': SubjectMain.objects.get(pk=subject_main_id).subject_main_name,
        'subject_parent_name': SubjectParents.objects.get(pk=subject_parent_id).subject_parent_name,
        'subject_children_name': SubjectChildren.objects.get(pk=subject_children_id).subject_child_name,
        'question': Question.objects.get(pk=question_id),
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

