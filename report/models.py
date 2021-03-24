from django.db import models
from user.models import User
from order.models import SellOrder


class SaleAgentReport(models.Model):
    sale_agent = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to="agent_report", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class Profit(models.Model):
    sell_order = models.OneToOneField(SellOrder, on_delete=models.CASCADE)
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    last_price = models.DecimalField(max_digits=20, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
