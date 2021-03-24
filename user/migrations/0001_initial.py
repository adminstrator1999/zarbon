# Generated by Django 3.1.6 on 2021-02-03 07:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+998991234567'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('role', models.CharField(choices=[('CEO', 'CEO'), ('director', 'director'), ('commodity_accountant', 'commodity_accountant'), ('accountant', 'accountant'), ('cashier', 'cashier'), ('agent', 'agent')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
