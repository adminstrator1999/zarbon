# Generated by Django 3.1.6 on 2021-02-11 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210211_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, choices=[('limited', 'limited'), ('unlimited', 'unlimited')], max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, choices=[('kg', 'kilogram'), ('litr', 'litr'), ('ta', 'dona')], max_length=15),
        ),
    ]
