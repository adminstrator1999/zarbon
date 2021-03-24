from rest_framework import serializers
from plan.models import Plan, PlanItem, AgentPlan


class PlanGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ['name', 'deadline']


class PlanPercentSerializer(serializers.ModelSerializer):
    percent = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'deadline', 'percent']


class PlanItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanItem
        fields = "__all__"


class PlanItemGetSerializer(serializers.ModelSerializer):
    percentage = serializers.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = PlanItem
        fields = ['product', 'quantity', 'percentage']
        depth = 1


class AgentPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentPlan
        fields = "__all__"

