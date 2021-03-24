from django.db import models
from product.models import Product


class Warehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    last_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
