# Generated by Django 3.1.6 on 2021-02-24 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_auto_20210224_0526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fixedsalary',
            old_name='fixed',
            new_name='flexible',
        ),
    ]
