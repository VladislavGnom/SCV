from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django import forms
from .models import Task, Image, Test, UserTest, CustomUser, SubjectChildren, SubjectMain, SubjectParents, Question, Answer

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


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Поля, которые дополнительно отображаются в админ панели
    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('open_password',)}), 
    )

    add_fieldsets = (
           (None, {
               'fields': ('username', 'first_name', 'last_name', 'password1', 'password2', 'open_password'),  # добавьте ваше поле здесь
           }),
       )


    list_display = ('first_name', 'last_name', 'get_username_display', 'open_password')
    list_display_links = ('first_name', 'last_name')

    def get_username_display(self, obj):
        return obj.username
    
    get_username_display.short_description = 'Логин'

admin.site.register(CustomUser, CustomUserAdmin)


class TestAdminForm(forms.ModelForm):
    class Meta:
        form = Task
        fields = ('title', 'group', 'is_complete', 'task_numbers', 'number_of_attempts')
        widgets = {
            'task_numbers': forms.CheckboxSelectMultiple(choices=TASK_CHOICES),
        }
        
    def clean_title(self):
        if self.cleaned_data['title'] == "No way!":
            raise forms.ValidationError("Invalid Title")
        
        return self.cleaned_data['title']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm
    list_display = ('title', 'group', 'is_complete')


@admin.register(Task)
class TaskAdminForm(admin.ModelAdmin):
    list_display = ('pk', 'title', 'type_task', 'view_tasks_link',)
    list_display_links = ('title', 'pk')
    
    def view_tasks_link(self, obj):
        from django.utils.html import format_html
        name = obj.link_to_answer
        url = obj.link_to_answer
        return format_html('<a href="{}">{}</a>', url, name)
    view_tasks_link.short_description = "Links"
    

@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'right_answers', 'is_complete')


@admin.register(SubjectMain)
class SubjectMainAdmin(admin.ModelAdmin):
    list_display = ('subject_main_name', 'enabled')

@admin.register(SubjectParents)
class SubjectParentsAdmin(admin.ModelAdmin):
    list_display = ('subject_main', 'enabled')

@admin.register(SubjectChildren)
class SubjectChildrenAdmin(admin.ModelAdmin):
    list_display = ('subject_parent', 'enabled')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'enabled')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text')

# admin.site.register(Task)
admin.site.register(Image)
# admin.site.register(Test)
