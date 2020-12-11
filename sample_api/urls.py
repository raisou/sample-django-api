from django.conf import settings
from django.contrib import admin
from django.urls import (path, include)
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

from . import api_urls


urlpatterns = [
    path('docs/', RedirectView.as_view(url="/docs/swagger/"), name='docs'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),
    path('api/', include(api_urls), name="api")
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
