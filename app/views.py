import ast
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from app.forms import ImageForm, TaskForm, TestForm
from app.models import Image, Task, Test, UserTest, CustomUser
from django.http import Http404
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# help function 
# отбирает все группы в которые входит пользователь, который был передан как аргумент
def get_user_groups(user):
    return [group.id for group in user.groups.all()]


def str_to_int(obj):
    return int(obj)


def index(request):
    return render(request, 'app/index.html')


@login_required()
# представление отображения страницы активных к/р
def scv_home(request):
    if request.user.groups.filter(name='Teachers').exists():
        return teachers_home(request)
    else:
        # ast.literal_eval - используется для преобразования строкового представления списка из БД в нормальный список
        
        # один пользователь принадлежит только одной группе(т.к это как классы в школе - каждый ученик определён только в один класс)
        # список (QuerySet) состоящий из тестов пользователя которые предназначены группе(классу) в которую он входит 
        has_user_group = get_user_groups(request.user)[0]
        tests = Test.objects.filter(group=has_user_group)
        
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
                data = UserTest.objects.filter(user=request.user)

                # список из id заданий для отображения сгенерированного варианта
                gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data]
                # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
                for gen_task in gen_tasks_for_type:
                    variant = [Task.objects.filter(pk=pk).order_by('?').first() for pk in gen_task]
                    all_tasks.append(variant)

                merge_title_and_task = list(zip(all_title_tests, all_tasks))


                context = {
                    'form': form, 
                    'img_obj': img_obj, 
                    'images': images,
                    'tasks': all_tasks,
                    'all_title_tests': all_title_tests,
                    'merge_title_and_task': merge_title_and_task,
                    }

                return render(request, 'app/scv_home.html', context=context)
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
                        variant = [Task.objects.filter(type_task=type).order_by('?').first() for type in gen_task]
                        # добавляем в список всех обьектов заданий для отображения в шаблоне
                        all_tasks.append(variant)
                        # сохраняем сгенерированный вариант из заданий по их id в таблицу UserTest
                        UserTest.objects.create(title=f'{name_for_test[indx]}', user=request.user, tasks_id=[v.pk for v in variant])
            else:
                # список из id заданий для отображения сгенерированного варианта
                gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data]
                # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
                for gen_task in gen_tasks_for_type:
                    variant = [Task.objects.get(pk=pk) for pk in gen_task]
                    all_tasks.append(variant)


            merge_title_and_task = list(zip(all_title_tests, all_tasks))
            


            context = {
                'form': form, 
                'images': images,
                'tasks': all_tasks,
                'all_title_tests': all_title_tests,
                'merge_title_and_task': merge_title_and_task,
                }
            
        
        return render(request, 'app/scv_home.html', context=context)
    


@login_required()
def show_result(request):
    if request.method == 'POST':
        # counter right answers
        count = 0
        data = dict(request.POST)

        # получаю первый ключ в словаре, который соответствует названию теста
        title_test = list(data.keys())[0]

        #-------------Fix bag---------#
        # проверка: если пользователь уже завершил свой тест то нельзя его сдать на проверку снова 
        test_obj = UserTest.objects.get(user=request.user, title=title_test)
        # если тест пользователя уже выполнен(на это указывает поле is_complete), то отправляем информационное сообщение и перенаправляем его на главную страницу
        # иначе проверяем тест
        if test_obj.is_complete:
            messages.info(request, "Вы уже загрузили свой тест!")

            return redirect('scv-home')
        else:
            # удаляю пару ключ-значение из словаря, которая соответствует названию теста
            # это нужно для корректной работы следующего цикла!!!
            del data[title_test]

            # списки для дальнеёшего отображения результатов теста
            right_answers = []
            user_answers = []

            for task_id, user_answer in data.items():
                if task_id != 'csrfmiddlewaretoken':  
                    id = task_id.split('-')[2]
                    right_answer = Task.objects.get(pk=id).answer

                    user_answer = user_answer[0].strip()

                    right_answers.append(right_answer)
                    user_answers.append(user_answer)

                    if right_answer == user_answer:
                        count += 1

            # отбираю запись с текущим тестом по его названию
            test_obj = UserTest.objects.get(user=request.user, title=title_test)
            # изменяю поле is_complete на True, т.е на завершенное 
            test_obj.is_complete = True
            # устанавливаю количество правильных ответов
            test_obj.right_answers = count
            # применяю изменения в таблице БД
            test_obj.save()

            task_id = list(map(str_to_int, ast.literal_eval(test_obj.tasks_id)))

            tasks = [Task.objects.get(pk=id) for id in task_id]


            merge_user_and_right_answers = list(zip(user_answers, right_answers))

            new_merge_user_and_right_answers = []  # format List[ List[Tuple(), Object] ], список из списков содержащих кортёж узерного и правильного ответа + обьект класса Task


            for el in merge_user_and_right_answers:
                new_merge_user_and_right_answers.append([el])

            for indx, val in enumerate(tasks):
                new_merge_user_and_right_answers[indx].append(val)


            context = {
                'count_right': count,
                'percent': int(count * 100 / len(tasks)), # вычисляю процент выполнения всей работы, умножаю по математике количество верных ответов на 100 и делю на количество всех ответов => результат в процентах выполнения всей работы
                'tasks': tasks,
                'title': title_test,
                'new_merge_user_and_right_answers': new_merge_user_and_right_answers,
            }
                    
            
            return render(request, 'app/show_result.html', context=context) 
    else:
        return redirect('scv-home')


@login_required()
def refresh_func(request):
    # список (QuerySet) состоящий из тестов пользователя которые предназначены группе(классу) в которую он входит 
    tests = Test.objects.filter(group=get_user_groups(request.user)[0])
    
    # список для списков типов заданий на основе которых будет генерироваться вариант/ы
    gen_tasks_for_type = []

    # имена для тестов
    name_for_test = []

    data = UserTest.objects.filter(user=request.user)
    # перебираем тесты для пользователя и добавляем в gen_tasks_for_type список из типов заданий, которые были заданы через админ панель
    for test in tests:
        # проверка есть ли уже тест в таблице UserTest из таблицы Test
        if not test.title in [test.title for test in data]:
            # используем функцию literal_eval - для безопасного интерпретирования списка из строки в виде которой он хранится в БД
            gen_tasks_for_type.append(list(map(str_to_int, ast.literal_eval(test.task_numbers))))
            name_for_test.append(test.title)


    # генерация варианта, перебираем список состоящий из списков типов заданий 
    for indx, gen_task in enumerate(gen_tasks_for_type):
        # создаём список из обьектов заданий из таблицы Task по их типу - берём рандомную задачу данного типа задачи
        variant = [Task.objects.filter(type_task=type).order_by('?').first() for type in gen_task]
        # сохраняем сгенерированный вариант из заданий по их id в таблицу UserTest
        UserTest.objects.create(title=f'{name_for_test[indx]}', user=request.user, tasks_id=[v.pk for v in variant])

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

    if request.user.groups.filter(name='Teachers').exists():
        return render(request, 'app/profile_teach.html', context=context)
    else:
        return render(request, 'app/profile.html', context=context)

#------------------Teachers Functional----------------------#

@login_required()
def teachers_home(request):
    return render(request, 'app/teachers_home.html', context={'active_block': ''})


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
        'form': form,
        'active_block': 'Добавить задание',
    }

    return render(request, "app/add_task.html", context=context)


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
        'form': form,
        'active_block': 'Добавить к/р',
    }

    return render(request, "app/add_test.html", context=context)


@login_required()
def show_classes(request):
    all_classes = Group.objects.all()

    context = {
        'classes': all_classes,
        'active_block': 'Мои классы',
    }

    return render(request, 'app/show_classes.html', context=context)


@login_required()
def show_tests(request, class_id):
    tests = Test.objects.filter(group_id=class_id)


    context = {
        'tests': tests,
        'class_id': class_id,
        'active_block': 'Мои классы',
    }

    return render(request, 'app/show_tests.html', context=context)


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
        'usertests': usertests,
        'count_tasks': count_tasks, 
        'active_block': 'Мои классы',
    }

    return render(request, 'app/show_result_detail.html', context=context)
