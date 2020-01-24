from django.db import models
from django.contrib.auth.models import User, AbstractUser
import json

# Create your models here.
TIPOS_USUARIO = (
	('Jefa','Jefa'),
	('Alumno','Alumno'),
    ('Aspirante', 'Aspirante'),
)

class Usuarios(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, blank=True, null=True, choices=TIPOS_USUARIO)
    edad = models.CharField(max_length=100, blank=True, null=True)
    sexo= models.CharField(max_length=100, blank=True, null=True)
    preparatoria = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    promedio = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    no_control = models.CharField(max_length=100, blank=True, null=True)
    nip = models.CharField(max_length=100, blank=True, null=True)
    semestre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.usuario.username

