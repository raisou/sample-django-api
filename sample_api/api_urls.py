from django.urls import include, path

from clients.urls import urlpatterns as clients_urlpatterns
from tasks.urls import urlpatterns as tasks_urlpatterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # DRF api auth
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # apps
    path("tasks/", include(tasks_urlpatterns)),
    path("clients/", include(clients_urlpatterns)),
]
