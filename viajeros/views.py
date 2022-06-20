
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from Modelos.models import Empresa, User, Viajero
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here

@login_required(login_url="/login")
def init_viajero(request):
    template = loader.get_template('inicioDeSesionViajero.html')
    usuario=request.user
    context={
        'login': usuario
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login")
def actualizar_viajero(request, username = None):
    template = loader.get_template('actualizarInformacionViajero.html')

    userviajero = request.user

    if username and username == userviajero.username:
        info = Viajero.objects.filter(usuario_viajero = userviajero).first()

        if request.method=='POST':
            nombre = request.POST['nombre_v']
            apellido = request.POST['apellido_v']
            cargo = request.POST['cargo_v']
            nacionalidad = request.POST['nacionalidad_v']

            viajeroAct = Viajero.objects.filter(usuario_viajero = userviajero).update(nombre_viajero =nombre, apellido_viajero=apellido,
                        cargo_viajero = cargo, nacionalidad_viajero = nacionalidad)   
        
            info = Viajero.objects.filter(usuario_viajero = userviajero).first()
            messages.add_message(request=request, level=messages.SUCCESS, message="Cambios guardados!!")
    context={
        'login': request.user, 
        'info': info
    }
    return HttpResponse(template.render(context, request))



# VIEWS DE EMPRESA!-----
def detalles_viajero(request, username = None):
    template = loader.get_template('detallesViajero.html')
    userempre = request.user
    num=request.GET.get('id')
    info = Viajero.objects.filter(id_viajero = num).first()
   
    context={

        'login': request.user,
        'info': info
    }
    return HttpResponse(template.render(context, request))
    

#ADMINISTRAR VIAJERO!!!!------

@login_required(login_url="/login")
def admin_viajeros(request, username = None):  

    template = loader.get_template('administrarViajero.html')
    userempresa = request.user
    empresa = Empresa.objects.get(usuario_empresa = userempresa)

    num=1
    num=request.GET.get('page')
    busqueda = request.GET.get('search')

    if request.GET.__contains__('search'):  
        busqueda = Viajero.objects.filter( id_viajero = busqueda ).values() | Viajero.objects.filter(usuario_viajero=busqueda).values() | Viajero.objects.filter(nombre_viajero=busqueda).values()
        pagi=Paginator(busqueda,8)
    else:
        pagi=Paginator(Viajero.objects.filter( id_empresa = empresa.id_empresa ).values() ,8)
        datos=pagi.get_page(num)

    context={
        'login': request.user,
       'paginacion': datos
    }

    return HttpResponse(template.render(context, request))
    

@login_required(login_url="/login")
def modificar_viajero(request, username = None):

    template = loader.get_template('modificarViajero.html')
    userempresa = request.user

    num=request.GET.get('id')

    info = Viajero.objects.filter(id_viajero = num).first()

    if request.method=='POST':
        nombre = request.POST['nombre_v']
        apellido = request.POST['apellido_v']
        cargo = request.POST['cargo_v']
        nacionalidad = request.POST['nacionalidad_v']

        viajeroAct = Viajero.objects.filter(id_viajero = num).update(nombre_viajero =nombre,
        apellido_viajero=apellido, cargo_viajero = cargo, nacionalidad_viajero = nacionalidad)   
        
        info = Viajero.objects.filter(id_viajero = num)
        return redirect('/adminu/request.user.username')

    context={
        'login': request.user, 
        'info': info
    }
    return HttpResponse(template.render(context, request))


def eliminar_viajero(request, id_viajero = None):

    userviajero = request.viajero
    template = loader.get_template('administrarViajero.html')
    
    viajerodelete = Viajero.objects.get( id_viajero = userviajero.id_viajero)
    viajerodelete.delele()

    

