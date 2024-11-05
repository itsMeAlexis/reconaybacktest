from django.contrib import admin
from fichastecnicas.models import FichaTecnica


@admin.register(FichaTecnica)
class FichaTecnicaAdmin(admin.ModelAdmin):
    pass
