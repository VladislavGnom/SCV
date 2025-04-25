# import nested_admin

# from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericTabularInline

# from quiz.models import Question, AnswerOption, UniversalTest, Subject, QuestionType


# class QuestionInline(nested_admin.NestedStackedInline):
#     model = Question
#     extra = 1
#     fieldsets = (
#         (None, {
#             'fields': ('type', 'text', 'explanation', 'points', 'order')
#         }),
#     )
#     inlines = ['AnswerOptionInline']

# class AnswerOptionInline(nested_admin.NestedTabularInline):
#     model = AnswerOption
#     extra = 2
#     fields = ('text', 'is_correct', 'feedback')

# @admin.register(UniversalTest)
# class UniversalTestAdmin(nested_admin.NestedModelAdmin):
#     list_display = ('title', 'subject', 'creator', 'is_published')
#     list_filter = ('subject', 'is_published')
#     search_fields = ('title', 'description')
#     inlines = [QuestionInline]
#     # filter_horizontal = ('allowed_groups',)

# @admin.register(Question)
# class QuestionAdmin(nested_admin.NestedModelAdmin):
#     list_display = ('text', 'test', 'type', 'points')
#     inlines = [AnswerOptionInline]
#     list_filter = ('test__subject', 'type')

# @admin.register(Subject)
# class SubjectAdmin(nested_admin.NestedModelAdmin):
#     list_display = ('name', 'slug')

# admin.site.register(QuestionType)

import nested_admin
from difflib import SequenceMatcher
from django.contrib import admin
from django.utils import timezone
from django import forms
from .models import Test, Question, Answer, UserTestResult, UserAnswer, TestGroupAccess, Group as TestGroup
from .forms import AnswerInlineFormSet, QuestionForm, AnswerForm


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    form = AnswerForm
    formset = AnswerInlineFormSet  # Подключаем наш FormSet
    # extra = 0
    # min_num = 2
    classes = ['answer-inline']  # Добавляем класс для селектора


    class Media:
        js = ('admin/js/question_type_handler.js',)
        css = {
            'all': ('admin/css/question_types.css',)
        }

    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.question_type == Question.QuestionType.TEXT:
            self.min_num = 0
            self.extra = 0
        return super().get_formset(request, obj, **kwargs)

    # def get_min_num(self, request, obj=None, **kwargs):
    #     if obj and obj.question_type == Question.QuestionType.TEXT:
    #         return 0
    #     return super().get_min_num(request, obj, **kwargs)

    # def get_extra(self, request, obj=None, **kwargs):
    #     if obj and obj.question_type == Question.QuestionType.TEXT:
    #         return 0
    #     return super().get_extra(request, obj, **kwargs)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        # Дополнительная валидация вопроса при необходимости
        return cleaned_data


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 0
    min_num = 1
    form = QuestionForm
    inlines = [AnswerInline]
    fields = ('text', 'question_type', 'max_score', 'correct_answer', 'answer_fuzzy_match')


class TestGroupAccessInline(nested_admin.NestedTabularInline):
    model = TestGroupAccess
    extra = 1
    fields = ('group', 'available_from', 'available_until', 'is_mandatory')
    autocomplete_fields = ['group'] 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            kwargs["queryset"] = TestGroup.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'test_type', 'is_timed', 'created_at')
    list_filter = ('test_type', )
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'test_type')
        }),
        ('Настройки', {
            'fields': ('time_limit',),
            'description': 'Параметры, специфичные для типа теста'
        })
    )
    inlines = [QuestionInline, TestGroupAccessInline]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.test_type in (Test.TestType.PRACTISE, Test.TestType.SURVEY, Test.TestType.PSYCHO):
            fieldsets[1][1]['fields'] = ()
        return fieldsets


class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'is_passed')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_test_result', 'question', 'check_status', 'score', 'is_correct')
    list_filter = ('check_status', 'question__test')
    list_editable = ('score', 'is_correct')
    actions = ['approve_answer', 'reject_answer']
    readonly_fields = ('user_test_result', 'question', 'text_answer')
    
    fieldsets = (
        (None, {
            'fields': ('user_test_result', 'question', 'check_status')
        }),
        ('Ответ', {
            # 'fields': ('text_answer', 'correct_answer', 'similarity')
            'fields': ('text_answer',)
        }),
        ('Проверка', {
            'fields': ('is_correct', 'score', 'admin_review_comment')
        }),
    )
    
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
    similarity.short_description = 'Схожесть с эталоном'

    def get_correct_answer(self, obj):
        """Показываем правильный ответ из связанного вопроса"""
        return obj.question.correct_answer
    get_correct_answer.short_description = 'Правильный ответ'
    
    def approve_answer(self, request, queryset):
        queryset.update(
            is_correct=True,
            check_status=UserAnswer.CheckStatusChoices.MANUAL_CHECKED,
            checked_by=request.user,
            checked_at=timezone.now()
        )
    
    def reject_answer(self, request, queryset):
        queryset.update(
            is_correct=False,
            check_status=UserAnswer.CheckStatusChoices.MANUAL_CHECKED,
            checked_by=request.user,
            checked_at=timezone.now()
        )


@admin.register(TestGroup)
class TestGroupAdmin(admin.ModelAdmin):
    filter_vertical = ('members',)
    search_fields = ('name',)  # Поля для поиска в autocomplete
    list_display = ('name', )
    list_filter = ('name', )

    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Количество участников'


@admin.register(TestGroupAccess)
class TestGroupAccessAdmin(admin.ModelAdmin):
    list_display = ('test', 'group', 'is_mandatory')
    list_filter = ('group', 'is_mandatory')

admin.site.register(Test, TestAdmin)
admin.site.register(UserTestResult, UserTestResultAdmin)