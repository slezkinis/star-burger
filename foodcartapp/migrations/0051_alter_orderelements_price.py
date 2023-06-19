# Generated by Django 3.2.15 on 2023-05-08 07:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_alter_orderelements_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelements',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
    ]