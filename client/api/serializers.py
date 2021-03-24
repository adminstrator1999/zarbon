from rest_framework import serializers

from client.models import Client, AgentClientReport


class ClientGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"
        depth = 1


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        exclude = ['created_date']


class AgentClientReportGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentClientReport
        fields = "__all__"
        depth = 1


class AgentClientReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentClientReport
        fields = "__all__"
