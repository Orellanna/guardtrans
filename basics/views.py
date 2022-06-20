from django.contrib import messages
from django import views
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from Modelos.models import Aduanero, Viajero, Empresa
import logging

def index(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())

def contactanos(request):
    template=loader.get_template('login.html')
    return HttpResponse(template.render())

def error404(request, exception ):
    template=loader.get_template('error404.html')
    return HttpResponse(template.render())

def login_r(request):
    if request.method == "POST":
        userdata= request.POST['username']
        passdata = request.POST['password']
        user = authenticate(request, username=userdata, password=passdata)
        if user is not None:
            login(request, user)
            usuario=user
            logging.warning('el id del usuario'+str(user.id))

            aduanero=Aduanero.objects.filter(usuario_aduanero=usuario.id).count()
            empre=Empresa.objects.filter(usuario_empresa=usuario.id).count()
            viaje=Viajero.objects.filter(usuario_viajero=usuario.id).count()
            
            logging.warning('valor de adu: '+str(aduanero) +':valor de empre'+ str(empre)+'///// : valor de viaje: '+ str(viaje))

            if aduanero> 0:
                return redirect('/admingestion')

            if empre> 0:
                return redirect('/initempresa')

            if viaje>0:
                return redirect('/initviajero')
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Usuario o contraseña incorrectos.\n Intentelo de nuevo!")
    return render(request, "login.html")


def registrar_viajero(request):
    template = loader.get_template('registroViajeroNuevo.html')
    logout(request)

    if request.method == 'POST':
        nombre = request.POST['nombre_viajero']
        apellido = request.POST['apellido_viajero']
        nacimiento = request.POST['fechanaci_viajero']
        cargo = request.POST['cargo_viajero']
        nacionalidad = request.POST['nacionalidad_viajero']
        usuario_viajero = request.POST['usuario_viajero']
        password1 = request.POST['password1_v']
        password2 = request.POST['password2_v']
         
        if password1 == password2:
            newusuario = User.objects.create_user( username = usuario_viajero)
            newusuario.set_password(password1) 
            newusuario.save()

            idempresa = Empresa.objects.get( id_empresa = 1 )
            usuariov = User.objects.get(username = usuario_viajero)

            newviajero = Viajero.objects.create( id_empresa = idempresa, tipo_user=1, nombre_viajero = nombre, apellido_viajero = apellido,
            fachanaci_viajero = nacimiento, cargo_viajero = cargo, nacionalidad_viajero = nacionalidad, usuario_viajero = usuariov)
            newviajero.save()
            user = authenticate(request, username=usuario_viajero, password=password1)
            if user is not None:
                login(request, user)
                return redirect('/initviajero')
           
        else:
            #MENSAJE DE ERROR
            messages.add_message(request=request, level=messages.ERROR, message="Las contraseñas deben coincidir.\nIntentelo de nuevo!")
            

    context={}
    return HttpResponse(template.render(context, request))


def registrar_empresa(request):  
    template = loader.get_template('registroEmpresa.html')
    logout(request)

    if request.method == 'POST':
        nombre = request.POST['nombre']
        nacionalidad = request.POST['nac']
        fechaingreso = request.POST['fecha']
        usuario_empresa = request.POST['user']
        password1 = request.POST['contra']
        password2 = request.POST['contra2']
        
        if password1 == password2:
           
            newusuario = User.objects.create_user( username = usuario_empresa)
            newusuario.set_password(password1) 
            newusuario.save()
            usuarioe = User.objects.get(username = usuario_empresa)

            newempresa = Empresa.objects.create(tipo_user=2, nombre_empresa = nombre, nacionalidad_empresa = nacionalidad,
            fechaingreso_empresa = fechaingreso, usuario_empresa = usuarioe)
            newempresa.save()   
            
            user = authenticate(request, username=usuario_empresa, password=password1)
            if user is not None:
                login(request, user)
                return redirect('/initempresa')
            
        else:
            messages.add_message(request=request, level=messages.ERROR, message="Las contraseñas deben coincidir.\nIntentelo de nuevo!")            

    context={}
    return HttpResponse(template.render(context, request))


#REGISTRO DE UN VIAJERO DESDE UN USUARIO EMPRESA----
def re_viajero(request, username = None):
    template = loader.get_template('registroViajero.html')

    userempresa = request.user

    if username and username == userempresa.username:       
        empresa = Empresa.objects.filter(usuario_empresa = userempresa).first()

        if request.method == 'POST':
            nombre = request.POST['nombre_viajero']
            apellido = request.POST['apellido_viajero']
            nacimiento = request.POST['fechanaci_viajero']
            cargo = request.POST['cargo_viajero']
            nacionalidad = request.POST['nacionalidad_viajero']
            usuario_viajero = request.POST['usuario_viajero']
            password1 = request.POST['password1_v']
            password2 = request.POST['password2_v']
            
            if password1 == password2:
                newusuario = User.objects.create_user( username = usuario_viajero)
                newusuario.set_password(password1) 
                newusuario.save()

                idempresa = Empresa.objects.get( id_empresa = empresa.id_empresa )
                usuariov = User.objects.get(username = usuario_viajero)

                newviajero = Viajero.objects.create( id_empresa = idempresa, tipo_user=1, nombre_viajero = nombre, apellido_viajero = apellido,
                fachanaci_viajero = nacimiento, cargo_viajero = cargo, nacionalidad_viajero = nacionalidad, usuario_viajero = usuariov)
                newviajero.save()         
                #return redirect('/adminu')
                messages.add_message(request=request, level=messages.SUCCESS, message="Viajero registrado correctamente!")
            else:
                #MENSAJE DE ERROR
                messages.add_message(request=request, level=messages.ERROR, message="Las contraseñas deben coincidir.\nIntentelo de nuevo!")
            

    context={}
    return HttpResponse(template.render(context, request))











