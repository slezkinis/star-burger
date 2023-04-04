# Generated by Django 3.2.15 on 2023-04-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_auto_20230404_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Наличными', 'Наличными'), ('Электронно', 'Электронно')], default='Наличные', max_length=100, verbose_name='Способ оплаты'),
        ),
    ]
