from django.db import models


class Place(models.Model):
    lat = models.FloatField(verbose_name='Геог. широта', null=True)
    lon = models.FloatField(verbose_name='Геог. долгота', null=True)
    adress = models.CharField('Адрес места', max_length=100)
    data = models.DateField('Дата запроса к геокодеру')

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self) -> str:
        return self.adress