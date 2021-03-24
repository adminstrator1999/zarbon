from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token

from .enums import UserRole


class UserManager(BaseUserManager):

    def _create_user(self, phone_number, role, first_name, last_name, password=None, **extra_fields):
        """ check if user have set required fields"""
        if not phone_number:
            raise ValueError("user must have phone number")
        if not first_name:
            raise ValueError("user must have first_name")
        if not last_name:
            raise ValueError("user must have last_name")
        if not role:
            raise ValueError("user must have role")
        user = self.model(phone_number=phone_number, role=role, first_name=first_name, last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, role, first_name, last_name, password=None, **extra_fields):
        self._create_user(phone_number=phone_number, role=role, first_name=first_name, last_name=last_name,
                          password=password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self._create_user(phone_number=phone_number, password=password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                           message="Phone number must be entered in the format: '+998991234567'. "
                                                   "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex_validator], max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices())
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True, null=True, blank=True) # can't be blank
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name', ]
    objects = UserManager()

    def __str__(self):
        return f'{self.role} {self.first_name}'

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission?
        return True

    def has_module_perms(self, app_label):
        # Does the user have permissions to view the app ?
        return True

    @property
    def is_staff(self):
        return self.is_superuser
