from django.db import models
from django.conf import settings
from django.db.models import Avg, F
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult as CeleryTask
from celery import states

from .tasks import (heavy_task, light_task, random_task)


class Task(models.Model):
    HEAVY = "Heavy"
    LIGHT = "Light"
    RANDOM = "Random"

    TASK_CHOICES = (
        (HEAVY, "Tâche à exécution longue"),
        (LIGHT, "Tâche à exécution rapide"),
        (RANDOM, "Tâche à exécution à durée variable")
    )

    SYNC = "sync"
    ASYNC = "async"

    EXECUTION_CHOICES = (
        (SYNC, "Synchrone"),
        (ASYNC, "Asynchrone")
    )

    task_type = models.CharField(max_length=30, choices=TASK_CHOICES)
    execution_type = models.CharField(
        max_length=30, choices=TASK_CHOICES, default=ASYNC, editable=False)
    celery_task = models.OneToOneField(CeleryTask, on_delete=models.PROTECT, editable=False)
    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.PROTECT, editable=False)

    @property
    def result(self):
        return self.celery_task.result if self.celery_task.status == states.SUCCESS else None

    def run_task(self, sync=False):
        if self.task_type == self.HEAVY:
            res = heavy_task.delay()
        elif self.task_type == self.LIGHT:
            res = light_task.delay()
        elif self.task_type == self.RANDOM:
            res = random_task.delay()
        else:
            raise Exception('This task_type is not allowed')

        if sync:
            res.wait()

        self.celery_task, created = CeleryTask.objects.get_or_create(task_id=res.id)

    def save(self, *args, **kwargs):
        # get average time execution for task
        avg_diff_qs = Task.objects.filter(
            task_type=self.task_type,
            celery_task__date_done__isnull=False) \
            .aggregate(
                avg_diff=Avg(
                    F('celery_task__date_done') - F('celery_task__date_created')))
        avg_time_diff = avg_diff_qs.get('avg_diff').total_seconds()
        # Run task in async mode if average time is under a treshold
        if settings.TASK_TRESHOLD < avg_time_diff:
            self.run_task()
            self.execution_type = self.ASYNC
        else:
            self.run_task(sync=True)
            self.execution_type = self.SYNC

        super().save(*args, **kwargs)
