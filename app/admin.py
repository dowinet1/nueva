from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, AbstractUser

# Register your models here.
class Usuario(admin.ModelAdmin):
    list_display = ["id","usuario"]
    list_display_links = ["usuario"]
    search_fields = ['usuario']
    
    class Meta:
        model = Usuarios


admin.site.register(Usuarios, Usuario)
admin.site.register(Tabla_intereses)
admin.site.register(Tabla_aptitud)
# admin.site.register(Respuesta)
# admin.site.register(Pregunta)
# admin.site.register(Examen_intereses)
# admin.site.register(Examen_aptitud)