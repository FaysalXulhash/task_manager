from django.contrib import admin
from .models import Task, Photo
# Register your models here.

@admin.register(Task)
class taskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']

@admin.register(Photo)
class photoAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'image']