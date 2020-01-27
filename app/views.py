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
        email = EmailMessage('Recuperar contraseña de Test', 'Para poder ingresar de nuevo a TECNODIDÁCTICA de click en el siguiente enlace\nhttp://localhost:8000/restablecerpass/'+usuario.username+"/",to = [request.POST.get("correo")])
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

def respuesta_test_intereses(request):
    usuario = request.user
    pregunta_uno= int(request.POST.get("pregunta_uno"))
    pregunta_dos= int(request.POST.get("pregunta_dos"))
    pregunta_tres= int(request.POST.get("pregunta_tres"))
    pregunta_cuatro= int(request.POST.get("pregunta_cuatro"))
    pregunta_cinco= int(request.POST.get("pregunta_cinco"))
    pregunta_seis= int(request.POST.get("pregunta_seis"))
    pregunta_siete= int(request.POST.get("pregunta_siete"))
    pregunta_ocho= int(request.POST.get("pregunta_ocho"))
    pregunta_nueve= int(request.POST.get("pregunta_nueve"))
    pregunta_diez= int(request.POST.get("pregunta_diez"))
    pregunta_once= int(request.POST.get("pregunta_once"))
    pregunta_doce= int(request.POST.get("pregunta_doce"))
    pregunta_trece= int(request.POST.get("pregunta_trece"))
    pregunta_catorce= int(request.POST.get("pregunta_catorce"))
    pregunta_quince= int(request.POST.get("pregunta_quince"))
    pregunta_dseis= int(request.POST.get("pregunta_dseis"))
    pregunta_dsiete= int(request.POST.get("pregunta_dsiete"))
    pregunta_docho= int(request.POST.get("pregunta_docho"))
    pregunta_dnueve= int(request.POST.get("pregunta_dnueve"))
    pregunta_veinte= int(request.POST.get("pregunta_veinte"))
    pregunta_vuno= int(request.POST.get("pregunta_vuno"))
    pregunta_vdos= int(request.POST.get("pregunta_vdos"))
    pregunta_vtres= int(request.POST.get("pregunta_vtres"))
    pregunta_vtres= int(request.POST.get("pregunta_vtres"))
    pregunta_vcuatro= int(request.POST.get("pregunta_vcuatro"))
    pregunta_vcinco= int(request.POST.get("pregunta_vcinco"))
    pregunta_vseis= int(request.POST.get("pregunta_vseis"))
    pregunta_vsiete= int(request.POST.get("pregunta_vsiete"))
    pregunta_vocho= int(request.POST.get("pregunta_vocho"))
    pregunta_vnueve= int(request.POST.get("pregunta_vnueve"))
    pregunta_treinta= int(request.POST.get("pregunta_treinta"))
    pregunta_tuno= int(request.POST.get("pregunta_tuno"))
    pregunta_tdos= int(request.POST.get("pregunta_tdos"))
    pregunta_tdos= int(request.POST.get("pregunta_tdos"))
    pregunta_ttres= int(request.POST.get("pregunta_ttres"))
    pregunta_tcuatro= int(request.POST.get("pregunta_tcuatro"))
    pregunta_tcuatro= int(request.POST.get("pregunta_tcuatro"))
    pregunta_tcinco= int(request.POST.get("pregunta_tcinco"))
    pregunta_tseis= int(request.POST.get("pregunta_tseis"))
    pregunta_tsiete= int(request.POST.get("pregunta_tsiete"))
    pregunta_tocho= int(request.POST.get("pregunta_tocho"))
    pregunta_tnueve= int(request.POST.get("pregunta_tnueve"))
    pregunta_cuarenta= int(request.POST.get("pregunta_cuarenta"))
    pregunta_cuno= int(request.POST.get("pregunta_cuno"))
    pregunta_cdos= int(request.POST.get("pregunta_cdos"))
    pregunta_ctres= int(request.POST.get("pregunta_ctres"))
    pregunta_ccuatro= int(request.POST.get("pregunta_ccuatro"))
    pregunta_ccinco= int(request.POST.get("pregunta_ccinco"))
    pregunta_cseis= int(request.POST.get("pregunta_cseis"))
    pregunta_csiete= int(request.POST.get("pregunta_csiete"))
    pregunta_cocho= int(request.POST.get("pregunta_cocho"))
    pregunta_cnueve= int(request.POST.get("pregunta_cnueve"))
    pregunta_cincuenta= int(request.POST.get("pregunta_cincuenta"))
    pregunta_suno= int(request.POST.get("pregunta_suno"))
    pregunta_sdos= int(request.POST.get("pregunta_sdos"))
    pregunta_stres= int(request.POST.get("pregunta_stres"))
    pregunta_scuatro= int(request.POST.get("pregunta_scuatro"))
    pregunta_scinco= int(request.POST.get("pregunta_scinco"))
    pregunta_sseis= int(request.POST.get("pregunta_sseis"))
    pregunta_ssiete= int(request.POST.get("pregunta_ssiete"))
    pregunta_socho= int(request.POST.get("pregunta_socho"))
    pregunta_snueve= int(request.POST.get("pregunta_snueve"))
    pregunta_sesenta= int(request.POST.get("pregunta_sesenta"))


    ss = pregunta_uno + pregunta_once + pregunta_vuno + pregunta_tuno + pregunta_cuno + pregunta_suno
    ep = pregunta_dos + pregunta_doce + pregunta_vdos + pregunta_tdos + pregunta_cdos + pregunta_sdos
    v = pregunta_tres + pregunta_trece + pregunta_vtres + pregunta_ttres + pregunta_ctres + pregunta_stres
    ap = pregunta_cuatro + pregunta_catorce + pregunta_vcuatro + pregunta_tcuatro + pregunta_ccuatro + pregunta_scuatro
    ms = pregunta_cinco + pregunta_quince + pregunta_vcinco + pregunta_tcinco + pregunta_ccinco + pregunta_scinco
    og = pregunta_seis + pregunta_dseis + pregunta_vseis + pregunta_tseis + pregunta_cseis + pregunta_sseis
    ct = pregunta_siete + pregunta_dsiete + pregunta_vsiete + pregunta_tsiete + pregunta_tsiete + pregunta_ssiete
    ci = pregunta_ocho + pregunta_docho + pregunta_vocho + pregunta_tocho + pregunta_cocho + pregunta_socho
    mc = pregunta_nueve + pregunta_dnueve + pregunta_vnueve + pregunta_tnueve + pregunta_cnueve + pregunta_dnueve
    al = pregunta_diez + pregunta_veinte + pregunta_treinta + pregunta_cuarenta + pregunta_cincuenta + pregunta_sesenta

    valor = 100/24

    p_ss = round(ss * valor)
    p_ep = round(ep * valor)
    p_v = round(v * valor)
    p_ap = round(ap * valor)
    p_ms = round(ms * valor)
    p_og = round(og * valor)
    p_ct = round(ct * valor)
    p_ci = round(ci * valor)
    p_mc = round(mc * valor)
    p_al = round(al * valor)

    print("suma: ", ss, " porcentaje: ", p_ss)
    print("suma: ", ep, " porcentaje: ", p_ep)
    print("suma: ", v, " porcentaje: ", p_v)
    print("suma: ", ap, " porcentaje: ", p_ap)
    print("suma: ", ms, " porcentaje: ", p_ms)
    print("suma: ", og, " porcentaje: ", p_og)
    print("suma: ", ct, " porcentaje: ", p_ct)
    print("suma: ", ci, " porcentaje: ", p_ci)
    print("suma: ", mc, " porcentaje: ", p_mc)
    print("suma: ", al, " porcentaje: ", p_al)


    resultados = Tabla_intereses.objects.create(usuario=usuario, ss=ss, ep=ep, v=v, ap=ap, ms=ms, og=og,
    ct=ct, ci=ci, mc=mc, al=al, p_ss=p_ss, p_ep=p_ep, p_v=p_v, p_ap=p_ap, p_ms=p_ms, p_og=p_og, p_ct=p_ct,
    p_ci=p_ci, p_mc=p_mc, p_al=p_al)

    print("Creado con éxito")

    return HttpResponseRedirect("/")



def respuesta_test_aptitud(request):
    usuario = request.user
    pregunta_uno= int(request.POST.get("pregunta_uno"))
    pregunta_dos= int(request.POST.get("pregunta_dos"))
    pregunta_tres= int(request.POST.get("pregunta_tres"))
    pregunta_cuatro= int(request.POST.get("pregunta_cuatro"))
    pregunta_cinco= int(request.POST.get("pregunta_cinco"))
    pregunta_seis= int(request.POST.get("pregunta_seis"))
    pregunta_siete= int(request.POST.get("pregunta_siete"))
    pregunta_ocho= int(request.POST.get("pregunta_ocho"))
    pregunta_nueve= int(request.POST.get("pregunta_nueve"))
    pregunta_diez= int(request.POST.get("pregunta_diez"))
    pregunta_once= int(request.POST.get("pregunta_once"))
    pregunta_doce= int(request.POST.get("pregunta_doce"))
    pregunta_trece= int(request.POST.get("pregunta_trece"))
    pregunta_catorce= int(request.POST.get("pregunta_catorce"))
    pregunta_quince= int(request.POST.get("pregunta_quince"))
    pregunta_dseis= int(request.POST.get("pregunta_dseis"))
    pregunta_dsiete= int(request.POST.get("pregunta_dsiete"))
    pregunta_docho= int(request.POST.get("pregunta_docho"))
    pregunta_dnueve= int(request.POST.get("pregunta_dnueve"))
    pregunta_veinte= int(request.POST.get("pregunta_veinte"))
    pregunta_vuno= int(request.POST.get("pregunta_vuno"))
    pregunta_vdos= int(request.POST.get("pregunta_vdos"))
    pregunta_vtres= int(request.POST.get("pregunta_vtres"))
    pregunta_vtres= int(request.POST.get("pregunta_vtres"))
    pregunta_vcuatro= int(request.POST.get("pregunta_vcuatro"))
    pregunta_vcinco= int(request.POST.get("pregunta_vcinco"))
    pregunta_vseis= int(request.POST.get("pregunta_vseis"))
    pregunta_vsiete= int(request.POST.get("pregunta_vsiete"))
    pregunta_vocho= int(request.POST.get("pregunta_vocho"))
    pregunta_vnueve= int(request.POST.get("pregunta_vnueve"))
    pregunta_treinta= int(request.POST.get("pregunta_treinta"))
    pregunta_tuno= int(request.POST.get("pregunta_tuno"))
    pregunta_tdos= int(request.POST.get("pregunta_tdos"))
    pregunta_tdos= int(request.POST.get("pregunta_tdos"))
    pregunta_ttres= int(request.POST.get("pregunta_ttres"))
    pregunta_tcuatro= int(request.POST.get("pregunta_tcuatro"))
    pregunta_tcuatro= int(request.POST.get("pregunta_tcuatro"))
    pregunta_tcinco= int(request.POST.get("pregunta_tcinco"))
    pregunta_tseis= int(request.POST.get("pregunta_tseis"))
    pregunta_tsiete= int(request.POST.get("pregunta_tsiete"))
    pregunta_tocho= int(request.POST.get("pregunta_tocho"))
    pregunta_tnueve= int(request.POST.get("pregunta_tnueve"))
    pregunta_cuarenta= int(request.POST.get("pregunta_cuarenta"))
    pregunta_cuno= int(request.POST.get("pregunta_cuno"))
    pregunta_cdos= int(request.POST.get("pregunta_cdos"))
    pregunta_ctres= int(request.POST.get("pregunta_ctres"))
    pregunta_ccuatro= int(request.POST.get("pregunta_ccuatro"))
    pregunta_ccinco= int(request.POST.get("pregunta_ccinco"))
    pregunta_cseis= int(request.POST.get("pregunta_cseis"))
    pregunta_csiete= int(request.POST.get("pregunta_csiete"))
    pregunta_cocho= int(request.POST.get("pregunta_cocho"))
    pregunta_cnueve= int(request.POST.get("pregunta_cnueve"))
    pregunta_cincuenta= int(request.POST.get("pregunta_cincuenta"))
    pregunta_suno= int(request.POST.get("pregunta_suno"))
    pregunta_sdos= int(request.POST.get("pregunta_sdos"))
    pregunta_stres= int(request.POST.get("pregunta_stres"))
    pregunta_scuatro= int(request.POST.get("pregunta_scuatro"))
    pregunta_scinco= int(request.POST.get("pregunta_scinco"))
    pregunta_sseis= int(request.POST.get("pregunta_sseis"))
    pregunta_ssiete= int(request.POST.get("pregunta_ssiete"))
    pregunta_socho= int(request.POST.get("pregunta_socho"))
    pregunta_snueve= int(request.POST.get("pregunta_snueve"))
    pregunta_sesenta= int(request.POST.get("pregunta_sesenta"))


    ss = pregunta_uno + pregunta_once + pregunta_vuno + pregunta_tuno + pregunta_cuno + pregunta_suno
    ep = pregunta_dos + pregunta_doce + pregunta_vdos + pregunta_tdos + pregunta_cdos + pregunta_sdos
    v = pregunta_tres + pregunta_trece + pregunta_vtres + pregunta_ttres + pregunta_ctres + pregunta_stres
    ap = pregunta_cuatro + pregunta_catorce + pregunta_vcuatro + pregunta_tcuatro + pregunta_ccuatro + pregunta_scuatro
    ms = pregunta_cinco + pregunta_quince + pregunta_vcinco + pregunta_tcinco + pregunta_ccinco + pregunta_scinco
    og = pregunta_seis + pregunta_dseis + pregunta_vseis + pregunta_tseis + pregunta_cseis + pregunta_sseis
    ct = pregunta_siete + pregunta_dsiete + pregunta_vsiete + pregunta_tsiete + pregunta_tsiete + pregunta_ssiete
    ci = pregunta_ocho + pregunta_docho + pregunta_vocho + pregunta_tocho + pregunta_cocho + pregunta_socho
    mc = pregunta_nueve + pregunta_dnueve + pregunta_vnueve + pregunta_tnueve + pregunta_cnueve + pregunta_dnueve
    dt = pregunta_diez + pregunta_veinte + pregunta_treinta + pregunta_cuarenta + pregunta_cincuenta + pregunta_sesenta

    valor = 100/24

    p_ss = round(ss * valor)
    p_ep = round(ep * valor)
    p_v = round(v * valor)
    p_ap = round(ap * valor)
    p_ms = round(ms * valor)
    p_og = round(og * valor)
    p_ct = round(ct * valor)
    p_ci = round(ci * valor)
    p_mc = round(mc * valor)
    p_dt = round(dt * valor)

    print("suma: ", ss, " porcentaje: ", p_ss)
    print("suma: ", ep, " porcentaje: ", p_ep)
    print("suma: ", v, " porcentaje: ", p_v)
    print("suma: ", ap, " porcentaje: ", p_ap)
    print("suma: ", ms, " porcentaje: ", p_ms)
    print("suma: ", og, " porcentaje: ", p_og)
    print("suma: ", ct, " porcentaje: ", p_ct)
    print("suma: ", ci, " porcentaje: ", p_ci)
    print("suma: ", mc, " porcentaje: ", p_mc)
    print("suma: ", dt, " porcentaje: ", p_dt)


    resultados = Tabla_aptitud.objects.create(usuario=usuario, ss=ss, ep=ep, v=v, ap=ap, ms=ms, og=og,
    ct=ct, ci=ci, mc=mc, dt=dt, p_ss=p_ss, p_ep=p_ep, p_v=p_v, p_ap=p_ap, p_ms=p_ms, p_og=p_og, p_ct=p_ct,
    p_ci=p_ci, p_mc=p_mc, p_dt=p_dt)

    print("Creado con éxito")

    return HttpResponseRedirect("/")


def resultados(request):
    usuario = request.user
    # usuario = Usuarios.objects.get(usuario=usuario)

    tabla_intereses = Tabla_intereses.objects.get(usuario=usuario)
    tabla_aptitud = Tabla_aptitud.objects.get(usuario=usuario)

    #Datos dE PORCENTAJE  de examen de intereses
    p_ss_int = tabla_intereses.p_ss
    p_ep_int = tabla_intereses.p_ep
    p_v_int = tabla_intereses.p_v
    p_ap_int = tabla_intereses.p_ap
    p_ms_int = tabla_intereses.p_ms
    p_og_int = tabla_intereses.p_og
    p_ct_int = tabla_intereses.p_ct
    p_ci_int = tabla_intereses.p_ci
    p_mc_int = tabla_intereses.p_mc
    p_al_int = tabla_intereses.p_al

    if p_ss_int > p_ep_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ct_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Urbanismo", "Ingeniería Civil", "Sociología","Trabajo Social", "Derecho"]
    
    if p_ep_int > p_ss_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ct_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Actuaría", "Economía", "Administración","Ciencias Políticas", "Administración"]
    
    if p_v_int > p_ss_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ct_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Derecho", "Ciencias de la Comunicación","Letras Clásicas", "Lengua" , "Literaturas"]
    
    if p_ap_int > p_ss_int and p_ep_int and p_v_int and p_ms_int and p_og_int and p_ct_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Artes Visuales", "Diseño y comunicación Visual", "Diseño Gráfico", "Arquitectura","Arquitectura de Paisaje"]

    if p_ms_int > p_ss_int and p_ep_int and p_v_int and p_ap_int and p_og_int and p_ct_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Composición", "Instrumentista", "Canto", "Etnomusicología", "Piano"]
    
    if p_og_int > p_ss_int and p_ep_int and p_v_int and p_ap_int and p_ms_int and p_ct_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Bibliotecología y Estudios de la Información", "Actuaría", "Matemáticas Aplicadas y Computación", "Informática","Contaduría"]

    if p_ct_int> p_ss_int and p_ep_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ci_int and p_mc_int and p_al_int:
        carreras_intereses = ["Investigación Biomédica Básica", "Ciencias Genómicas", "Matemáticas", "Física","Ingeniería Mecatrónica"]
    
    if p_ci_int> p_ss_int and p_ep_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ct_int and p_mc_int and p_al_int:
        carreras_intereses = ["Matemáticas", "Economía", "Contaduría","Física", "Ingenierías"]
    
    if p_mc_int> p_ss_int and p_ep_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ct_int and p_ci_int and p_al_int:
        carreras_intereses = ["Eléctrica-Electrónica","Geofísica", "Topográfica", "Civil", "Petrolera"]

    if p_al_int> p_ss_int and p_ep_int and p_v_int and p_ap_int and p_ms_int and p_og_int and p_ct_int and p_ci_int and p_mc_int:
        carreras_intereses = ["Biología", "Ingeniería Agrícola", "Ingeniería Geológica", "Ingeniería Petrolera", "Geografía"]


       
    #Datos PORCENTAJE de examen de aptitud
    p_ss_ap = tabla_aptitud.p_ss
    p_ep_ap = tabla_aptitud.p_ep
    p_v_ap = tabla_aptitud.p_v
    p_ap_ap = tabla_aptitud.p_ap
    p_ms_ap = tabla_aptitud.p_ms
    p_og_ap = tabla_aptitud.p_og
    p_ct_ap = tabla_aptitud.p_ct
    p_ci_ap = tabla_aptitud.p_ci
    p_mc_ap = tabla_aptitud.p_mc
    p_dt_ap = tabla_aptitud.p_dt


    if p_ep_ap > p_ss_ap and p_v_ap and p_ap_ap and p_ms_ap and p_og_ap and p_ct_ap and p_ci_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Actuaría", "Economía", "Administración","Ciencias Políticas", "Administración"]
    
    if p_v_ap > p_ss_ap and p_v_int and p_ap_ap and p_ms_ap and p_og_ap and p_ct_ap and p_ci_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Derecho", "Ciencias de la Comunicación","Letras Clásicas", "Lengua" , "Literaturas"]
    
    if p_ap_ap > p_ss_ap and p_ep_ap and p_v_ap and p_ms_ap and p_og_ap and p_ct_ap and p_ci_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Artes Visuales", "Diseño y comunicación Visual", "Diseño Gráfico", "Arquitectura","Arquitectura de Paisaje"]

    if p_ms_ap > p_ss_ap and p_ep_ap and p_v_ap and p_ap_ap and p_og_ap and p_ct_ap and p_ci_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Composición", "Instrumentista", "Canto", "Etnomusicología", "Piano"]
    
    if p_og_ap > p_ss_ap and p_ep_ap and p_v_ap and p_ap_ap and p_ms_ap and p_ct_ap and p_ci_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Bibliotecología y Estudios de la Información", "Actuaría", "Matemáticas Aplicadas y Computación", "Informática","Contaduría"]

    if p_ct_ap> p_ss_ap and p_ep_ap and p_v_ap and p_ap_ap and p_ms_ap and p_og_ap and p_ci_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Investigación Biomédica Básica", "Ciencias Genómicas", "Matemáticas", "Física","Ingeniería Mecatrónica"]
    
    if p_ci_ap> p_ss_ap and p_ep_int and p_v_ap and p_ap_ap and p_ms_ap and p_og_ap and p_ct_ap and p_mc_ap and p_dt_ap:
        carreras_aptitud = ["Matemáticas", "Economía", "Contaduría","Física", "Ingenierías"]
    
    if p_mc_ap> p_ss_ap and p_ep_int and p_v_ap and p_ap_ap and p_ms_ap and p_og_ap and p_ct_ap and p_ci_ap and p_dt_ap:
        carreras_aptitud = ["Eléctrica-Electrónica","Geofísica", "Topográfica", "Civil", "Petrolera"]

    if p_dt_ap> p_ss_ap and p_ep_ap and p_v_ap and p_ap_ap and p_ms_ap and p_og_ap and p_ct_ap and p_ci_ap and p_mc_int:
        carreras_aptitud = ["Biología", "Ingeniería Agrícola", "Ingeniería Geológica", "Ingeniería Petrolera", "Geografía"]



    datos = {"usuario":usuario,
    "p_ss_ap":p_ss_ap, 
    "p_ep_ap":p_ep_ap, 
    "p_v_ap":p_v_ap, 
    "p_ap_ap":p_ap_ap, 
    "p_ms_ap":p_ms_ap, 
    "p_og_ap":p_og_ap, 
    "p_ct_ap":p_ct_ap, 
    "p_ci_ap":p_ci_ap, 
    "p_mc_ap":p_mc_ap, 
    "p_dt_ap":p_dt_ap, 
    "carreras_aptitud":carreras_aptitud,
    
    "p_ss_int":p_ss_int, 
    "p_ep_int": p_ep_int, 
    "p_v_int":p_v_int, 
    "p_ap_int":p_ap_int, 
    "p_ms_int":p_ms_int, 
    "p_og_int":p_og_int, 
    "p_ct_int":p_ct_int, 
    "p_ci_int":p_ci_int, 
    "p_mc_int":p_mc_int, 
    "p_al_int":p_al_int, 
    "carreras_intereses":carreras_intereses
       }

    return render(request, "resultados.html", datos)

