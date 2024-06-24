from typing import Any, cast

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

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

    def get_queryset(self) -> QuerySet[Task]:
        return Task.objects.filter(user=cast(User, self.request.user))

    def get_serializer_class(self) -> type[BaseSerializer[Any]]:
        """
        We override this function to add exception for create serializer
        """
        if self.action == "create":
            return TaskCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer: BaseSerializer[TaskCreateSerializer]) -> None:
        serializer.save(user=self.request.user)

    @action(detail=True)
    def result(self, request: Request, pk: int | None = None) -> Response:  # noqa: ARG002
        """
        View to display only result of task
        """
        instance = self.get_object()
        return Response({"result": instance.result})

    @action(detail=True)
    def stop(self, request: Request, pk: int | None = None) -> Response:  # noqa: ARG002
        """
        View to stop running task
        """
        instance = self.get_object()
        instance.revoke()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
