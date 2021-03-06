# Generated by Django 3.1.6 on 2021-02-15 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20210213_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedClientProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failed_status', models.CharField(choices=[('fully', 'fully'), ('party', 'party')], max_length=6)),
                ('returned_products_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('sell_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.sellorder')),
            ],
        ),
        migrations.CreateModel(
            name='FailedProviderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failed_status', models.CharField(choices=[('fully', 'fully'), ('party', 'party')], max_length=6)),
                ('returned_products_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('buy_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.buyorder')),
            ],
        ),
        migrations.DeleteModel(
            name='FailedProduct',
        ),
    ]
