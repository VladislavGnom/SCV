from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# class Subject(models.Model):
#     """Учебные предметы (география, математика и т.д.)"""
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)

#     def __str__(self) -> str:
#         return self.name

# class UniversalTest(models.Model):
#     """Базовая модель теста"""
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     time_limit = models.PositiveIntegerField(help_text="В минутах (0 - без ограничения)", default=0)
#     is_published = models.BooleanField(default=False)

# class QuestionType(models.Model):
#     """Типы вопросов (можно расширять)"""
#     name = models.CharField(max_length=50)  # Ключ (например, 'multiple_choice')
#     verbose_name = models.CharField(max_length=100)  # Человекочитаемое название
#     template = models.CharField(max_length=100)  # Шаблон для рендеринга
#     has_answers = models.BooleanField(default=True)  # Есть варианты ответов?

#     def __str__(self):
#         return self.verbose_name

# class Question(models.Model):
#     """Вопрос теста"""
#     test = models.ForeignKey(UniversalTest, on_delete=models.CASCADE, related_name='questions')
#     type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
#     text = models.TextField()
#     explanation = models.TextField(blank=True)  # Пояснение после ответа
#     order = models.PositiveIntegerField(default=0)
#     points = models.PositiveIntegerField(default=1)

# class AnswerOption(models.Model):
#     """Варианты ответов"""
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
#     text = models.TextField()
#     is_correct = models.BooleanField(default=False)
#     feedback = models.TextField(blank=True)  # Пояснение для конкретного варианта

# class TestAttempt(models.Model):
#     """Попытка прохождения теста"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     test = models.ForeignKey(UniversalTest, on_delete=models.CASCADE)
#     started_at = models.DateTimeField(auto_now_add=True)
#     completed_at = models.DateTimeField(null=True)
#     results = models.JSONField(default=dict)  # Гибкое хранение результатов

from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=200)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)