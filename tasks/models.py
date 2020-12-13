from django.db import models
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult as CeleryTask
from celery import states


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
    execution_type = models.CharField(max_length=30, choices=TASK_CHOICES, editable=False)
    celery_task = models.OneToOneField(CeleryTask, on_delete=models.PROTECT, editable=False)
    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.PROTECT, editable=False)

    @property
    def result(self):
        return self.celery_task.result if self.celery_task.status == states.SUCCESS else None

    def run(self):
        from .tasks import (heavy_task, light_task, random_task)

        if self.task_type == self.HEAVY:
            res = heavy_task.delay()
        elif self.task_type == self.LIGHT:
            res = light_task.delay()
        elif self.task_type == self.RANDOM:
            res = random_task.delay()
        else:
            raise Exception('This task_type is not allowed')

        # TODO to improve in real setup
        self.celery_task, created = CeleryTask.objects.get_or_create(task_id=res.id)

    def save(self, *args, **kwargs):
        self.run()
        super().save(*args, **kwargs)
