# Generated by Django 3.1.6 on 2021-02-12 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_sale_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]