from django.contrib.auth.models import User
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    total_calls = serializers.SerializerMethodField()
    heavy_calls = serializers.IntegerField()
    random_calls = serializers.IntegerField()
    light_calls = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            "username",
            "is_superuser",
            "email",
            "date_joined",
            "heavy_calls",
            "random_calls",
            "light_calls",
            "total_calls",
        )

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_calls(self, obj):
        return obj.heavy_calls + obj.random_calls + obj.light_calls
