from rest_framework import serializers

from provider.models import Provider
from client.models import Client
from warehouse.models import Warehouse
from report.models import SaleAgentReport


class DirectorWarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        exclude = ["profit"]
        depth = 2


class ProviderDebtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ['id', 'name', 'responsible_agent', 'phone_number1']


class ClientDebtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'name', 'responsible_agent', 'phone_number1', "sale_agent", "address"]
        depth = 1


class AgentClientDebtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'name', 'responsible_agent', 'phone_number1', 'address']


class SaleAgentReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleAgentReport
        fields = "__all__"


class SaleAgentReportGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleAgentReport
        fields = "__all__"
        depth = 1