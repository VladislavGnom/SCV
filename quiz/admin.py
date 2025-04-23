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
from django.contrib import admin
from django import forms
from .models import Test, Question, Answer, UserTestResult, TestGroupAccess, Group as TestGroup
from .forms import AnswerInlineFormSet


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and self.instance.answers.count() < 2:
            raise forms.ValidationError("Вопрос должен содержать минимум 2 ответа")
        return cleaned_data


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    form = AnswerForm
    formset = AnswerInlineFormSet  # Подключаем наш FormSet
    extra = 0
    min_num = 2


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
    fields = ('text', 'question_type')


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