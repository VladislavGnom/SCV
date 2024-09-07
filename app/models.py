from django.db import models
from django.contrib.auth.models import Group, AbstractUser



class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    title = models.CharField(max_length=255, default='Задание ')
    type_task = models.IntegerField()
    answer = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images_for_tasks', blank=True)
    link_to_answer = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return str(self.title)
    

# хранит активные и завершённые тесты/работы
class Test(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    task_numbers = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    count_right_answers = models.IntegerField(blank=True, null=True)
    number_of_attempts = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.title


class UserTest(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    tasks_id = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    right_answers = models.IntegerField(blank=True, default=0)
    number_of_attempts = models.IntegerField(blank=True, default=1)
    current_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
