from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ['timestamp', 'task_status']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
