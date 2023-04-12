# Generated by Django 3.2.15 on 2023-04-12 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_order_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='order',
            name='executive_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodcartapp.restaurant', verbose_name='Ресторан, который готовит'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличными'), ('electronically', 'Электронно')], max_length=100, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('manager', 'Менеджер'), ('restaurant', 'Ресторан'), ('courier', 'Курьер'), ('delivered', 'Доставлен')], default='Менеджер', max_length=100, verbose_name='Статус'),
        ),
    ]