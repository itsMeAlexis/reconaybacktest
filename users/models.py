from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nombreDependencia = models.CharField(max_length=200, null=True, blank=True)
    DP = models.CharField(max_length=200, null=True, blank=True)
    puesto = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    correo = models.CharField(max_length=200, null=True, blank=True)
    clave = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=50, unique=False)
    


class CustomEmailValidator(EmailValidator):
    def __call__(self, value):
        super().__call__(value)  # Realizar la validación base de Django

        # Agregar validación adicional para permitir dominios específicos
        allowed_domains = ['gmail.com', 'hotmail.com', 'nay.gob.mx',
                           'nayarit.gob.mx', 'uan.edu.mx', 'outlook.es', 'sdsnayarit.gob.mx','outlook.com']
        domain = value.split('@')[1]

        if domain not in allowed_domains:
            raise ValidationError(
                'Hola el dominio del correo electrónico no está permitido.')


User._meta.get_field('email').validators = [CustomEmailValidator()]
