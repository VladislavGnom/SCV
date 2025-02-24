from django.db import models
from django.contrib.auth.models import Group


class TestNewFormat(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название теста")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    file_with_tasks = models.FileField(upload_to='files_with_tasks', max_length=254, verbose_name="Файл с заданиями")
    number_of_inputs = models.IntegerField(verbose_name="Кол-во полей ввода в тесте")
    file_with_answers = models.FileField(upload_to='files_with_answers', max_length=254, verbose_name="Файл с ответами")
    number_of_attempts = models.IntegerField(blank=True, default=1, verbose_name="Количество попыток")
    count_right_answers = models.IntegerField(blank=True, null=True, verbose_name="Количество верных ответов")
    is_complete = models.BooleanField(default=False, verbose_name="Завершён ли тест")
    input_with_number_task = models.CharField(max_length=255, null=True, blank=True)    # порядок именования инпутов (соотношение их с номерами заданий)
    # generate_random_order_tasks = models.BooleanField(default=False, verbose_name="Генерировать вопросы в перемешку")
    is_show_answers = models.BooleanField(default=False, verbose_name="Показывать ответы")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тест нового образца'
        verbose_name_plural = 'Тесты нового образца'


class FilesForTestModel(models.Model):
    test_new_format = models.ForeignKey(TestNewFormat, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files_for_tasks', max_length=254, verbose_name="Файл для заданий")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test's file for called is {self.test_new_format.title}"
    

    class Meta:
        verbose_name = 'Файл для теста нового образца'
        verbose_name_plural = 'Файлы для теста нового образца'
