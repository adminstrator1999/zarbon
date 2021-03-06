# Generated by Django 3.1.6 on 2021-02-11 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210211_1652'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0007_sellorder_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleAgentOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('payed_part', models.DecimalField(decimal_places=2, max_digits=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
