# Generated by Django 3.1.6 on 2021-03-08 09:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20210302_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='phone',
            new_name='phone_number1',
        ),
        migrations.AddField(
            model_name='client',
            name='INN',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='account_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='bank',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='bank_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='director',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='latitude',
            field=models.DecimalField(decimal_places=20, default=1, max_digits=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='longitude',
            field=models.DecimalField(decimal_places=20, default=1, max_digits=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+998991234567'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
