from rest_framework import serializers
from product.models import Product, Category
from warehouse.models import Warehouse


class ProductGetSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    def get_quantity(self, obj):
        warehouse = Warehouse.objects.get(product=obj)
        return warehouse.quantity


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'product_type']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductDiscountSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=20, decimal_places=2)
    provider = serializers.CharField(max_length=100)
    last_update = serializers.DateTimeField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'product_type', 'quantity', 'provider', 'last_update']
