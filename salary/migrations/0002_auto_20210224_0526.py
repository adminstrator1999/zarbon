# Generated by Django 3.1.6 on 2021-02-24 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('CEO', 'CEO'), ('director', 'director'), ('commodity_accountant', 'commodity_accountant'), ('accountant', 'accountant'), ('cashier', 'cashier'), ('agent', 'agent')], max_length=20)),
                ('salary_quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('fixed', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='salary',
            name='CEO_salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='accountant_salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='agent_flexible_salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='agent_salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='cashier_salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='commodity_accountant_salary',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='director_salary',
        ),
        migrations.AddField(
            model_name='salary',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salary',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salary',
            name='salary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='salary.fixedsalary'),
        ),
    ]
