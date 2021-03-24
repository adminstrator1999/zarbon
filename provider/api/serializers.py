from rest_framework import serializers
from provider.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['name', 'address', 'phone_number1', 'responsible_agent']


class ProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ProviderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = "__all__"
