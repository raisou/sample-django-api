import factory
from factory.fuzzy import FuzzyChoice
from django_celery_results.models import TaskResult

from clients.factories import UserFactory

from .models import Task


class TaskResultFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TaskResult


class TaskFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Task

    celery_task = factory.SubFactory(TaskResultFactory)
    task_type = FuzzyChoice([Task.HEAVY, Task.RANDOM, Task.LIGHT])
    user = factory.SubFactory(UserFactory)
