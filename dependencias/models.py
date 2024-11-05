from django.db import models

class Dependencia(models.Model):
    nombreDependencia = models.CharField(max_length=200, null=True, blank=True)
    DP =  models.CharField(max_length=10, null=True, blank=True)
    UR =  models.CharField(max_length=10, null=True, blank=True)
    nombreSecretario =  models.CharField(max_length=200, null=True, blank=True)
    puestoSecretario =  models.CharField(max_length=200, null=True, blank=True)    
    nombreCoordinador =  models.CharField(max_length=200, null=True, blank=True)
    puestoCoordinador =  models.CharField(max_length=200, null=True, blank=True)    
    NoUR =  models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to='dependencias', blank='True')
    dependencia_id = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.nombreDependencia