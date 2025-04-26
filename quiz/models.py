from django.db import models
from django.utils.timezone import now
from datetime import timedelta
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
from django.core.exceptions import ValidationError
from difflib import SequenceMatcher
from .validators import validate_test_type

class Test(models.Model):
    class TestType(models.TextChoices):
        EXAM = 'EX', 'Экзамен'
        QUIZ = 'QZ', 'Быстрый тест'
        PRACTISE = 'PR', 'Тренировка'
        SURVEY = 'SR', 'Опрос'
        PSYCHO = 'PS', 'Психологический тест'

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    test_type = models.CharField(
        'Тип теста',
        max_length=2,
        choices=TestType.choices,
        default=TestType.QUIZ
    )
    time_limit = models.PositiveIntegerField(
        'Лимит времени (в мин)',
        null=True,
        blank=True,
        help_text='Оставьте пустым, если без ограничений'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    groups = models.ManyToManyField(
        'Group',
        through='TestGroupAccess',
        related_name='tests',
        verbose_name='Доступные группы',
        blank=True
    )

    def is_exam(self) -> bool:
        return self.test_type == self.TestType.EXAM
    
    def is_available_for(self, user):
        return self.groups.filter(members=user).exists()

    def clean(self):
        super().clean()
        validate_test_type(self)

    def __str__(self):
        return f"{self.title} ({self.get_test_type_display()})"

    @property
    def is_timed(self) -> bool:
        '''Проверяет ограничен ли тест по времени'''
        return self.time_limit is not None
    
    def __str__(self):
        return self.title


class Question(models.Model):
    class QuestionType(models.TextChoices):
        SINGLE = 'SN', 'Один правильный ответ'
        MULTIPLE = 'ML', 'Несколько правильных ответов'
        TEXT = 'TX', 'Текстовый'
        TEXT_AUTO = 'TXA', 'Текстовый (auto)'
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(
        'Тип вопроса',
        max_length=3,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE
        )
    text = models.TextField('Текст вопроса')
    max_score = models.PositiveIntegerField('Максимальный балл', default=1)
    
    correct_answer = models.TextField('Правильный ответ (для автопроверки)', blank=True, null=True)
    answer_fuzzy_match = models.BooleanField(
        'Нечеткое сравнение ответов',
        default=False,
        help_text='Если включено, система будет учитывать опечатки и синонимы'
    )
    # explanation = models.CharField('Пояснение')

    def __str__(self):
        return self.text




class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class UserTestResult(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='user_results'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    score = models.PositiveIntegerField(default=0)
    is_passed = models.BooleanField(default=False)

    def __str__(self):
        return self.test.title

    class Meta:
        unique_together = [['user', 'test']]


class UserAnswer(models.Model):
    user_test_result = models.ForeignKey(
        UserTestResult,
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    text_answer = models.TextField('Текстовый ответ', blank=True, null=True)
    selected_answers = models.ManyToManyField(Answer, blank=True)
    is_correct = models.BooleanField('Правильный ответ', null=True)
    score = models.PositiveIntegerField('Начисленные баллы', default=0)
    checked_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Проверил'
    )
    checked_at = models.DateTimeField('Время проверки', null=True, blank=True)
    feedback = models.TextField('Комментарий преподавателя', blank=True, null=True)


    class CheckStatusChoices(models.TextChoices):
        NEEDS_REVIEW = 'review', 'Требуется проверка'
        AUTO_CHECKED = 'auto', 'Автоматическая проверка'
        MANUAL_CHECKED = 'manual', 'Проверено вручную'
    

    check_status = models.CharField(
        'Статус проверки',
        max_length=10,
        choices=CheckStatusChoices.choices,
        default=CheckStatusChoices.AUTO_CHECKED
    )
    admin_review_comment = models.TextField('Комментарий преподавателя', blank=True)

    @property
    def similarity(self, obj):
        """Вычисляем процент схожести для текстовых ответов"""
        if obj.text_answer and obj.question.correct_answer:
            ratio = SequenceMatcher(
                None, 
                obj.text_answer.lower(), 
                obj.question.correct_answer.lower()
            ).ratio()
            return f"{ratio:.0%}"
        return "-"


    @property
    def get_correct_answer(self, obj):
        """Показываем правильный ответ из связанного вопроса"""
        return obj.question.correct_answer

    class Meta:
        unique_together = [['user_test_result', 'question']]


class Group(models.Model):
    """Группа пользователей (курсы, классы и т.д.)"""
    name = models.CharField('Название', max_length=100)
    members = models.ManyToManyField(
        User,
        related_name='learning_groups',
        blank=True
    )

    class Meta:
        ordering = ['name']  # Сортировка по умолчанию по имени
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class TestGroupAccess(models.Model):
    """Контроль доступа тестов к группам"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    available_from = models.DateTimeField('Доступен с', null=True, blank=True, auto_now_add=True)
    available_until = models.DateTimeField('Доступен до', null=True, blank=True)
    is_mandatory = models.BooleanField('Обязательный', default=False)

    
    class Meta:
        unique_together = [['test', 'group']]
        verbose_name = 'Доступ теста к группе'
        verbose_name_plural = 'Настройки доступа тестов'

    def save(self, *args, **kwargs):
        if not self.available_until:
            self.available_until = self.available_from + timedelta(days=1)
        super().save(*args, **kwargs)
        