from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from plan.api.serializers import AgentPlanSerializer, PlanSerializer, PlanItemSerializer, PlanGetSerializer, \
    PlanPercentSerializer, PlanItemGetSerializer
from plan.models import Plan, PlanItem, AgentPlan
from order.models import SellOrder


def get_agent_percent(agent_id):
    plans = AgentPlan.objects.filter(agent_id=agent_id, plan__expired=False)
    valid_plans = []
    for plan in plans:
        sell_orders = SellOrder.objects.filter(status="delivered", client__sale_agent=agent_id,
                                               updated_date__gt=plan.plan.created_date)
        plan_items = PlanItem.objects.filter(plan=plan.plan)
        total_percent = 0
        count = 1
        for plan_item in plan_items:
            count += 1
            plan_item_orders = sell_orders.filter(product=plan_item.product)
            total_quantity = 0
            for plan_item_order in plan_item_orders:
                total_quantity += plan_item_order.quantity
            percent = total_quantity / plan_item.quantity
            total_percent += percent
        if count == 1:
            percentage = total_percent / count
        else:
            percentage = total_percent / (count - 1)
        valid_plan = {
            "id": plan.plan.id,
            "name": plan.plan.name,
            "deadline": plan.plan.deadline,
            "percent": percentage
        }
        valid_plans.append(valid_plan)
    return valid_plans


class PlanList(APIView):

    def get_serializer(self, *args, **kwargs):
        return PlanSerializer(*args, **kwargs)

    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanGetSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = PlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanDetail(APIView):

    def get(self, request, agent_id):
        try:
            plans = AgentPlan.objects.filter(agent=agent_id)
            valid_plans = []
            for plan in plans:
                if not plan.plan.expired:
                    valid_plans.append(plan.plan)
            serializer = PlanSerializer(valid_plans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AgentPlan.DoesNotExist:
            return Response({"error": "Bu agentga plan qo'yilmagan"}, status=status.HTTP_404_NOT_FOUND)


class PlanItemCreate(APIView):

    def get_serializer(self, *args, **kwargs):
        return PlanItemSerializer(*args, **kwargs)

    def post(self, request):
        data = request.data
        serializer = PlanItemSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanItemList(APIView):

    def get(self, request, plan_id, agent_id):
        plan_items = PlanItem.objects.filter(plan=plan_id)
        if len(plan_items) == 0:
            raise Http404
        created_date = Plan.objects.get(id=plan_items[0].plan.id).created_date
        sell_orders = SellOrder.objects.filter(status="delivered", updated_date__gt=created_date,
                                                   client__sale_agent_id=agent_id)

        serialized_data = []
        for plan_item in plan_items:
            sell_order_products = sell_orders.filter(product=plan_item.product)
            sale_quantity = 0
            if not len(sell_order_products) == 0:
                for sell_order in sell_order_products:
                    sale_quantity += sell_order.quantity

                percentage = (sale_quantity/plan_item.quantity)*100
                data = {
                    "product": plan_item.product,
                    "quantity": plan_item.quantity,
                    "percentage": percentage
                }
                serializer = PlanItemGetSerializer(data)
                serialized_data.append(serializer.data)
            else:
                data = {
                    "product": plan_item.product,
                    "quantity": plan_item.quantity,
                    "percentage": 0.00
                }
                serializer = PlanItemGetSerializer(data)
                serialized_data.append(serializer.data)

        return Response(serialized_data, status=status.HTTP_200_OK)


class AgentPlanList(APIView):

    def get_serializer(self, *args, **kwargs):
        return AgentPlanSerializer(*args, **kwargs)

    def post(self, request):
        data = request.data
        serializer = AgentPlanSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentPlanDetail(APIView):

    def get(self, request, agent_id):
        valid_plans = get_agent_percent(agent_id=agent_id)
        serializer = PlanPercentSerializer(valid_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


