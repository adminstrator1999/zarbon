# Generated by Django 3.1.6 on 2021-02-16 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20210215_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyorder',
            name='provider',
        ),
    ]