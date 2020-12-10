from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_type', 'celery_task', 'user')
    list_per_page = 20


admin.site.unregister(Group)
