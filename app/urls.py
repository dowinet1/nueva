from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.index),
    path('iniciosesion/', views.iniciosesion),
    path('cerrarsesion/', views.cerrarsesion),
    path('aspirante/', views.aspirante),
    path('alumno/', views.alumno),
    path('crear_usuario/', views.crear_usuario),
    path('perfil/', views.perfil),
    path('lista_alumno/', views.lista_alumno),
    path('test_aptitud/', views.test_aptitud),
    path('test_intereses/', views.test_intereses),
    path('resultados/', views.resultados),
    path('reset_password/', views.reset_password),
    path('send_reset_pass/', views.send_reset_pass),
    re_path('restablecerpass/(?P<usuario>[\w.@+-]+)/', views.restablecerpass),
    path('new_pass/', views.new_pass),

    path('respuesta_test_intereses/', views.respuesta_test_intereses),
    path('respuesta_test_aptitud/', views.respuesta_test_aptitud),
    
]
