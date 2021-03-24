# Generated by Django 3.1.6 on 2021-02-13 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_remove_buyorder_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellOrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('cash', 'cash'), ('credit_card', 'credit_card')], max_length=15)),
                ('payment', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sellorder',
            name='payment_type',
        ),
        migrations.AddField(
            model_name='buyorder',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sellorder',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyorderpayment',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'cash'), ('credit_card', 'credit_card')], max_length=15),
        ),
        migrations.AlterField(
            model_name='sellorder',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered'), ('delivered', 'delivered')], default='ordered', max_length=15),
        ),
        migrations.DeleteModel(
            name='SaleAgentOrder',
        ),
        migrations.AddField(
            model_name='sellorderpayment',
            name='sell_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.sellorder'),
        ),
    ]
