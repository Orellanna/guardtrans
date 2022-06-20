from datetime import datetime
import logging
from re import template
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpRequest
from django.template import loader
from django.test import RequestFactory
from Modelos.models import RegistroAduanero, User,Empresa,Vehiculo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url="/login")
def init_empresa(request):  
    template = loader.get_template('InicioDeSesionEmpresa.html')
    usuario=request.user
    context={
        'login': usuario
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def empresa_update(request):
    if request.method=='POST':
        nom=request.POST['nombre']
        nac=request.POST['nac']
        reg=request.POST['reg']
        if request.POST.__contains__('user') and request.POST.__contains__('pass'):
            User.objects.filter(id=request.user.id).update(username=request.POST['user'])
            Empresa.objects.filter(usuario_empresa=request.user.id).update(nombre_empresa=nom, nacionalidad_empresa=nac, registro_empresa=reg)
        else:
            Empresa.objects.filter(usuario_empresa=request.user.id).update(nombre_empresa=nom, nacionalidad_empresa=nac, registro_empresa=reg)

    empresa2=Empresa.objects.filter(usuario_empresa=request.user.id).first()
    context={
        'login': request.user,
        'empresa':empresa2
    }

    template=loader.get_template('modificarEmpresa.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def admin_aduanero(request):

    num=1
    num=request.GET.get('page')
    pagi=Paginator(RegistroAduanero.objects.filter(estado_registro=False) ,8)
    datos=pagi.get_page(num)

    context={
        'login': request.user,
        'paginacion': datos,
        'fecha': datetime.now()
    }

    logging.warning('valor de datos: '+ str(datos.paginator.count))

    template=loader.get_template('gestionAduanera.html')

    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def registro_aduanero(request):

    num=1
    num=request.GET.get('page')
    pagi=Paginator(RegistroAduanero.objects.filter(reg_registro=True) ,8)
    datos=pagi.get_page(num)

    context={
        'login': request.user,
        'paginacion': datos,
    }


    template=loader.get_template('registroAduana.html')

    return HttpResponse(template.render(context, request))


@login_required(login_url="/login")
def adunero_info(request):

    id=request.GET.get('id')
    datos=RegistroAduanero.objects.filter(id_registro=id).first()

    if request.POST.__contains__('val1'):
        RegistroAduanero.objects.filter(id_registro=id).update(estado_registro=True, reg_registro=True)
            
    if request.POST.__contains__('val2'):
        RegistroAduanero.objects.filter(id_registro=id).update(estado_registro=False, reg_registro=True)

    logging.warning('probando valor: '+str(datos.id_viajero.nombre_viajero))
    context={
        'login': request.user,
        'item': datos,
    }

    template=loader.get_template('informacionAduanera.html')
    return HttpResponse(template.render(context, request))


def salir(request):
    logout(request)
    return redirect('/')