import logging
import re
from urllib.request import Request
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpRequest, QueryDict
from django.template import loader
from Modelos.models import User,Empresa,Vehiculo, Viajero
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url="/login")
def admin_vehiculo(request , username = None):  
    template = loader.get_template('administrarVehiculo.html')

    usuario1=Viajero.objects.filter(usuario_viajero=User.objects.get(id=request.user.id)).first()
    usuario2=Empresa.objects.filter(usuario_empresa=User.objects.get(id=request.user.id)).first()

    logging.warning('prueba'+str(bool(usuario1)))
    logging.warning('prueba'+str(bool(usuario2)))
    if bool(usuario1):
        logging.warning('prueba tipo_user'+str(usuario1.tipo_user))
        num1=usuario1.tipo_user    
        if num1==1:
            datosquery=Vehiculo.objects.filter(id_viajero=usuario1)

    if bool(usuario2):
        num1=usuario2.tipo_user  
        logging.warning('prueba tipo_user'+str(usuario2.tipo_user))
        if num1==2:
            empleados=Viajero.objects.filter(id_empresa=usuario2)
            i=0
            for empre in empleados:
                if i<1:
                    datosquery=Vehiculo.objects.filter(id_viajero=empre)
                    i=i+1
                    logging.warning('PASO EN UN SOLO LADO A :'+str(i)) 
                else:
                    datosquery.union(Vehiculo.objects.filter(id_viajero=empre)).values()
                    logging.warning('PASO EN UN SOLO LADO B')


    logging.warning('Aver: '+ str(User.objects.filter(id=request.user.id)))
    num=1
    if request.GET.__contains__('page'):
        num=request.GET.get('page')

    busque=request.GET.get('search')

    if request.POST.__contains__('del'):
        elim=request.POST['del']
        Vehiculo.objects.get(placa_vehiculo=elim).delete()

    if request.GET.__contains__('search'):
        busque=Vehiculo.objects.filter(placa_vehiculo=busque).values() | Vehiculo.objects.filter(marca_vehiculo=busque).values() | Vehiculo.objects.filter(modelo_vehiculo=busque).values()
        pagi=Paginator(busque,8)
        datos=pagi.get_page(num)
    else:
        pagi=Paginator(datosquery ,8)
        datos=pagi.get_page(num)

    context={
        'login': request.user,
        'paginacion': datos
    }

    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def details_vehiculo(request):  
    template = loader.get_template('detallesVehiculo.html')
    num=request.GET.get('id')
    datos=Vehiculo.objects.filter(placa_vehiculo=num).first()
    context={
        'login': request.user,
        'datos': datos
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def update_vehiculo(request):  
    template = loader.get_template('modificarVehiculo.html')

    if request.method=='POST':
        placa=request.POST['placa']
        marca=request.POST['marca']
        modelo=request.POST['placa']
        nac=request.POST['nac']
        color=request.POST['color']
        Vehiculo.objects.filter(placa_vehiculo=placa).update(placa_vehiculo=placa, marca_vehiculo=marca, modelo_vehiculo=modelo, nacionalidad_vehiculo=nac, color_vehiculo=color)

    num=request.GET.get('id')
    datos=Vehiculo.objects.filter(placa_vehiculo=num).first()
    context={
        'login': request.user,
        'datos': datos
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def add_vehiculo(request):  
    template = loader.get_template('registroVehiculo.html')
    usuario=request.user


    if request.method=='POST':
        placa=request.POST['placa']
        marca=request.POST['marca']
        modelo=request.POST['placa']
        nac=request.POST['nac']
        color=request.POST['color']
        via=Viajero.objects.get(usuario_viajero=User.objects.get(id=request.user.id))
        newvehiculo=Vehiculo(id_viajero=via,placa_vehiculo=placa, marca_vehiculo=marca, modelo_vehiculo=modelo, nacionalidad_vehiculo=nac, color_vehiculo=color)
        newvehiculo.save()
        return redirect('/adminv/'+str(request.user.id))

    context={
        'login': usuario
    }
    return HttpResponse(template.render(context, request))

