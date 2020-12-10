from django.contrib import admin
from django.contrib.auth.models import Group
from django_celery_results.admin import TaskResultAdmin

from .models import (Task, CeleryTask)


admin.site.unregister(Group)
admin.site.unregister(CeleryTask)


@admin.register(CeleryTask)
class CeleryTaskAdmin(TaskResultAdmin):

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_type', 'celery_task', 'user')
    list_per_page = 20
