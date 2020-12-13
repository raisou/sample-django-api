from django.urls import path

from .views import ClientListAPIView


urlpatterns = [
    path('', ClientListAPIView.as_view(), name='clients-list')
]
