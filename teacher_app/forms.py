from django import forms
from user_app.models import Task, Test, SubjectMain, Question
from django.core.exceptions import ValidationError


TASK_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        labels = {
            'title': 'Название задания (Образец: Задание <type_task>)',
            'type_task': 'Тип задания',
            'answer': 'Ответ на задание',
            'photo': 'Изображение задания (Напр. Скрин)',
            'link_to_answer': 'Ссылка на сайт с заданием и ответом (для проверки)',
        }

    def clean_type_task(self):
        data = self.cleaned_data.get('type_task')

        if data not in range(1, 16):
            raise ValidationError("Введите верный тип задания")
        
        return data
    

# class TestForm(forms.ModelForm):

#     class Meta:
#         model = Test
#         fields = ('title', 'group', 'task_numbers', 'number_of_attempts')
#         widgets = {
#             'task_numbers': forms.CheckboxSelectMultiple(choices=TASK_CHOICES),
#         }
#         labels = {
#             'title': 'Название', 
#             'group': 'Класс', 
#             'task_numbers': 'Типы заданий',
#             'number_of_attempts': 'Количество попыток',
#             }

class TestForm(forms.ModelForm):
    # questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Test
        fields = ('title', 'group', 'task_numbers', 'number_of_attempts')

# class TestFormTeacher(forms.ModelForm):

#     class Meta:
#         model = Test
#         fields = ('title', 'group', 'task_numbers', 'number_of_attempts')
#         widgets = {
#             'task_numbers': forms.CheckboxSelectMultiple(choices=TASK_CHOICES),
#         }
#         labels = {
#             'title': 'Название', 
#             'group': 'Класс', 
#             'task_numbers': 'Типы заданий',
#             'number_of_attempts': 'Количество попыток',
#             }

