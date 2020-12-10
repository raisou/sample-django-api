from rest_framework import (viewsets, mixins, generics)
from rest_framework.permissions import IsAuthenticated
from django_celery_results.models import TaskResult

from .models import Task
from .serializers import (TaskSerializer, TaskCreateSerializer)


class TaskViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    permissions_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return self.serializer_class
