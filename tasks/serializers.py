from django_celery_results.models import TaskResult as CeleryTask
from rest_framework import serializers

from .models import Task


class CeleryTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeleryTask
        fields = (
            "task_name",
            "task_id",
            "status",
            "date_created",
            "date_done",
            "result",
        )


class TaskSerializer(serializers.ModelSerializer):
    celery_task = CeleryTaskSerializer()

    class Meta:
        model = Task
        fields = ("id", "execution_type", "celery_task", "user")


class TaskCreateSerializer(serializers.Serializer):
    task_type = serializers.ChoiceField(Task.TASK_CHOICES)

    def create(self, validated_data: dict) -> Task:
        """
        Create and return a new Task instance, given the validated data.
        """
        return Task.objects.create(**validated_data)

    def to_representation(self, instance: Task) -> dict:
        return TaskSerializer(instance).data
