from django.db import models
from django.contrib.auth.models import User, AbstractUser
import json

# Create your models here.
TIPOS_USUARIO = (
	('Jefa','Jefa'),
	('Alumno','Alumno'),
    ('Aspirante', 'Aspirante'),
)
# class Respuesta(models.Model):
#     respuesta = models.CharField(max_length=250,null=True, blank=True)
#     puntaje = models.IntegerField()
    
#     def __str__(self):
#         return self.respuesta
    

# class Pregunta(models.Model):
#     pregunta = models.CharField(max_length=250,null=True, blank=True)
#     name = models.CharField(max_length=250,null=True, blank=True)
#     respuesta = models.ManyToManyField(Respuesta)

#     def __str__(self):
#         return self.pregunta

# class Examen_intereses(models.Model):
#     pregunta = models.ManyToManyField(Pregunta)

# class Examen_aptitud(models.Model):
#     pregunta = models.ManyToManyField(Pregunta)


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
    



class Tabla_intereses(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ss = models.IntegerField()
    ep = models.IntegerField()
    v = models.IntegerField()
    ap = models.IntegerField()
    ms = models.IntegerField()
    og = models.IntegerField()
    ct = models.IntegerField()
    ci = models.IntegerField()
    mc = models.IntegerField()
    al = models.IntegerField()
    p_ss = models.IntegerField()
    p_ep = models.IntegerField()
    p_v = models.IntegerField()
    p_ap = models.IntegerField()
    p_ms = models.IntegerField()
    p_og = models.IntegerField()
    p_ct = models.IntegerField()
    p_ci = models.IntegerField()
    p_mc = models.IntegerField()
    p_al = models.IntegerField()
    

class Tabla_aptitud(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ss = models.IntegerField()
    ep = models.IntegerField()
    v = models.IntegerField()
    ap = models.IntegerField()
    ms = models.IntegerField()
    og = models.IntegerField()
    ct = models.IntegerField()
    ci = models.IntegerField()
    mc = models.IntegerField()
    dt = models.IntegerField()
    p_ss = models.IntegerField()
    p_ep = models.IntegerField()
    p_v = models.IntegerField()
    p_ap = models.IntegerField()
    p_ms = models.IntegerField()
    p_og = models.IntegerField()
    p_ct = models.IntegerField()
    p_ci = models.IntegerField()
    p_mc = models.IntegerField()
    p_dt = models.IntegerField()
    


