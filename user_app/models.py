from django.db import models
from django.contrib.auth.models import Group, AbstractUser



class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
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
    
class SubjectMain(models.Model):
    subject_main_name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=1)
    
    def __str__(self):
        return self.subject_main_name
    

class SubjectParents(models.Model):
    subject_main = models.ForeignKey(SubjectMain, on_delete=models.CASCADE)
    subject_parent_name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=1)
    timestamps = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.subject_parent_name
    

class SubjectChildren(models.Model):
    subject_parent = models.ForeignKey(SubjectParents, on_delete=models.CASCADE)
    subject_child_name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=1)
    timestamps = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.subject_child_name
    

class Question(models.Model):
    subject = models.ForeignKey(SubjectMain, on_delete=models.CASCADE)
    # subject_parent = models.ForeignKey(SubjectParents, on_delete=models.CASCADE)
    # subject_child = models.ForeignKey(SubjectChildren, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=600)
    question_group = models.IntegerField(default=0)
    question_points = models.IntegerField()
    question_type = models.IntegerField()

    def __str__(self):
        return self.question_text[:10]



class CustomUser(AbstractUser):
    open_password = models.CharField(max_length=255, verbose_name='Пароль')
