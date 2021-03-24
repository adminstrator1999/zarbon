from django.db import models

from product.models import Product
from provider.models import Provider
from client.models import Client
from user.models import User
from order.enums import OrderPaymentType, OrderStatus, FailedProductStatus


# we need to create new order when we add the same product update
class BuyOrder(models.Model):
    """Creating database for buying products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    # Three types of paying, via cash or credit card or it can be debt
    deadline = models.DateTimeField(default=None, null=True, blank=True)
    debt = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.product.provider.name}-{self.product.name}'


class BuyOrderPayment(models.Model):
    buy_order = models.ForeignKey(BuyOrder, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=15, choices=OrderPaymentType.choices())
    payment = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True)


class SellOrder(models.Model):
    """Creating datatable for selling products
    the first order will be created by sale_agent"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    # ordered and delivered
    status = models.CharField(max_length=15, choices=OrderStatus.choices(), default="ordered")
    debt = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    deadline = models.DateTimeField(default=None, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.client.name}-{self.product.name}'


class SellOrderPayment(models.Model):
    sell_order = models.ForeignKey(SellOrder, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=15, choices=OrderPaymentType.choices())
    payment = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True)


# failed product is under discussion
class FailedProviderProduct(models.Model):
    """Creating datatable for Failed Products from the provider"""
    buy_order = models.ForeignKey(BuyOrder, on_delete=models.CASCADE)
    failed_status = models.CharField(max_length=8, choices=FailedProductStatus.choices())
    returned_quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)


class FailedClientProduct(models.Model):
    """Creating database for Failed Products from the Client"""
    sell_order = models.ForeignKey(SellOrder, on_delete=models.CASCADE)
    failed_status = models.CharField(max_length=8, choices=FailedProductStatus.choices())
    returned_quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
