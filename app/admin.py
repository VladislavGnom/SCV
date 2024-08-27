from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django import forms
from .models import Task, Image, Test, UserTest, CustomUser

TASK_CHOICES = {
    '1': '1',
    '2': '2',
    '3': '3',
}


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('full_name', ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('full_name', ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class TestAdminForm(forms.ModelForm):
    class Meta:
        form = Task
        fields = ('title', 'group', 'task_numbers')
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
    list_display = ('title', 'group')


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

# admin.site.register(Task)
admin.site.register(Image)
# admin.site.register(Test)
