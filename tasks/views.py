from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permissions_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        We override this function to add exception for create serializer
        """
        if self.action == "create":
            return TaskCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True)
    def result(self, request, pk=None):
        """
        View to display only result of task
        """
        instance = self.get_object()
        return Response({"result": instance.result})

    @action(detail=True)
    def stop(self, request, pk=None):
        """
        View to stop running task
        """
        instance = self.get_object()
        instance.revoke()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
