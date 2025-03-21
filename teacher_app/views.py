import os
import ast
from django.shortcuts import render, redirect
from django.http import HttpRequest
from teacher_app.forms import TaskForm, TestForm, AnswerForm
from user_app.models import Test, UserTest, SubjectMain, SubjectParents, SubjectChildren, Question, Answer
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from django.core.paginator import Paginator

from utils.utils import extract_filename_substring, clean_html, get_group_by_name

from .forms import TASK_CHOICES_SUBJECT, TASK_CHOICES_SUBJECT_PARENT, TASK_CHOICES_SUBJECT_CHILD
from .models import TestNewFormat, FilesForTestModel

#------------------Teachers Functional----------------------#

@login_required()
def teachers_home(request):
    return render(request, 'teacher_app/teachers_home.html', context={'active_block': '', 'title': 'Главная страница'})


@login_required
def tests_page(request):
    if request.method == "POST":
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.save()

            messages.success(request, 'Тест успешно создан!')
            request.session['tasks'] = []

            return redirect('show-tests')
    else:
        form = TestForm()

    context = {
        'title': 'Тесты',
        'active_block': 'Добавить к/р',
        'form_test': form,
        'subjects_main': SubjectMain.objects.filter(enabled=1),
    }

    return render(request, "teacher_app/tests_page.html", context=context)


@login_required()
def add_task(request):
    if request.method == "POST":
        print(request.POST)
        form = TaskForm(request.POST, request.FILES)
        form_answer = AnswerForm(request.POST)
        if form.is_valid() and form_answer.is_valid():
            new_task = form.save(commit=False)
            new_answer = form_answer.save(commit=False)

            SUBJECT_MAIN = request.POST.get("SUBJECT_MAIN")
            SUBJECT_PARENT = request.POST.get("SUBJECT_PARENT")
            SUBJECT_CHILD = request.POST.get("SUBJECT_CHILD")

            new_task.subject_id = SubjectMain.objects.get(subject_main_name=SUBJECT_MAIN).pk
            new_task.subject_parent_id = SubjectParents.objects.get(subject_parent_name=SUBJECT_PARENT).pk
            new_task.subject_child_id = SubjectChildren.objects.get(subject_child_name=SUBJECT_CHILD).pk

            new_task.question_text = new_task.image
            new_task.save()
            
            new_answer.question = Question.objects.get(pk=new_task.pk)

            new_answer.save()

            messages.success(request, 'Задание успешно добавлено!')

            return redirect('add-task')
    else:
        form = TaskForm()
        form_answer = AnswerForm()
    # print(TASK_CHOICES_SUBJECT_PARENT)

    context = {
        'title': 'Добавление задания',
        'form': form,
        'form_answer': form_answer,
        'active_block': 'Добавить задание',
        'TASK_CHOICES_SUBJECT': TASK_CHOICES_SUBJECT,
        'TASK_CHOICES_SUBJECT_PARENT': sorted(TASK_CHOICES_SUBJECT_PARENT, key=lambda x: (x[0], x[1])),
        'TASK_CHOICES_SUBJECT_CHILD': sorted(TASK_CHOICES_SUBJECT_CHILD, key=lambda x: (x[0], x[1])),
    }

    return render(request, "teacher_app/add_task.html", context=context)


@login_required()
def add_test(request):
    context = {
        'title': 'Добавление теста',
        'active_block': 'Добавить к/р',
        'subjects_main': SubjectMain.objects.filter(enabled=1),
    }

    return render(request, "teacher_app/add_test.html", context=context)


@login_required
def add_task_subject(request,  subject_main_id):
    subject_questions = Question.objects.filter(subject_id__gt=4, enabled=1)
    paginator = Paginator(subject_questions, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subject_main_id': subject_main_id,
        'subject_main_name': SubjectMain.objects.get(pk=subject_main_id).subject_main_name,
        'subjects_parents': SubjectParents.objects.filter(subject_main_id=subject_main_id, enabled=1),
        'subject_questions': page_obj,
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
        'subjects_children': SubjectChildren.objects.filter(subject_parent_id=subject_parent_id, enabled=1),
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
        # 'questions': Question.objects.filter(Q(subject_child_id=subject_children_id) | Q(subject_id=subject_main_id) | Q(subject_parent_id=subject_parent_id)),
        # 'questions': (Question.objects.filter(subject_child_id=subject_children_id) or (Question.objects.filter(Q(subject_parent_id=subject_parent_id) | Q(subject_id=subject_main_id)))),
        'questions': (Question.objects.filter(subject_child_id=subject_children_id, enabled=1).order_by('-time_create') or (Question.objects.filter(Q(subject_parent_id=subject_parent_id, enabled=1)).order_by('-time_create'))),
    }
    
    return render(request, "teacher_app/add_test.html", context=context)


@login_required
def add_task_question(request, subject_main_id, subject_parent_id, subject_children_id, question_id):
    if request.method == "POST":
        task = request.POST.get('task')
        tasks = request.session.get('tasks', [])

        # используется для проверки что задание добавилось в сессию, для вывода оповещающих сообщений
        flag = False

        # Добавляем новую задачу в список
        if task and task not in tasks:  # Проверка на пустую задачу и уникальность
            flag = True
            tasks.append(task)
            request.session['tasks'] = tasks  # Сохраняем обновленный список в сессии

        if flag:
            messages.success(request, "Задание успешно добавлено в тест!")
        else:
            messages.warning(request, "Задание уже нахожится в тесте!")
    else:
        ...
    question = Question.objects.get(pk=question_id, enabled=1)
    answers_count = Answer.objects.filter(question_id=question_id).aggregate(count=Count("answer_text"))['count']
    
    is_warning_task = False
    print(f'{answers_count}')

    # check if task is warning
    if answers_count > 1:
        is_warning_task = True
    
    filename = extract_filename_substring(question.question_text),
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
        'question': question,
        'filename': filename[0],
        'text_task': clean_html(" ".join([i for i in question.question_text.split() if i != filename[0]])),
    
        'is_warning_task': is_warning_task,
    }
    #request.COOKIES['info'] = 'kkk'
    # request.COOKIES['tasks'].append('11')
    #request.session['tasks'] = [111]
    print([i for i in question.question_text.split()])

    return render(request, "teacher_app/add_test.html", context=context)


# @login_required
# def add_question_to_task_list(request):
#     request.COOKIES['tasks'].append('11')
#     return


@login_required
def add_task_question_safe(request, subject_main_id, question_id):
    if request.method == "POST":
        task = request.POST.get('task')
        tasks = request.session.get('tasks', [])

        # используется для проверки что задание добавилось в сессию, для вывода оповещающих сообщений
        flag = False

        # Добавляем новую задачу в список
        if task and task not in tasks:  # Проверка на пустую задачу и уникальность
            flag = True
            tasks.append(task)
            request.session['tasks'] = tasks  # Сохраняем обновленный список в сессии

        if flag:
            messages.success(request, "Задание успешно добавлено в тест!")
        else:
            messages.warning(request, "Задание уже нахожится в тесте!")
    else:
        ...
    question = Question.objects.get(pk=question_id, enabled=1)
    
    answers_count = Answer.objects.filter(question_id=question_id).aggregate(count=Count("answer_text"))['count']
    
    is_warning_task = False

    # check if task is warning
    if answers_count > 1:
        is_warning_task = True

    context = {
        'title': 'Добавление теста',
        # 'form': form,
        'active_block': 'Добавить к/р',
        'subject_main_id': subject_main_id,
        'question_id': question_id,
        'subject_main_name': SubjectMain.objects.get(pk=subject_main_id).subject_main_name,
        'question': question,
        'filename': question.question_text,
        'text_task': clean_html(" ".join([i for i in question.question_text.split() if i != question.question_text])),
    
        'is_warning_task': is_warning_task,
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
        'tests': [t.title.replace("/", "\\") for t in tests],
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
    usertests = UserTest.objects.filter(title=title.replace('\\', '/'), user_id__in=users_id)


    # отбираю записи из таблицы Test по названию и получаю строковое представление списка номеров заданий и с помощью функции ast.literal_eval() преобразую эту строку в список, а затем узнаю кол-во элеменотов с помощью len() 
    count_tasks = len(ast.literal_eval(Test.objects.get(title=title.replace('\\', '/')).task_numbers))

    from utils.utils import create_excel_table, restyles_excel_file

    filename = f'{title}-{class_id}.xlsx'
    data = {
        "Ученик": [],
        "Название теста": [],
        "ID заданий": [],
        "Кол-во правильных ответов": [],
        "Процент выполнения работы": []
    }

    for usertest in usertests:
        data['Ученик'].append(f"{usertest.user.first_name} {usertest.user.last_name}")
        data['Название теста'].append(f"{usertest.title}")
        data['ID заданий'].append(f"{usertest.tasks_id}")
        data['Кол-во правильных ответов'].append(f"{usertest.right_answers}")
        data['Процент выполнения работы'].append(f"{ (usertest.right_answers * 100) / count_tasks }%")


    # создаём таблицу
    create_excel_table(filename=filename, data=data)
    # применяем стили к таблице
    restyles_excel_file(filename=filename)

    context = {
        'title': 'Результаты класса',
        'usertests': usertests,
        'count_tasks': count_tasks, 
        'active_block': 'Мои классы',
        'filename': filename,
    }

    return render(request, 'teacher_app/show_result_detail.html', context=context)

# NEW UPDATE
# ---------------------------------------
@login_required
def add_test_new_format_view(request: HttpRequest):
    groups = Group.objects.all().exclude(name='Администратор')
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        title_test = data.get('title-test')
        selected_group = data.get('selected-group')
        number_of_attempts = data.get('number-of-attempts')
        file_with_tasks = files.get('file_with_tasks')
        input_with_number_task = data.getlist('input_with_number_task')
        # input_with_answer = data.get('input_with_answer')

        # preparation
        # ---------------------------------------------
        number_of_inputs = len(input_with_number_task)
        # BASE_DIR = settings.BASE_DIR
        # with open(os.path.join(BASE_DIR, f'media/files_with_answers/{title_test}-answers.txt'), 'w') as file: 
        #     for ans in input_with_answer:
        #         file.write(ans + '\n')
            
        # ---------------------------------------------
        # file with answers
        answers_file = request.FILES.get('answers-field')

        # validation 
        # ---------------------------------------------
        if selected_group == 'default':
            messages.error(request, "Вы не заполнили поле c group")
            return redirect('add-test-new-format')
        # ---------------------------------------------

        test = TestNewFormat.objects.create(
            title=title_test,
            group=get_group_by_name(selected_group),
            file_with_tasks=file_with_tasks,
            number_of_inputs=number_of_inputs,
            file_with_answers=answers_file,
            number_of_attempts=number_of_attempts,
            input_with_number_task=input_with_number_task,
        )

        # -------- SAVE FILES FOR COMPLETING TEST -------------
        if request.method == 'POST' and files:
            for file in request.FILES.getlist('file_for_done_tasks'):
                FilesForTestModel.objects.create(test_new_format=test, file=file)
        # -----------------------------------------------------

        messages.success(request, "Тест успешно создан!")
        return redirect('add-test-new-format')
    else:
        ...

    context = {
        'title': 'Тест нового образца - Добавление',
        'groups': groups,
    }
    
    return render(request, 'teacher_app/add_test_new_format.html', context=context)
