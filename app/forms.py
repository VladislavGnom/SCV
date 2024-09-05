from django import forms
from .models import Image, Task, Test
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


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean_type_task(self):
        data = self.cleaned_data.get('type_task')

        if data not in range(1, 16):
            raise ValidationError("Введите верный тип задания")
        
        return data
    

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('title', 'group', 'task_numbers')
        widgets = {
            'task_numbers': forms.CheckboxSelectMultiple(choices=TASK_CHOICES),
        }

