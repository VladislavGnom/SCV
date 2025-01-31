from django.contrib import admin

from .models import TestNewFormat

@admin.register(TestNewFormat)
class TestNewFormatAdmin(admin.ModelAdmin):
    ...
