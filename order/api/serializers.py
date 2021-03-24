from django.http import Http404
from rest_framework import serializers

from order.models import BuyOrder, SellOrder, BuyOrderPayment, SellOrderPayment, FailedProviderProduct, \
    FailedClientProduct
from client.api.serializers import ClientSerializer


class BuyOrderGetSerializer(serializers.ModelSerializer):
    """Creating serializer to get items"""
    class Meta:
        model = BuyOrder
        fields = "__all__"
        depth = 2


class BuyOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyOrder
        exclude = ['updated_date', 'created_date', 'debt']


class BuyOrderPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyOrderPayment
        exclude = ['created_date']


class BuyOrderPaymentGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyOrderPayment
        fields = "__all__"
        depth = 3


class SellOrderGetSerializer(serializers.ModelSerializer):
    """Creating serializer class to get the items"""
    class Meta:
        model = SellOrder
        fields = "__all__"
        depth = 2


class SellOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellOrder
        exclude = ['created_date', 'updated_date', 'debt']


class ClientSellOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellOrder
        exclude = ["client"]
        depth = 1


class SellOrderPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellOrderPayment
        exclude = ['created_date']


class SellOrderPaymentGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellOrderPayment
        fields = "__all__"
        depth = 3


class FailedProviderProductGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedProviderProduct
        fields = "__all__"
        depth = 2


class FailedProviderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedProviderProduct
        fields = ['buy_order', 'failed_status', 'returned_quantity']


class FailedClientProductGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedClientProduct
        fields = "__all__"
        depth = 2


class FailedClientProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedClientProduct
        fields = ['sell_order', 'failed_status', 'returned_quantity']


class AgentSellOrderSerializer(serializers.ModelSerializer):
    # product_name, status, quantity, price, client, created_date
    product_name = serializers.CharField(max_length=50)
    client = serializers.CharField(max_length=100)

    class Meta:
        model = SellOrder
        fields = ['product_name', "status", "quantity", "price", "client", "created_date"]
