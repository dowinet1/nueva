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