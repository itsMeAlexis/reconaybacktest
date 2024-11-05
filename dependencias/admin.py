from django.contrib import admin
from dependencias.models import Dependencia

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    pass


