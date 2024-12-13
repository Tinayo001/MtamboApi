from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MaintenanceProvider

# Get the correct User model
User = get_user_model()

class MaintenanceProviderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = MaintenanceProvider
        fields = ['id', 'speacialization', 'company_name', 'company_address', 'company_registration_number']

    def create(self, validated_data):
        return MaintenanceProvider.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

