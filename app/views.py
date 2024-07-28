import ast
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from app.forms import ImageForm
from app.models import Image, Task, Test, UserTest
from django.http import Http404


# help function 
# отбирает все группы в которые входит пользователь, который был передан как аргумент
def get_user_groups(user):
    return [group.id for group in user.groups.all()]


def str_to_int(obj):
    return int(obj)


def index(request):
    print(request.group)
    return render(request, 'app/index.html')



# представление отображения страницы активных к/р
def scv_home(request):
    # ast.literal_eval - используется для преобразования строкового представления списка из БД в нормальный список

    # один пользователь принадлежит только одной группе(т.к это как классы в школе - каждый ученик определён только в один класс)
    # список (QuerySet) состоящий из тестов пользователя которые предназначены группе(классу) в которую он входит 
    tests = Test.objects.filter(group=get_user_groups(request.user)[0])
    
    # список для списков типов заданий на основе которых будет генерироваться вариант/ы
    gen_tasks_for_type = []
    # все задания - список обьектов отобранных из БД для отображения в шаблоне
    all_tasks = []

    # перебираем тесты для пользователя и добавляем в gen_tasks_for_type список из типов заданий, которые были заданы через админ панель
    for test in tests:
        # используем функцию literal_eval - для безопасного интерпретирования списка из строки в виде которой он хранится в БД
        gen_tasks_for_type.append(list(map(str_to_int, ast.literal_eval(test.task_numbers))))


    # upload file
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            # устанавливаю пользователя который загружает фото - владельцем этого фото
            form.user = request.user
            form.save()

            # получаем экземпляр файла
            img_obj = form.instance
            # получаем список из загруженных фотографий в БД ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
            images = get_list_or_404(Image, user=request.user)

            # тесты пользователя (сгенерированные)
            data = UserTest.objects.filter(user=request.user)

            # список из id заданий для отображения сгенерированного варианта
            gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data]
            # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
            for gen_task in gen_tasks_for_type:
                variant = [Task.objects.filter(pk=pk).order_by('?').first() for pk in gen_task]
                all_tasks.append(variant)


            context = {
                'form': form, 
                'img_obj': img_obj, 
                'images': images,
                'tasks': all_tasks,
                }

            return render(request, 'app/scv_home.html', context=context)
    else:
        # получаем список из загруженных фотографий в БД ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
        images = get_list_or_404(Image, user=request.user)

        # форма для загрузки фото
        form = ImageForm()

        # тесты пользователя (сгенерированные)
        data = UserTest.objects.filter(user=request.user)

        # усли нет сгенерированных тестов для пользователя, то генерируем их
        if not data:
            # счётчик (используется для названия теста)
            count = 1
            # генерация варианта, перебираем список состоящий из списков типов заданий 
            for gen_task in gen_tasks_for_type:
                    # создаём список из обьектов заданий из таблицы Task по их типу - берём рандомную задачу данного типа задачи
                    variant = [Task.objects.filter(type_task=type).order_by('?').first() for type in gen_task]
                    # добавляем в список всех обьектов заданий для отображения в шаблоне
                    all_tasks.append(variant)
                    # сохраняем сгенерированный вариант из заданий по их id в таблицу UserTest
                    UserTest.objects.create(title=f'Variant {count}', user=request.user, tasks_id=[v.pk for v in variant])
                    count += 1
        else:
            # список из id заданий для отображения сгенерированного варианта
            gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data]
            # создание списка all_tasks из обьектов модели Task из уже имеющихся id задач в БД 
            for gen_task in gen_tasks_for_type:
                variant = [Task.objects.filter(pk=pk).order_by('?').first() for pk in gen_task]
                all_tasks.append(variant)



        context = {
            'form': form, 
            'images': images,
            'tasks': all_tasks,
            'gen_is_true': True,
            }
        
    
    return render(request, 'app/scv_home.html', context=context)
    


def show_result(request):
    if request.method == 'POST':
        # counter right answers
        count = 0
        data = dict(request.POST)

        for task_id, user_answer in data.items():
            if task_id != 'csrfmiddlewaretoken':  
                id = task_id.split('-')[2]
                right_answer = Task.objects.get(pk=id).answer

                user_answer = user_answer[0].strip()

                if right_answer == user_answer:
                    count += 1

        context = {
            'count': count,

        }
                
        
        return render(request, 'app/show_result.html', context=context) 
    else:
        return redirect('scv-home')

