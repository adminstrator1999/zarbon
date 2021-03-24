from decimal import Decimal
from datetime import timedelta, datetime
from django.utils import timezone

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from salary.api.serializers import SalarySerializer, FlexibleSalarySerializer, FixedSalarySerializer, \
    SalaryGetSerializer
from salary.models import Salary, FixedSalary
from plan.api.views import get_agent_percent
from user.models import User


class FixedSalaryList(APIView):

    def get_serializer(self, *args, **kwargs):
        return FixedSalarySerializer(*args, **kwargs)

    def get(self, request):
        items = FixedSalary.objects.all()
        serializer = FixedSalarySerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FixedSalarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FixedSalaryDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return FixedSalarySerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return FixedSalary.objects.get(id=pk)
        except FixedSalary.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = FixedSalarySerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = FixedSalarySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SalaryNotGivenUser(APIView):
    def get(self, request):
        start_date = (timezone.now() - timedelta(days=28)).replace(tzinfo=None)
        salary_given_users = Salary.objects.filter(created_date__gt=start_date).values_list("user", flat=True)
        salary_not_given_users = []
        users = User.objects.all().values_list("id", flat=True)
        for user_id in users:
            if user_id not in salary_given_users:
                user_data = User.objects.get(id=user_id)
                data = {
                    "first_name": user_data.first_name,
                    "last_name": user_data.last_name,
                    "role": user_data.role
                }
                salary_not_given_users.append(data)
        return Response(salary_not_given_users, status=status.HTTP_200_OK)


class SalaryList(APIView):

    def get_serializer(self, *args, **kwargs):
        return SalarySerializer(*args, **kwargs)

    def get(self, request):
        items = Salary.objects.all()
        serializer = SalaryGetSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = SalarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalaryDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return SalarySerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return Salary.objects.get(id=pk)
        except Salary.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        salary = self.get_object(pk)
        serializer = SalarySerializer(salary)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        salary = self.get_object(pk)
        data = request.data
        serializer = SalarySerializer(salary, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        salary = self.get_object(pk)
        salary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgentFlexibleSalary(APIView):

    def get(self, request, agent_id):
        agent = User.objects.get(id=agent_id)
        valid_plans = get_agent_percent(agent_id=agent_id)
        try:
            flexible_salary = FixedSalary.objects.get(flexible=True, role="agent")
            fixed_salary = FixedSalary.objects.get(role="agent", flexible=False)
        except Salary.DoesNotExist:
            raise Http404
        percentage = 0
        count = 1
        for valid_plan in valid_plans:
            count += 1
            percentage += Decimal(valid_plan.get('percent'))
        if count == 1:
            total_percentage = percentage / count
        else:
            total_percentage = percentage / (count-1)

        agent_flexible_salary = (total_percentage/100)*flexible_salary.salary_quantity
        data = {
            "fixed_salary": fixed_salary.salary_quantity,
            "flexible_salary": agent_flexible_salary,
            "first_name": agent.first_name,
            "last_name": agent.last_name,
            "role": agent.role
        }
        serializer = FlexibleSalarySerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)





