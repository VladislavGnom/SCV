import ast
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from app.forms import ImageForm
from app.models import Image, Task, Test, UserTest
from django.http import Http404


# help function
def get_user_groups(user):
    return [group.id for group in user.groups.all()]


# def get_count_groups(user):
#     return user.groups.count()


def str_to_int(obj):
    return int(obj)


def index(request):
    print(request.group)
    return render(request, 'app/index.html')


def scv_home(request):
    # ast.literal_eval - используется для преобразования строкового представления списка из БД в нормальный список
    # пока что ограничиваемся отображением одной к/р. Это нужно допилить:)
    # этот код позволяет регать пользователя в разных группах и он всегда будет получать ДЗ со всех этих групп. Функционалпод вопросом
    # tests = []
    # for i in range(get_count_groups(request.user)):
    #     test = Test.objects.filter(group=get_user_groups(request.user)[i])
    #     tests.append(test)

    tests = Test.objects.filter(group=get_user_groups(request.user)[0])
    
    gen_tasks_for_type = []
    all_tasks = []

    for test in tests:
        gen_tasks_for_type.append(list(map(str_to_int, ast.literal_eval(test.task_numbers))))

    # list(map(str_to_int, ast.literal_eval(tests[0].task_numbers)))


    # upload file
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            img_obj = form.instance
            images = get_list_or_404(Image)

            for gen_task in gen_tasks_for_type:
                for type in gen_task:
                    all_tasks.append(Task.objects.filter(type_task=type).order_by('?').first())


            context = {
                'form': form, 
                'img_obj': img_obj, 
                'images': images,
                'tasks': all_tasks,
                }

            return render(request, 'app/scv_home.html', context=context)
    else:
        images = Image.objects.all()
        form = ImageForm()

        data = UserTest.objects.filter(user=request.user)

        if not data:
            count = 1
            for gen_task in gen_tasks_for_type:
                    variant = [Task.objects.filter(type_task=type).order_by('?').first() for type in gen_task]
                    all_tasks.append(variant)
                    UserTest.objects.create(title=f'Variant {count}', user=request.user, tasks_id=[v.pk for v in variant])
                    count += 1
        else:
            gen_tasks_for_type = [ast.literal_eval(obj.tasks_id) for obj in data]
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


# # check handler tasks
# def tasks_handler(request):
#     if request.method == 'POST':
#         # counter right answers
#         count = 0
#         data = dict(request.POST)

#         for task_id, user_answer in data.items():
#             if task_id != 'csrfmiddlewaretoken':  
#                 id = task_id.split('-')[2]
#                 right_answer = Task.objects.get(pk=id).answer

#                 user_answer = user_answer[0].strip()

#                 if right_answer == user_answer:
#                     count += 1
#     else:
#         return redirect('scv-home')

        
#     return redirect('show-result')
    


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

