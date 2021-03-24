from django.db import models
from product.models import Product
from user.models import User


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # can it be enum ?
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)


class Discount(models.Model):
    product = models.ManyToManyField(Product)
    name = models.CharField(max_length=100)
    discount = models.IntegerField()
    active = models.BooleanField()
    deadline = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


