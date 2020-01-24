from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from django.conf import settings
from django.core import serializers
from django.contrib.auth.hashers import check_password
import json
import smtplib
import sweetify
import datetime

# Create your views here.


def index(request):
    usuario = request.user
    if usuario.is_active:
        usuario = Usuarios.objects.get(usuario=usuario)

        datos = {"usuario":usuario}

        return render (request, 'index.html', datos)
    else:
        return render(request, 'login.html',{})



# LOGIN Y CERRAR SESION
def iniciosesion(request):
    username = request.POST.get("usuario")
    password = request.POST.get("password")
    print("Esto llego: ", username)
    try: 
        username = authenticate(request, username=username, password=password)
        login(request,username)
        return redirect('/')
    except Exception as e:
        sweetify.error(request, 'Oops!', text='¡El Usuario y/o Contraseña es Incorrecto!', persistent=':´(')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def cerrarsesion(request):
	logout(request)
	return HttpResponseRedirect("/")


def aspirante(request):
    return render(request, "aspirante.html", {})

def alumno(request):
    return render(request, "alumno.html", {})

@csrf_exempt
def crear_usuario(request):
    tipo =  request.POST.get("tipo")
    print("Recibiendo el tipo: ", tipo)

    nombre =  request.POST.get("nombre")
    apellidos = request.POST.get("apellidos")
    usuario = request.POST.get("usuario")
    password = request.POST.get("password")
    correo = request.POST.get("correo")

    edad = request.POST.get("edad")
    sexo = request.POST.get("sexo")

    if tipo == "Aspirante":
        
        preparatoria= request.POST.get("preparatoria")
        direccion = request.POST.get("direccion")
        promedio = request.POST.get("promedio")
        area = request.POST.get("area")

        user = User.objects.filter(username=usuario).exists()
        if user == False:
            user = User.objects.create_user(first_name=nombre,
            last_name = apellidos,
            email = correo,
            username = usuario,
            password = password)

            aspirante = Usuarios.objects.create(usuario=user, tipo=tipo, edad=edad, sexo=sexo,
            preparatoria=preparatoria, direccion=direccion, promedio=promedio, area=area)

            print("Usuario creado con exito")

            user = authenticate(request, username=usuario, password=password)

            

            # user = authenticate(request, username=usuario, password=password)
    
    if tipo == "Alumno":
        no_control = request.POST.get("control")
        nip = request.POST.get("nip")
        semestre = request.POST.get("semestre")

        user = User.objects.filter(username=usuario).exists()
        if user == False:
            user = User.objects.create_user(first_name=nombre,
            last_name = apellidos,
            email = correo,
            username = usuario,
            password = password)

            alumno = Usuarios.objects.create(usuario=user, tipo=tipo, edad=edad, sexo=sexo,
            no_control=no_control, nip=nip, semestre=semestre)

            print("Usuario creado con exito")

            user = authenticate(request, username=usuario, password=password)

        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def lista_alumno(request):
    usuario = request.user
    usuario = Usuarios.objects.get(usuario=usuario)

    usuarios = Usuarios.objects.all()

    datos = {"usuario":usuario, "usuarios":usuarios}
    
    return render(request, "lista_alumno.html", datos)

def test_aptitud(request):
    usuario = request.user
    usuario = Usuarios.objects.get(usuario=usuario)

    datos = {"usuario":usuario}

    return render(request, "test_aptitud.html", datos)


def test_intereses(request):
    usuario = request.user
    usuario = Usuarios.objects.get(usuario=usuario)

    datos = {"usuario":usuario}

    return render(request, "test_intereses.html", datos)


def perfil(request):
    usuario = request.user
    usuario = Usuarios.objects.get(usuario=usuario)

    datos = {"usuario":usuario}

    return render(request, "perfil.html", datos)


def resultados(request):
    usuario = request.user
    usuario = Usuarios.objects.get(usuario=usuario)

    datos = {"usuario":usuario}

    return render(request, "resultados.html", datos)

#funciones para recuperar contraseña
def reset_password(request):

    datos = {}

    return render(request, "reset_password.html", datos)

def send_reset_pass(request):
    correo = User.objects.filter(email=request.POST.get("correo")).exists()
    print("si existe el correo")
    if correo==True:
        usuario = User.objects.get(email=request.POST.get("correo"))
        sesion = "Se ha enviado un enlace a su correo para que recupere su contraseña"
        email = EmailMessage('Recuperar contraseña de Tecnodidáctica', 'Para poder ingresar de nuevo a TECNODIDÁCTICA de click en el siguiente enlace\nhttp://localhost:8000/restablecerpass/'+usuario.username+"/",to = [request.POST.get("correo")])
        #email = EmailMessage('Recuperar contraseña de Tecnodidáctica', 'Para poder ingresar de nuevo a TECNODIDÁCTICA de click en el siguiente enlace\nhttps://wwww.tecnodidactica.com/resetpass/'+usuario.username+"/",to = [request.POST.get("correo")])
        email.send()
        a = "Por favor, verifique su bandeja de entrada"
        data = {"a":a}
        print("Envio exitoso de correo")
        
        return JsonResponse(data)

def restablecerpass(request, usuario):
	return render(request, 'new_pass.html', {'usuario':usuario})


def new_pass(request):
    usuario =  request.POST.get("usuario")
    contrasena = request.POST.get("newpass")
    validar_contrasena = request.POST.get("newpassdos")
    if contrasena == validar_contrasena:
        mi_usuario = User.objects.get(username = request.POST.get('usuario'))
        mi_usuario.set_password(contrasena)
        mi_usuario.save()
        # resultado = 1
        # # data = {"resultado":resultado}
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
        
        # resultado = 0
        # data = {"resultado":resultado}
        
        
		# return JsonResponse(data)

