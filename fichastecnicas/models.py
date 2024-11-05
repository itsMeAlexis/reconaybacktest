from django.db import models
from django.db.models.fields.files import FieldFile

class FichaTecnica(models.Model):
    dependenciaFicha = models.ForeignKey('dependencias.Dependencia',on_delete = models.SET_NULL, null=True, blank=True)
    nombrePdS = models.CharField(max_length=255, null=True, blank=True)
    telefonoPdS = models.CharField(max_length=255, null=True, blank=True)
    servicioRequerido = models.CharField(max_length=500, null=True, blank=True)
    areaRequiereServicio = models.CharField(max_length=500, null=True, blank=True)
    domicilioUnidadAdmin = models.CharField(max_length=255, null=True, blank=True)
    nombreTitularSolicitante = models.CharField(max_length=255, null=True, blank=True)
    cargoTitularSolicitante = models.CharField(max_length=255, null=True, blank=True)
    tipoContrato = models.CharField(max_length=255, null=True, blank=True)
    fechaInicioContrato = models.CharField(max_length=20, null=True, blank=True)
    fechaFinContrato = models.CharField(max_length=20, null=True, blank=True)
    importeMensual = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    ajusteMensual = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)    
    nombreSecretario = models.CharField(max_length=200, null=True, blank=True)
    puestoSecretario = models.CharField(max_length=200, null=True, blank=True)
    nombreVoBo = models.CharField(max_length=200, null=True, blank=True)
    puestoVoBo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombrePdS
