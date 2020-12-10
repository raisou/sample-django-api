from django.db import models
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult as CeleryTask


class Task(models.Model):
    HEAVY = "Heavy"
    LIGHT = "Light"
    RANDOM = "Random"

    TASK_CHOICES = (
        (HEAVY, "Tâche à exécution longue"),
        (LIGHT, "Tâche à exécution rapide"),
        (RANDOM, "Tâche à exécution à durée variable")
    )

    task_type = models.CharField(max_length=30, choices=TASK_CHOICES)
    celery_task = models.OneToOneField(CeleryTask, on_delete=models.PROTECT, editable=False)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.PROTECT, editable=False)

    def __str__(self):
        return "{}-{}".format(self.task_type, self.time_start)

    @property
    def status(self):
        from sample_api.celery import app
        return app.AsyncResult(self.celery_task.task_id).state

    def run(self):
        from .tasks import (heavy_task, light_task, random_task)

        if self.name == self.HEAVY:
            heavy_task.delay()
        elif self.name == self.LIGHT:
            light_task.delay()
        elif self.name == self.RANDOM:
            random_task.delay()
