# Generated by Django 3.2.15 on 2023-04-02 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_orderelements_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('М', 'Менеджер'), ('Р', 'Ресторан'), ('К', 'Курьер'), ('Д', 'Доставлен')], default='Менеджер', max_length=100, verbose_name='Статус'),
        ),
    ]