from django.contrib import admin

from .models import TestNewFormat, FilesForTestModel

@admin.register(TestNewFormat)
class TestNewFormatAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'is_complete')

@admin.register(FilesForTestModel)
class FilesForTestModelAdmin(admin.ModelAdmin):
    model = FilesForTestModel
    extra = 1