from django.db.models import Count, Q
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from tasks.models import Task

from .serializers import ClientSerializer


class ClientListAPIView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ClientSerializer

    def get_queryset(self):
        return User.objects.annotate(
            heavy_calls=Count("tasks", filter=Q(tasks__task_type=Task.HEAVY)),
            random_calls=Count("tasks", filter=Q(tasks__task_type=Task.RANDOM)),
            light_calls=Count("tasks", filter=Q(tasks__task_type=Task.LIGHT)),
        )
