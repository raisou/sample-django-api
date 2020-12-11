from rest_framework import status
from rest_framework.response import Response
from rest_framework import (viewsets, mixins, generics)
from rest_framework.decorators import action
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

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # make immediate response if fast
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True)
    def result(self, request, pk=None):
        instance = self.get_object()
        return Response({ 'result': instance.result })
