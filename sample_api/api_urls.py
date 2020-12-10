from django.urls import (path, include)
from rest_framework import routers

from tasks.urls import tasks_urlpatterns


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # DRF api auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # apps
    path('tasks/', include(tasks_urlpatterns))
]
