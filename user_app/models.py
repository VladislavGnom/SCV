from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, AbstractUser



class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Изображение пользователя'
        verbose_name_plural = 'Изображения пользователей'


class Task(models.Model):
    title = models.CharField(max_length=255, default='Задание ')
    type_task = models.IntegerField()
    answer = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images_for_tasks', blank=True)
    link_to_answer = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
    

# хранит активные и завершённые тесты/работы
class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название теста")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    task_numbers = models.CharField(max_length=255, verbose_name="ID заданий")
    is_complete = models.BooleanField(default=False, verbose_name="Завершён ли тест")
    count_right_answers = models.IntegerField(blank=True, null=True, verbose_name="Количество верных ответов")
    number_of_attempts = models.IntegerField(blank=True, default=1, verbose_name="Количество попыток")
    generate_random_order_tasks = models.BooleanField(default=False, verbose_name="Генерировать вопросы в перемешку")
    is_show_answers = models.BooleanField(default=False, verbose_name="Показывать ответы")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class UserTest(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    tasks_id = models.CharField(max_length=255, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    right_answers = models.IntegerField(blank=True, default=0)
    number_of_attempts = models.IntegerField(blank=True, default=1)
    current_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тесты пользователя'
        verbose_name_plural = 'Тесты пользователей'
    

class SubjectMain(models.Model):
    subject_main_name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=1)
    
    def __str__(self):
        return self.subject_main_name
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
    

class SubjectParents(models.Model):
    subject_main = models.ForeignKey(SubjectMain, on_delete=models.CASCADE)
    subject_parent_name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=1)
    timestamps = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.subject_parent_name
    
    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
    

class SubjectChildren(models.Model):
    subject_parent = models.ForeignKey(SubjectParents, on_delete=models.CASCADE)
    subject_child_name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=1)
    timestamps = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.subject_child_name
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
    

class Question(models.Model):
    # subject = models.ForeignKey(SubjectMain, on_delete=models.CASCADE, default=0)
    subject_id = models.IntegerField()
    # subject_parent = models.ForeignKey(SubjectParents, on_delete=models.CASCADE, default=0)
    subject_parent_id = models.IntegerField()
    # subject_child = models.ForeignKey(SubjectChildren, on_delete=models.CASCADE, default=0)
    subject_child_id = models.IntegerField()
    question_text = models.TextField(max_length=600)
    enabled = models.BooleanField(default=1)
    image = models.ImageField(upload_to='imgs')
    time_create = models.DateTimeField(auto_now_add=timezone.now(), blank=True, null=True)
    # question_group = models.IntegerField(default=0)
    # question_points = models.IntegerField()
    # question_type = models.IntegerField()

    def __str__(self):
        return self.question_text[:20]
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class CustomUser(AbstractUser):
    open_password = models.CharField(max_length=255, verbose_name='Пароль')
