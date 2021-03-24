from django.db import models
from product.enums import ProductType, ProductUnit
from provider.models import Provider


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.CharField(max_length=15, choices=ProductUnit.choices())
    product_type = models.CharField(max_length=10, choices=ProductType.choices())
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
