from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass