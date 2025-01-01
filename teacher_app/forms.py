from django import forms
from user_app.models import Task, Test, SubjectMain, SubjectChildren, SubjectParents, Question, Answer
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


TASK_CHOICES_SUBJECT = [(i.pk, i) for i in SubjectMain.objects.exclude(subject_main_name="Несуществующий")]
TASK_CHOICES_SUBJECT_PARENT = [(i.subject_main.subject_main_name, i.subject_parent_name) for i in SubjectParents.objects.exclude(subject_parent_name="Несуществующий")]
TASK_CHOICES_SUBJECT_CHILD = [(i.subject_parent.subject_parent_name, i.subject_child_name) for i in SubjectChildren.objects.exclude(subject_child_name="Несуществующий")]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Question
        # fields = ('image', 'subject_id', 'subject_parent_id', 'subject_child_id')
        fields = ('image', )
        labels = {
            'image': 'Изображение с заданием',
            'subject_id': 'Предмет',
            'subject_parent_id': 'Направление',
            'subject_child_id': 'Тема',
        }
        # widgets = {
        #     'subject_id': forms.RadioSelect(choices=TASK_CHOICES_SUBJECT),
        #     'subject_parent_id': forms.RadioSelect(choices=TASK_CHOICES_SUBJECT_PARENT),
        #     'subject_child_id': forms.RadioSelect(choices=TASK_CHOICES_SUBJECT_CHILD),
        # }

    # def clean_type_task(self):
    #     data = self.cleaned_data.get('type_task')

    #     if data not in range(1, 16):
    #         raise ValidationError("Введите верный тип задания")
        
    #     return data
    

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("answer_text", )
        labels = {
            'answer_text': 'Ответ',
        }


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
        fields = ('title', 'group', 'task_numbers', 'number_of_attempts', 'generate_random_order_tasks', 'is_show_answers')

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

