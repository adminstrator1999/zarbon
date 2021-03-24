from django.db import models
from user.models import User
from user.enums import UserRole


class FixedSalary(models.Model):
    role = models.CharField(max_length=20, choices=UserRole.choices())
    salary_quantity = models.DecimalField(max_digits=20, decimal_places=2)
    flexible = models.BooleanField(default=False)


class Salary(models.Model):
    salary = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


