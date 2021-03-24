from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from expense_discount.models import Discount, Expense
from product.models import Product
from expense_discount.api.serializers import DiscountSerializer, DiscountGetSerializer, AgentDiscountSerializer, \
    AgentDiscountProductSerializer, ExpenseSerializer, ExpenseGetSerializer


class DiscountList(APIView):

    def get_serializer(self, *args, **kwargs):
        return DiscountSerializer(*args, **kwargs)

    def get(self, request):
        discounts = Discount.objects.all().order_by("-id")
        serializer = DiscountGetSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        discount_serializer = DiscountSerializer(data=data)
        if discount_serializer.is_valid():
            discount_serializer.save()
            return Response(discount_serializer.data, status=status.HTTP_201_CREATED)
        return Response(discount_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return DiscountSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return Discount.objects.get(pk=pk)
        except Discount.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        discount = self.get_object(pk)
        serializer = DiscountGetSerializer(discount)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk)
        data = request.data
        serializer = DiscountSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discount = self.get_object(pk)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AndroidDiscountList(APIView):

    def get(self, request):
        discounts = Discount.objects.filter(active=True)
        serializer = AgentDiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AndroidDiscountProducts(APIView):

    def get(self, request, discount_id):
        products = Product.objects.filter(discount=discount_id)
        product_list = []
        for product in products:
            data = {"id": product.id,
                    "name": product.name,
                    "unit": product.unit,
                    "quantity": product.warehouse_set.get(product=product).quantity,
                    "provider": product.provider.name,
                    }
            product_list.append(data)
        serializer = AgentDiscountProductSerializer(product_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseList(APIView):

    def get_serializer(self, *args, **kwargs):
        return ExpenseSerializer(*args, **kwargs)

    def get(self, request):
        expenses = Expense.objects.all().order_by("-id")
        serializer = ExpenseGetSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = ExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return ExpenseSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return Expense.objects.get(id=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk=pk)
        serializer = ExpenseSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk=pk)
        serializer = ExpenseSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
