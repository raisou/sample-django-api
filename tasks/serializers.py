from rest_framework import serializers
from django_celery_results.models import TaskResult

from .models import Task


class CeleryTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = (
            'task_name', 'task_id', 'status', 'date_created', 'date_done'
        )


class TaskSerializer(serializers.ModelSerializer):
    celery_task = CeleryTaskSerializer()

    class Meta:
        model = Task
        fields = ('id', 'celery_task', 'user_id')


class TaskCreateSerializer(serializers.Serializer):
    task_name = serializers.ChoiceField(Task.TASK_CHOICES)
    param = serializers.CharField()

    def to_representation(self, instance):
        return TaskSerializer(instance).data
