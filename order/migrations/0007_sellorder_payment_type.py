# Generated by Django 3.1.6 on 2021-02-11 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_sellorder_sale_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellorder',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'cash'), ('credit_card', 'credit_card'), ('debt', 'debt')], default=1, max_length=15),
            preserve_default=False,
        ),
    ]
