from django.core.validators import RegexValidator
from django.db import models
from user.models import User
from product.models import Product


class Client(models.Model):
    phone_regex_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                           message="Phone number must be entered in the format: '+998991234567'. "
                                                   "Up to 15 digits allowed.")
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    phone_number1 = models.CharField(validators=[phone_regex_validator], max_length=16)
    phone_number2 = models.CharField(validators=[phone_regex_validator], max_length=16, blank=True, null=True)
    account_number = models.IntegerField()
    bank = models.CharField(max_length=120)
    bank_code = models.IntegerField()  # MFO
    INN = models.IntegerField()
    director = models.CharField(max_length=120)
    responsible_agent = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    sale_agent = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AgentClientReport(models.Model):
    phone_regex_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                           message="Phone number must be entered in the format: '+998991234567'. "
                                                   "Up to 15 digits allowed.")
    sale_agent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    responsible_person = models.CharField(max_length=50)
    phone_number1 = models.CharField(validators=[phone_regex_validator], max_length=16)
    phone_number2 = models.CharField(validators=[phone_regex_validator], max_length=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    image = models.ImageField(upload_to="client")
    assumption_value = models.DecimalField(max_digits=20, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
