from django.db import models

from product.models import Product
from user.models import User


class Plan(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    expired = models.BooleanField(default=False)


class PlanItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


class AgentPlan(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
