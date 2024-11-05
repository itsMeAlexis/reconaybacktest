from django.contrib import admin
from contratos.models import Contrato


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    pass

# Register your models here.
