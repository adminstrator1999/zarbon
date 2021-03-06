# Generated by Django 3.1.6 on 2021-02-10 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('provider', '0002_auto_20210208_1337'),
        ('order', '0004_auto_20210210_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AlterField(
            model_name='buyorder',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.provider'),
        ),
    ]
