import os
import json
import ast
from itertools import chain
from random import shuffle
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.db.models import Q
from user_app.forms import ImageForm, TaskForm, TestForm
from user_app.models import Image, Task, Test, UserTest, CustomUser, Question, Answer
from django.http import Http404, HttpResponseNotFound, JsonResponse, HttpResponseServerError, HttpRequest
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.timezone import now

from teacher_app.views import teachers_home
from utils.utils import get_user_groups, str_to_int
from teacher_app.models import TestNewFormat, FilesForTestModel
from quiz.models import Test as UniversalTest, TestGroupAccess, UserTestResult as UserUniversalTest
from quiz.utils import get_test_group_by_user


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
    base_data_for_variant = TestNewFormat.objects.get(title=test.title)
    file_with_tasks = base_data_for_variant.file_with_tasks
    number_of_inputs = base_data_for_variant.number_of_inputs
    input_with_number_task = ast.literal_eval(base_data_for_variant.input_with_number_task)
    file_for_done_tasks = base_data_for_variant.files.all()

    indx_and_numbers_of_inputs = zip(range(1, number_of_inputs + 1), input_with_number_task)

    context = {
        'title': test.title, 
        'file_with_tasks': file_with_tasks,
        'file_with_tasks_filename': base_data_for_variant.task_filename,
        'file_for_done_tasks': file_for_done_tasks,
        'title_test': test.title,
        'input_with_number_task': indx_and_numbers_of_inputs,
        'number_of_inputs_for_js': list(map(int, input_with_number_task)),
    }

    return render(request, 'user_app/user_test_new_format.html', context=context)


def index(request):
    links = [
        'https://sun9-30.userapi.com/impg/JXbB_lHjyAkiHKHZetzw9F7N6D3ZMQeyHazJbQ/-mwFlPHn0P8.jpg?size=1280x853&quality=95&sign=463fed56f999b612e89742689f68e415&type=album',
        'https://sun9-74.userapi.com/impg/8O1eS5AOtnpRCnf1rpwswCEguGVLr8YdOGjq1A/L7Y_9jJob8Q.jpg?size=1280x853&quality=95&sign=4a5b3430d33ab6007cc840bfd2985df0&type=album',
        'https://sun9-7.userapi.com/impg/bioaZB-lSCF_CLJMPy3ckc94ERzho43lyDfnaw/ijoOKi32a_s.jpg?size=1280x853&quality=95&sign=450f88fead938f2e960c0f434e5c3b87&type=album',
        'https://sun9-64.userapi.com/impg/7kyn97Z9L6VcAqrBaUzX1Jt30hsvwv19edhPYw/2_8KhXpyhBQ.jpg?size=1280x853&quality=95&sign=a06ab877bd174edf33e39f12bfa10c3f&type=album',
        'https://sun9-40.userapi.com/impg/TZhlDE8898MNxvV28TmhP2wlYBUNRWR-T-4XDA/JPl49TZduSs.jpg?size=1280x853&quality=95&sign=1bb558d3b173544be5da174d10a1312e&type=album',
        'https://sun9-56.userapi.com/impg/X_0G_Xto5BVFWUVLNF9B3crhq6op9M0g8qspLw/YlpwkBOFo9E.jpg?size=1280x853&quality=95&sign=0d1f7d9c8e15c08bdd5d07af9c5f092d&type=album',
        'https://sun9-35.userapi.com/impg/-m-387O42RW0y_JeaaKsuvWalcI_bUJ_YaPlnA/ZwQbBH-jnzw.jpg?size=1280x853&quality=95&sign=13b21fe2c7771f907f1ce4a0913d3b36&type=album',
        'https://sun9-80.userapi.com/impg/6ux8BRhr5Lsc5vitkJ7olL25hamnM8Qn88Mlog/6-XHwX5mt2c.jpg?size=1280x1091&quality=95&sign=8204d7b3fcfad89a55948b141dc6838b&type=album',
        'https://sun9-6.userapi.com/impg/5zTP6p4L6gK_cNgB-A_RAU6IQrmtCqPZPXdGVw/O_TsfG7tRqs.jpg?size=1280x853&quality=95&sign=6611285e6980edb9022b528ca8ad9706&type=album',
    ]

    context={
        'title': 'Индексная страница', 
        'links': links,
    }

    return render(request, 'user_app/index.html', context=context)


@login_required()
# представление отображения страницы активных к/р
def scv_home(request):
    current_user = request.user

    if current_user.groups.filter(Q(name='Администратор') | Q(name='Учитель')).exists():
        return teachers_home(request)
    else:
        # ast.literal_eval - используется для преобразования строкового представления списка из БД в нормальный список
        
        # один пользователь принадлежит только одной группе(т.к это как классы в школе - каждый ученик определён только в один класс)
        # список (QuerySet) состоящий из тестов пользователя которые предназначены группе(классу) в которую он входит 
        has_user_group = get_user_groups(current_user)[0]
        tests = Test.objects.filter(group=has_user_group, is_complete=False)
        
        # -------- NEW - ACCESS TO SPECIALIZED TESTS FOR GROUPS -------
        tests_for_group = TestGroupAccess.objects.filter(
            group=get_test_group_by_user(current_user), 
            available_from__lte=now(),
            available_until__gte=now()
        )

        for test_group in tests_for_group:
            try:
                user_universal_test = UserUniversalTest.objects.get(user=current_user, test=test_group.test)
            except ObjectDoesNotExist:
                user_universal_test = UserUniversalTest.objects.create(
                    user=current_user, 
                    test=test_group.test
                    )
                user_universal_test.save()

        # --------------------

        # список для списков типов заданий на основе которых будет генерироваться вариант/ы
        gen_tasks_for_type = []
        # все задания - список обьектов отобранных из БД для отображения в шаблоне
        all_tasks = []

        # имена для тестов
        name_for_test = []

        # тесты пользователя (сгенерированные)
        user_generated_tests = UserTest.objects.filter(user=current_user, is_complete=False)

        # список для названия всех тестов пользователя которые не завершены 
        all_title_tests = []

        # перебираем тесты пользователя которые незавершены и формируем список из названий этих тестов
        for test in user_generated_tests:
            all_title_tests.append(test.title) 

        # перебираем тесты для пользователя и добавляем в gen_tasks_for_type список из типов заданий, которые были заданы через админ панель
        for test in tests:
            if not test.title in [test.title for test in UserTest.objects.filter(user=current_user, is_complete=True)]:
                # проверка есть ли уже тест в таблице UserTest из таблицы Test
                if not test.title in [test.title for test in user_generated_tests]:
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

        # получаем список из загруженных фотографий в БД ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
        images = Image.objects.filter(user=current_user)

        # форма для загрузки фото
        form = ImageForm()

        # усли нет сгенерированных тестов для пользователя, то генерируем их
        if not user_generated_tests:
            # генерация варианта, перебираем список состоящий из списков типов заданий 
            for indx, gen_task in enumerate(gen_tasks_for_type):
                    # создаём список из обьектов заданий из таблицы Task по их типу - берём рандомную задачу данного типа задачи
                    variant = [Question.objects.get(pk=pk) for pk in gen_task]
                    # добавляем в список всех обьектов заданий для отображения в шаблоне
                    all_tasks.append(variant)
                    # сохраняем сгенерированный вариант из заданий по их id в таблицу UserTest
                    UserTest.objects.create(title=f'{name_for_test[indx]}', user=current_user, tasks_id=[v.pk for v in variant], number_of_attempts=tests.get(title=f'{name_for_test[indx]}').number_of_attempts)
        else:
            # список из id заданий для отображения сгенерированного варианта
            gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in user_generated_tests if obj.tasks_id]
            # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
            for gen_task in gen_tasks_for_type:
                variant = [Question.objects.get(pk=pk) for pk in gen_task]
                all_tasks.append(variant)


        usertests = user_generated_tests
        universal_usertests = UserUniversalTest.objects.filter(user=current_user, is_passed=False)
        all_usertests = list(chain(usertests, universal_usertests))

        merge_title_and_task = list(zip(all_title_tests, usertests))

        completed_usertests = UserTest.objects.filter(user=current_user, is_complete=True)
        completed_universal_usertests = UserUniversalTest.objects.filter(user=current_user, is_passed=True)

        all_completed_usertests = list(chain(completed_usertests, completed_universal_usertests))

        context = {
            'title': 'Главная страница',
            'form': form, 
            'images': images,
            'tasks': all_tasks,
            'all_title_tests': all_title_tests,
            'merge_title_and_task': merge_title_and_task,
            'usertests': all_usertests,
            'completed_usertests': all_completed_usertests,
            'universal_tests': UserUniversalTest.objects.filter(is_passed=False)
            }
        
        return render(request, 'user_app/scv_home.html', context=context)
    


@login_required()
def show_result(request):
    if request.method == 'POST':
        # counter right answers
        count = 0
        data = dict(request.POST)

        # get data from frontend js
        if data.get('json-data-answers')    :
            data_answers = json.loads(data['json-data-answers'][0])
        else:
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
            # данные для варианта берутся на основе производной модели TestNewFormat
            try:
                base_data_from_variant = TestNewFormat.objects.get(title=test_obj.title)
            except TestNewFormat.DoesNotExist as error:
                base_data_from_variant = None

            # удаляю пару ключ-значение из словаря, которая соответствует названию теста
            # это нужно для корректной работы следующего цикла!!!
            del data[title_test]

            # списки для дальнеёшего отображения результатов теста
            right_answers = []
            user_answers = []

            for task_id, user_answer in data_answers.items():
                if task_id != 'csrfmiddlewaretoken': 
                    if base_data_from_variant:
                        right_answer = base_data_from_variant.file_with_answers
                        if base_data_from_variant.file_with_answers and base_data_from_variant.file_with_answers.file:
                            line_number = int(task_id)
                            with base_data_from_variant.file_with_answers.file.open("rb") as f:
                                for i, line in enumerate(f, start=1): 
                                    if i == line_number:
                                        right_answer = line.strip().decode('utf-8')
                                        break
                    else:
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

            if not base_data_from_variant:
                task_id = list(map(str_to_int, ast.literal_eval(test_obj.tasks_id)))

                tasks = [Question.objects.get(pk=id) for id in task_id]
                number_of_inputs_for_js = []
            else:
                number_of_inputs_for_js = list(map(int, ast.literal_eval(base_data_from_variant.input_with_number_task)))
                tasks = []


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
                'percent': int(count * 100 / len(right_answers)), # вычисляю процент выполнения всей работы, умножаю по математике количество верных ответов на 100 и делю на количество всех ответов => результат в процентах выполнения всей работы
                'tasks': tasks,
                'title': title_test,
                'new_merge_user_and_right_answers': new_merge_user_and_right_answers,
                'number_of_inputs_for_js': number_of_inputs_for_js,            
            }  

            # если не нужно показывать ответы то тогда просто редиректимся на главную
            group = Group.objects.get(pk=get_user_groups(request.user)[0])
            try:
                if not Test.objects.get(group=group, title=title_test).is_show_answers:
                    messages.info(request, 'Ваши ответы записаны и уже на проверке, за результатами обращайтесь к учителю')
                    return redirect('scv-home')
            except Test.DoesNotExist as error:
                ...
            try:
                if not TestNewFormat.objects.get(group=group, title=title_test).is_show_answers:
                    messages.info(request, 'Ваши ответы записаны и уже на проверке, за результатами обращайтесь к учителю')
                    return redirect('scv-home')
            except TestNewFormat.DoesNotExist as error:
                ...
            
            return render(request, 'user_app/show_result.html', context=context) 
    else:
        return redirect('scv-home')


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
def profile(request: HttpRequest):
    data = CustomUser.objects.get(username=request.user)
    user_id_group = get_user_groups(request.user)[0]

    name_group = Group.objects.get(id=user_id_group)


    context = {
        'title': 'Профиль',
        'data': data,
        'group': name_group,
        'active_block': '',
    }

    if request.user.groups.filter(Q(name='Администратор') | Q(name='Учитель')).exists():
        return render(request, 'teacher_app/profile_teach.html', context=context)
    else:
        return render(request, 'user_app/profile.html', context=context)


@login_required
def show_tests_user_profile(request: HttpRequest):
    user = request.user

    all_tests_of_user = UserTest.objects.filter(user=user)
    count_of_questions_list = []

    for test in UserTest.objects.filter(user=user):
        if test.tasks_id:
            count_of_questions_list.append(len(ast.literal_eval(test.tasks_id)))
        else: 
            # данные для варианта берутся на основе производной модели TestNewFormat
            count_of_questions_list.append(TestNewFormat.objects.get(title=test.title).number_of_inputs)

    data_tests_of_user = zip(all_tests_of_user, count_of_questions_list)

    attempts = UserUniversalTest.objects.filter(user=request.user).select_related('test')   
    correct_completed_questions_by_tests = [attempt.user_answers.filter(is_correct=True).count() for attempt in attempts]
    all_questions_by_tests = [attempt.user_answers.all().count() for attempt in attempts]
    data_universal_tests_of_user = zip(attempts, zip(correct_completed_questions_by_tests, all_questions_by_tests))

    context = {
        'title': 'Все тесты',
        'data_tests_of_user': data_tests_of_user,
        'data_universal_tests_of_user': data_universal_tests_of_user,
    }

    return render(request, 'user_app/tests_user_profile.html', context=context)\
    
def handle_uploaded_file(request):
    current_user = request.user
    has_user_group = get_user_groups(current_user)[0]

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.group = Group.objects.get(pk=has_user_group)
            image.save()

            messages.success(request, message='Успешно загружено!')

            return redirect('scv-home')

