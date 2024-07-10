from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest
from django_celery_results.admin import TaskResultAdmin

from .models import CeleryTask, Task

admin.site.unregister(CeleryTask)


@admin.register(CeleryTask)
class CeleryTaskAdmin(TaskResultAdmin):
    def has_add_permission(self, request: HttpRequest, obj: str | None = None) -> bool:  # noqa: ARG002
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

    def status(self, obj: Task) -> str:
        return obj.celery_task.status

    def save_model(
        self,
        request: HttpRequest,
        obj: Any,
        form: Any,  # noqa: ARG002
        change: Any,  # noqa: ARG002
    ) -> None:
        if getattr(obj, "user", None) is None:
            obj.user = request.user
        obj.save()
