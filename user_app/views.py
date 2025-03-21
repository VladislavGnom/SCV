import os
import json
import ast
from random import shuffle
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from user_app.forms import ImageForm, TaskForm, TestForm
from user_app.models import Image, Task, Test, UserTest, CustomUser, Question, Answer
from django.http import Http404, HttpResponseNotFound, JsonResponse, HttpResponseServerError
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator

from teacher_app.views import teachers_home
from utils.utils import get_user_groups, str_to_int
from teacher_app.models import TestNewFormat, FilesForTestModel



@login_required
def user_test(request, user_test_id):
    try:
        test = UserTest.objects.get(user=request.user, pk=user_test_id, is_complete=False)
    except ObjectDoesNotExist as error:
        return HttpResponseNotFound("404 Page not Found")
    
    # redirect to test new format process
    if not test.tasks_id:
        return user_test_new_format(request, user_test_id)
    # --------------------------------------

    if request.COOKIES.get('saved_answers'):
        request.session['saved_answers'] = request.COOKIES.get('saved_answers')
    else:
        request.session['saved_answers'] = {}

    # print(json.loads([i[14:] for i in request.META.get('HTTP_COOKIE').split('; ') if i.startswith("saved_answers=")][0]))
    
    gen_tasks_for_type = list(map(str_to_int, ast.literal_eval(test.tasks_id)))
    

    # создание списка variant из обьектов модели Question из уже имеющихся id задач в БД 
    variant = [Question.objects.get(pk=pk) for pk in gen_tasks_for_type]   

    paginator = Paginator(variant, 1)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': test.title, 
        'tasks': page_obj,
        'title_test': test.title,
    }


    return render(request, 'user_app/user_test.html', context=context)


@login_required
def user_test_new_format(request, user_test_id):
    try:
        test = UserTest.objects.get(user=request.user, pk=user_test_id, is_complete=False)
    except ObjectDoesNotExist as error:
        return HttpResponseNotFound("404 Page not Found")
    
    # данные для варианта берутся на основе производной модели TestNewFormat
    # TODO: заменить на выборку по ID вместо названия
    base_data_for_variant = TestNewFormat.objects.get(title=test.title)
    file_with_tasks = base_data_for_variant.file_with_tasks
    number_of_inputs = base_data_for_variant.number_of_inputs
    file_for_done_tasks = base_data_for_variant.files.all()
    
    context = {
        'title': test.title, 
        'file_with_tasks': file_with_tasks,
        'iterator': range(number_of_inputs),
        'file_for_done_tasks': file_for_done_tasks,
        'title_test': test.title,
    }

    return render(request, 'user_app/user_test_new_format.html', context=context)


def index(request):
    return render(request, 'user_app/index.html', context={'title': 'Индексная страница', })


@login_required()
# представление отображения страницы активных к/р
def scv_home(request):
    if request.user.groups.filter(name='Администратор').exists():
        return teachers_home(request)
    else:
        # ast.literal_eval - используется для преобразования строкового представления списка из БД в нормальный список
        
        # один пользователь принадлежит только одной группе(т.к это как классы в школе - каждый ученик определён только в один класс)
        # список (QuerySet) состоящий из тестов пользователя которые предназначены группе(классу) в которую он входит 
        has_user_group = get_user_groups(request.user)[0]
        tests = Test.objects.filter(group=has_user_group, is_complete=False)
        
        # список для списков типов заданий на основе которых будет генерироваться вариант/ы
        gen_tasks_for_type = []
        # все задания - список обьектов отобранных из БД для отображения в шаблоне
        all_tasks = []

        # имена для тестов
        name_for_test = []

        # тесты пользователя (сгенерированные)
        data = UserTest.objects.filter(user=request.user, is_complete=False)

        # список для названия всех тестов пользователя которые не завершены 
        all_title_tests = []

        # перебираем тесты пользователя которые незавершены и формируем список из названий этих тестов
        for test in data:
            all_title_tests.append(test.title) 

        # перебираем тесты для пользователя и добавляем в gen_tasks_for_type список из типов заданий, которые были заданы через админ панель
        for test in tests:
            if not test.title in [test.title for test in UserTest.objects.filter(user=request.user, is_complete=True)]:
                # проверка есть ли уже тест в таблице UserTest из таблицы Test
                if not test.title in [test.title for test in data]:
                    if test.generate_random_order_tasks:
                        # используем функцию literal_eval - для безопасного интерпретирования списка из строки в виде которой он хранится в БД
                        lst_current_tasks = ast.literal_eval(test.task_numbers)
                        shuffle(lst_current_tasks)
                        gen_tasks_for_type.append(list(map(str_to_int, lst_current_tasks)))
                        name_for_test.append(test.title)
                    else:
                        # используем функцию literal_eval - для безопасного интерпретирования списка из строки в виде которой он хранится в БД
                        gen_tasks_for_type.append(list(map(str_to_int, ast.literal_eval(test.task_numbers))))
                        name_for_test.append(test.title)


        # upload file
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                # устанавливаю пользователя который загружает фото - владельцем этого фото
                image.user = request.user
                image.save()

                # получаем экземпляр файла
                img_obj = form.instance
                # получаем список из загруженных фотографий в БД ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
                images = Image.objects.filter(user=request.user)

                # тесты пользователя (сгенерированные)
                data = UserTest.objects.filter(user=request.user, is_complete=False)

                # список из id заданий для отображения сгенерированного варианта
                gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data]
                # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
                for gen_task in gen_tasks_for_type:
                    variant = [Question.objects.get(pk=pk) for pk in gen_task]
                    all_tasks.append(variant)

                usertests = data

                merge_title_and_task = list(zip(all_title_tests, usertests))

                completed_usertests = UserTest.objects.filter(user=request.user, is_complete=True)

                context = {
                    'form': form, 
                    'img_obj': img_obj, 
                    'images': images,
                    'tasks': all_tasks,
                    'all_title_tests': all_title_tests,
                    'merge_title_and_task': merge_title_and_task,
                    'usertests': usertests,
                    'completed_usertests': completed_usertests,
                    }

                return render(request, 'user_app/scv_home.html', context=context)
        else:
            # получаем список из загруженных фотографий в БД ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
            images = Image.objects.filter(user=request.user)

            # форма для загрузки фото
            form = ImageForm()

            # # тесты пользователя (сгенерированные)
            # data = UserTest.objects.filter(user=request.user)

            # усли нет сгенерированных тестов для пользователя, то генерируем их
            if not data:
                # генерация варианта, перебираем список состоящий из списков типов заданий 
                for indx, gen_task in enumerate(gen_tasks_for_type):
                        # создаём список из обьектов заданий из таблицы Task по их типу - берём рандомную задачу данного типа задачи
                        variant = [Question.objects.get(pk=pk) for pk in gen_task]
                        # добавляем в список всех обьектов заданий для отображения в шаблоне
                        all_tasks.append(variant)
                        # сохраняем сгенерированный вариант из заданий по их id в таблицу UserTest
                        UserTest.objects.create(title=f'{name_for_test[indx]}', user=request.user, tasks_id=[v.pk for v in variant], number_of_attempts=tests.get(title=f'{name_for_test[indx]}').number_of_attempts)
            else:
                # список из id заданий для отображения сгенерированного варианта
                gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data if obj.tasks_id]
                # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
                for gen_task in gen_tasks_for_type:
                    variant = [Question.objects.get(pk=pk) for pk in gen_task]
                    all_tasks.append(variant)


            usertests = data


            merge_title_and_task = list(zip(all_title_tests, usertests))

            completed_usertests = UserTest.objects.filter(user=request.user, is_complete=True)
            
            print(merge_title_and_task)

            context = {
                'title': 'Главная страница',
                'form': form, 
                'images': images,
                'tasks': all_tasks,
                'all_title_tests': all_title_tests,
                'merge_title_and_task': merge_title_and_task,
                'usertests': usertests,
                'completed_usertests': completed_usertests,
                }
        
        # print(f'{Answer.objects.get(question_id=290).answer_text=}')
        
        return render(request, 'user_app/scv_home.html', context=context)
    


@login_required()
def show_result(request):
    if request.method == 'POST':
        # counter right answers
        count = 0
        data = dict(request.POST)

        # get data from frontend js
        # data_answers = json.loads(request.session['saved_answers'])
        data_answers = json.loads(request.session['saved_answers'])

        # получаю первый ключ в словаре, который соответствует названию теста
        title_test = list(data.keys())[0]

        #-------------Fix bag---------#
        # проверка: если пользователь уже завершил свой тест то нельзя его сдать на проверку снова 
        test_obj = UserTest.objects.get(user=request.user, title=title_test)
        # если тест пользователя уже выполнен(на это указывает поле is_complete), то отправляем информационное сообщение и перенаправляем его на главную страницу
        # иначе проверяем тест
        if test_obj.is_complete:
            messages.info(request, "Вы исчерпали свои попытки на этот тест, поэтому он закрылся!")

            return redirect('scv-home')
        else:
            # удаляю пару ключ-значение из словаря, которая соответствует названию теста
            # это нужно для корректной работы следующего цикла!!!
            del data[title_test]

            # списки для дальнеёшего отображения результатов теста
            right_answers = []
            user_answers = []

            for task_id, user_answer in data_answers.items():
                if task_id != 'csrfmiddlewaretoken':  
                    id = task_id.split('-')[2]
                    right_answer = Answer.objects.get(question_id=id).answer_text
                    user_answer = user_answer.strip()

                    right_answers.append(right_answer)
                    user_answers.append(user_answer)

                    if right_answer == user_answer:
                        count += 1

            # отбираю запись с текущим тестом по его названию
            test_obj = UserTest.objects.get(user=request.user, title=title_test)


            # увеличиваю число текущих попыток
            test_obj.current_attempts += 1

            # если количество попыток стало числом равному разрешёному количеству пересдач, то тест закрывается
            if test_obj.current_attempts == test_obj.number_of_attempts:
                # изменяю поле is_complete на True, т.е на завершенное 
                test_obj.is_complete = True
                messages.info(request, "Вы исчерпали свои попытки на этот тест, поэтому он закрылся!")
            # если пользователь решил тест правильно то даже если есть попытки, незачем его высвечивать, поэтому он тоже закрывается
            elif count == len(right_answers):
                # изменяю поле is_complete на True, т.е на завершенное 
                test_obj.is_complete = True
                messages.info(request, "Вы сделали тест полностью верно, поэтому он закрылся!")
            # устанавливаю количество правильных ответов
            test_obj.right_answers = count
            # применяю изменения в таблице БД
            test_obj.save()

            task_id = list(map(str_to_int, ast.literal_eval(test_obj.tasks_id)))

            tasks = [Question.objects.get(pk=id) for id in task_id]


            merge_user_and_right_answers = list(zip(user_answers, right_answers))

            new_merge_user_and_right_answers = []  # format List[ List[Tuple(), Object] ], список из списков содержащих кортёж узерного и правильного ответа + обьект класса Task


            for el in merge_user_and_right_answers:
                new_merge_user_and_right_answers.append([el])

            try:
                for indx, val in enumerate(tasks):
                    new_merge_user_and_right_answers[indx].append(val)
            except IndexError as error:
                # увеличиваю число текущих попыток
                test_obj.current_attempts -= 1

                test_obj.save()
                return HttpResponseServerError("Error, please come back and reload page!")

            # путь до бэкапа к/р
            directory_path_to_save_homeworks = f'{settings.BASE_DIR}/static/data_tests/homeworks/'

            # Создание директории, если она не существует
            os.makedirs(directory_path_to_save_homeworks, exist_ok=True)
            
            with open(f'{settings.BASE_DIR}/static/data_tests/homeworks/{title_test.replace('/', '\\')}-{request.user}.txt', mode='w+') as file:
                file.write('Ответ пользователя: Правильный ответ\n')
                for i in range(len(right_answers)):
                    file.write(f'{user_answers[i]}: {right_answers[i]}\n')


            context = {
                'count_right': count,
                'percent': int(count * 100 / len(tasks)), # вычисляю процент выполнения всей работы, умножаю по математике количество верных ответов на 100 и делю на количество всех ответов => результат в процентах выполнения всей работы
                'tasks': tasks,
                'title': title_test,
                'new_merge_user_and_right_answers': new_merge_user_and_right_answers,
            }  

            # если не нужно показывать ответы то тогда просто редиректимся на главную
            group = Group.objects.get(pk=get_user_groups(request.user)[0])
            if not Test.objects.get(group=group, title=title_test).is_show_answers:
                messages.info(request, 'Ваши ответы записаны и уже на проверке, за результатами обращайтесь к учителю')
                return redirect('scv-home')
            
            return render(request, 'user_app/show_result.html', context=context) 
    else:
        return redirect('scv-home')
    
@login_required()
def show_result_test_new_format(request):
    ...


@login_required()
def refresh_func(request):
    # список (QuerySet) состоящий из тестов пользователя которые предназначены группе(классу) в которую он входит 
    tests = Test.objects.filter(group=get_user_groups(request.user)[0], is_complete=False)
    
    # список для списков типов заданий на основе которых будет генерироваться вариант/ы
    gen_tasks_for_type = []

    # имена для тестов
    name_for_test = []

    all_user_tests = UserTest.objects.filter(user=request.user)

    # перебираем тесты для пользователя и добавляем в gen_tasks_for_type список из типов заданий, которые были заданы через админ панель
    for test in tests:
        # проверка есть ли уже тест в таблице UserTest из таблицы Test
        if not test.title in [test.title for test in all_user_tests]:
            if test.generate_random_order_tasks:
                # используем функцию literal_eval - для безопасного интерпретирования списка из строки в виде которой он хранится в БД
                lst_current_tasks = ast.literal_eval(test.task_numbers)
                shuffle(lst_current_tasks)
                gen_tasks_for_type.append(list(map(str_to_int, lst_current_tasks)))
                name_for_test.append(test.title)
            else:
                # используем функцию literal_eval - для безопасного интерпретирования списка из строки в виде которой он хранится в БД
                gen_tasks_for_type.append(list(map(str_to_int, ast.literal_eval(test.task_numbers))))
                name_for_test.append(test.title)


    # ------------------- TEST NEW FORMAT PROCESS -----------------------
    test_new_format = TestNewFormat.objects.filter(group=get_user_groups(request.user)[0], is_complete=False)
    for test in test_new_format:
        # проверка есть ли уже тест в таблице UserTest из таблицы TestNewFormat
        if test.title not in [test.title for test in all_user_tests]:
            UserTest.objects.create(
                title=test.title, 
                user=request.user, 
                number_of_attempts=test.number_of_attempts,
                )


    # генерация варианта, перебираем список состоящий из списков типов заданий 
    for indx, gen_task in enumerate(gen_tasks_for_type):
        # создаём список из обьектов заданий из таблицы Task по их типу - берём рандомную задачу данного типа задачи
        variant = [Question.objects.get(pk=pk) for pk in gen_task]
        
        current_number_of_attempts = tests.get(title=f'{name_for_test[indx]}').number_of_attempts

        # сохраняем сгенерированный вариант из заданий по их id в таблицу UserTest
        UserTest.objects.create(
            title=f'{name_for_test[indx]}',
            user=request.user, tasks_id=[v.pk for v in variant], 
            number_of_attempts=current_number_of_attempts,
            )

    return redirect('scv-home')


@login_required()
def profile(request):
    data = CustomUser.objects.get(username=request.user)
    user_id_group = get_user_groups(request.user)[0]

    name_group = Group.objects.get(id=user_id_group)


    context = {
        'data': data,
        'group': name_group,
        'active_block': '',
    }

    if request.user.groups.filter(name='Администратор').exists():
        return render(request, 'teacher_app/profile_teach.html', context=context)
    else:
        return render(request, 'user_app/profile.html', context=context)

