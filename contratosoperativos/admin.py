from django.contrib import admin
from contratosoperativos.models import ContratoOperativo


@admin.register(ContratoOperativo)
class ContratoOperativoAdmin(admin.ModelAdmin):
    pass


# Register your models here.
