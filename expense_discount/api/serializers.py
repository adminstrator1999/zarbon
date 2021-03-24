from rest_framework import serializers

from expense_discount.models import Discount, Expense
from product.api.serializers import ProductSerializer
from product.models import Product


class DiscountGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Discount
        fields = "__all__"


class DiscountProductGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        exclude = ["product"]


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        exclude = ['created_date']


class AgentDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'name', 'discount', 'deadline']


# id, product_name, quantity, product_unit, provider_name
class AgentDiscountProductSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=20, decimal_places=2)
    provider = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'unit', 'provider']


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        exclude = ['created_date']


class ExpenseGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = "__all__"
        depth = 1
