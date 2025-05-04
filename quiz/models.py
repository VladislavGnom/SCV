from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError
from .validators import validate_test_type

User = get_user_model()


class Test(models.Model):
    """Тест - главная единица этого приложения"""


    class TestType(models.TextChoices):
        EXAM = 'EX', 'Экзамен'
        QUIZ = 'QZ', 'Быстрый тест'
        PRACTISE = 'PR', 'Тренировка'
        SURVEY = 'SR', 'Опрос'
        PSYCHO = 'PS', 'Психологический тест'

    
    class VisibilityChoices(models.TextChoices):
        HIDDEN = 'hidden', 'Не показывать'
        ALL = 'all', 'Всем пользователям'

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    test_type = models.CharField(
        'Тип теста',
        max_length=2,
        choices=TestType.choices,
        default=TestType.QUIZ
    )
    results_visibility = models.CharField(
        'Показ результатов',
        max_length=20, 
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.ALL
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
    

    class Meta:
        verbose_name = "Тест"  
        verbose_name_plural = "Тесты" 


class Question(models.Model):
    """Вопрос к тесту"""


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
    explanation = models.CharField('Пояснение к заданию', blank=True, null=True, max_length=100)

    def __str__(self):
        return self.text


    class Meta:
        verbose_name = "Вопрос"  
        verbose_name_plural = "Вопросы"  


class Answer(models.Model):
    """Ответ на вопрос"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

    class Meta:
        verbose_name = "Ответ" 
        verbose_name_plural = "Ответы"  


class UserTestResult(models.Model):
    """Результат пользователя по тесту"""
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='test_results',
        verbose_name='Пользователь'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='user_results',
        verbose_name='Тест'
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Начат в')
    completed_at = models.DateTimeField(null=True, verbose_name='Завершён в')
    score = models.PositiveIntegerField(default=0, verbose_name='Количество баллов')
    max_score = models.FloatField(verbose_name='Максимальный балл', default=1)
    is_passed = models.BooleanField(default=False, verbose_name='Статус сдачи теста')

    def percentage(self):
        return round((self.score / self.max_score) * 100)
    
    def __str__(self):
        return self.test.title


    class Meta:
        unique_together = [['user', 'test']]
        verbose_name = "Результат пользователя по тесту" 
        verbose_name_plural = "Результат пользователя по тестам" 
        ordering = ['-completed_at']


class UserAnswer(models.Model):
    """Ответ пользователя к вопросу из теста"""


    class CheckStatusChoices(models.TextChoices):
        NEEDS_REVIEW = 'review', 'Требуется проверка'
        AUTO_CHECKED = 'auto', 'Автоматическая проверка'
        MANUAL_CHECKED = 'manual', 'Проверено вручную'

    user_test_result = models.ForeignKey(
        UserTestResult,
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name='Вопрос'
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
    check_status = models.CharField(
        'Статус проверки',
        max_length=10,
        choices=CheckStatusChoices.choices,
        default=CheckStatusChoices.AUTO_CHECKED
    )
    admin_review_comment = models.TextField('Комментарий преподавателя', blank=True)

    def __str__(self):
        return f'ID-{self.pk}'
        

    class Meta:
        unique_together = [['user_test_result', 'question']]
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"


class Group(models.Model):
    """Группа пользователей (курсы, классы и т.д.)"""
    name = models.CharField('Название', max_length=100)
    members = models.ManyToManyField(
        User,
        related_name='learning_groups',
        blank=True
    )

    def __str__(self):
        return self.name
    

    class Meta:
        ordering = ['name'] 
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class TestGroupAccess(models.Model):
    """Контроль доступа тестов к группам"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    available_from = models.DateTimeField('Доступен с', null=True, blank=True, auto_now_add=True)
    available_until = models.DateTimeField('Доступен до', null=True, blank=True)
    is_mandatory = models.BooleanField('Обязательный', default=False)

    def save(self, *args, **kwargs):
        if not self.available_until and self.available_from:
            self.available_until = self.available_from + timedelta(days=1)
        else:
            self.available_until = now() + timedelta(days=1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.test.title} - {self.group.name}'
    

    class Meta:
        unique_together = [['test', 'group']]
        verbose_name = 'Доступ теста к группе'
        verbose_name_plural = 'Настройки доступа тестов'


class TestStatistics(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    average_score = models.FloatField()
    completion_rate = models.FloatField()
    average_time_spent = models.DurationField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Статистика тестов"
        