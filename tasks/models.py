from typing import Any

from celery import states
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, F
from django_celery_results.models import TaskResult as CeleryTask

from sample_api.celery_app import app

from .exceptions import IncorrectTaskTypeError
from .tasks import heavy_task, light_task, random_task


class Task(models.Model):
    HEAVY = "Heavy"
    LIGHT = "Light"
    RANDOM = "Random"

    TASK_CHOICES = (
        (HEAVY, "Tâche à exécution longue"),
        (LIGHT, "Tâche à exécution rapide"),
        (RANDOM, "Tâche à exécution à durée variable"),
    )

    SYNC = "sync"
    ASYNC = "async"

    EXECUTION_CHOICES = ((SYNC, "Synchrone"), (ASYNC, "Asynchrone"))

    task_type = models.CharField(max_length=30, choices=TASK_CHOICES)
    execution_type = models.CharField(
        max_length=30, choices=EXECUTION_CHOICES, default=ASYNC, editable=False
    )
    celery_task = models.OneToOneField(
        CeleryTask, on_delete=models.PROTECT, editable=False
    )
    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.PROTECT, editable=False
    )

    def __str__(self) -> str:
        return f"{self.task_type} - {self.execution_type} - {self.celery_task}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        We override save method to introduce our task autorun
        Be carefull if you move this, it need to be available from API and Admin
        """
        # get average time execution for task
        avg_diff = (
            Task.objects.filter(
                task_type=self.task_type, celery_task__date_done__isnull=False
            )
            .aggregate(
                avg_diff=Avg(
                    F("celery_task__date_done") - F("celery_task__date_created")
                )
            )
            .get("avg_diff")
        )
        avg_time_diff = avg_diff.total_seconds() if avg_diff else 0
        # Run task in async mode if average time is under a treshold
        # We check value 0 foor the case with empty data
        if avg_time_diff == 0 or avg_time_diff > settings.TASK_TRESHOLD:
            self.run_task()
            self.execution_type = self.ASYNC
        else:
            self.run_task(sync=True)
            self.execution_type = self.SYNC

        super().save(*args, **kwargs)

    @property
    def result(self) -> str | None:
        return (
            self.celery_task.result
            if self.celery_task.status == states.SUCCESS
            else None
        )

    def revoke(self) -> None:
        app.AsyncResult(self.celery_task.task_id).revoke(terminate=True)

    def run_task(self, *, sync: bool = False) -> None:
        if self.task_type == self.HEAVY:
            res = heavy_task.delay()
        elif self.task_type == self.LIGHT:
            res = light_task.delay()
        elif self.task_type == self.RANDOM:
            res = random_task.delay()
        else:
            raise IncorrectTaskTypeError("This task_type is not allowed")

        if sync:
            res.wait()

        self.celery_task, _created = CeleryTask.objects.get_or_create(task_id=res.id)
