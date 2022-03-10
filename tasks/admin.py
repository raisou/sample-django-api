from django.contrib import admin
from django_celery_results.admin import TaskResultAdmin

from .models import CeleryTask, Task

admin.site.unregister(CeleryTask)


@admin.register(CeleryTask)
class CeleryTaskAdmin(TaskResultAdmin):
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_type", "execution_type", "celery_task", "status", "user")
    list_per_page = 20
    list_filter = (
        "user__username",
        "task_type",
        "execution_type",
        "celery_task__status",
    )
    search_fields = ("celery_task__task_id", "user__username")

    def status(self, obj):
        return obj.celery_task.status

    def save_model(self, request, obj, form, change):
        if getattr(obj, "user", None) is None:
            obj.user = request.user
        obj.save()
